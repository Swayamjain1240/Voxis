import pytest

from src.contracts.model_config import ModelConfig, model_config_from_mapping


def test_model_config_matches_canonical_contract():
    config = ModelConfig().validate()
    assert config.input_features == 300
    assert config.sequence_length == 60
    assert config.num_classes == 12
    assert config.as_dict()["config_version"] == "1.0.0"


def test_model_config_rejects_shape_architecture_and_version_drift():
    with pytest.raises(ValueError, match="60 frames"):
        ModelConfig(sequence_length=30).validate()
    with pytest.raises(ValueError, match="Unsupported"):
        ModelConfig(architecture="lstm").validate()
    with pytest.raises(ValueError, match="vocabulary version"):
        ModelConfig(vocabulary_version="2.0.0").validate()


def test_model_config_mapping_round_trip():
    payload = ModelConfig().as_dict()
    assert model_config_from_mapping(payload).model_version == "sign-transformer-0.1.0"
