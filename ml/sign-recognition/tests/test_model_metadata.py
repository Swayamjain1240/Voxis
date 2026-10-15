import pytest

from src.contracts.label_map import load_label_map
from src.contracts.model_metadata import ModelMetadata, validate_checkpoint_metadata


def checkpoint(**overrides):
    label_map = load_label_map().gloss_to_label
    payload = {
        **ModelMetadata(model_version="sign-transformer-0.1.0").as_dict(),
        "label_map": label_map,
    }
    payload.update(overrides)
    return payload


def test_checkpoint_metadata_requires_canonical_shape_and_versions():
    metadata = validate_checkpoint_metadata(checkpoint())
    assert metadata.model_version == "sign-transformer-0.1.0"
    assert metadata.sequence_length == 60
    assert metadata.input_features == 300

    with pytest.raises(ValueError, match="label map"):
        validate_checkpoint_metadata(checkpoint(label_map={"PAIN": 0}))
    with pytest.raises(ValueError, match="input shape"):
        validate_checkpoint_metadata(checkpoint(sequence_length=30))
    with pytest.raises(ValueError, match="unknown label"):
        validate_checkpoint_metadata(checkpoint(unknown_label=0))


def test_checkpoint_metadata_requires_model_version():
    with pytest.raises(ValueError, match="model_version"):
        validate_checkpoint_metadata(checkpoint(model_version=""))
