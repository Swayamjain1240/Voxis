from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import nn


@dataclass
class EpochResult:
    loss: float
    accuracy: float


class SignTrainer:
    def __init__(
        self,
        model: nn.Module,
        optimizer: torch.optim.Optimizer,
        criterion: nn.Module,
        device: str,
        gradient_clip_norm: float = 1.0,
    ):
        self.model = model
        self.optimizer = optimizer
        self.criterion = criterion
        self.device = torch.device(device)
        self.gradient_clip_norm = (
            gradient_clip_norm
        )

        self.model.to(
            self.device
        )

    def _accuracy(
        self,
        logits,
        targets,
    ) -> float:
        predictions = (
            logits.argmax(dim=1)
        )

        return (
            predictions == targets
        ).float().mean().item()

    def train_epoch(
        self,
        loader,
    ) -> EpochResult:

        self.model.train()

        total_loss = 0.0
        total_accuracy = 0.0
        batches = 0

        for inputs, targets in loader:
            inputs = inputs.to(
                self.device
            )
            targets = targets.to(
                self.device
            )

            self.optimizer.zero_grad(
                set_to_none=True
            )

            logits = self.model(
                inputs
            )

            loss = self.criterion(
                logits,
                targets,
            )

            loss.backward()

            if (
                self.gradient_clip_norm
                > 0
            ):
                torch.nn.utils.clip_grad_norm_(
                    self.model.parameters(),
                    self.gradient_clip_norm,
                )

            self.optimizer.step()

            total_loss += (
                loss.item()
            )

            total_accuracy += (
                self._accuracy(
                    logits,
                    targets,
                )
            )

            batches += 1

        if batches == 0:
            return EpochResult(
                loss=0.0,
                accuracy=0.0,
            )

        return EpochResult(
            loss=total_loss / batches,
            accuracy=(
                total_accuracy
                / batches
            ),
        )

    @torch.no_grad()
    def evaluate(
        self,
        loader,
    ) -> EpochResult:

        self.model.eval()

        total_loss = 0.0
        total_accuracy = 0.0
        batches = 0

        for inputs, targets in loader:
            inputs = inputs.to(
                self.device
            )
            targets = targets.to(
                self.device
            )

            logits = self.model(
                inputs
            )

            loss = self.criterion(
                logits,
                targets,
            )

            total_loss += (
                loss.item()
            )

            total_accuracy += (
                self._accuracy(
                    logits,
                    targets,
                )
            )

            batches += 1

        if batches == 0:
            return EpochResult(
                loss=0.0,
                accuracy=0.0,
            )

        return EpochResult(
            loss=total_loss / batches,
            accuracy=(
                total_accuracy
                / batches
            ),
        )
