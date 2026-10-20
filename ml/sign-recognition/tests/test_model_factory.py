import pytest


torch = pytest.importorskip("torch")

from src.contracts.model_config import ModelConfig
from src.models.factory import create_model


@pytest.mark.parametrize("architecture", ["transformer", "conformer"])
def test_model_factory_supports_configured_architectures(architecture):
    model = create_model(ModelConfig(architecture=architecture, d_model=32, num_heads=4))
    output = model(torch.randn(2, 60, 300))
    assert output.shape == (2, 12)
