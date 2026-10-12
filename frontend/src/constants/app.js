import vocabulary from "../../../shared/vocabulary/vocabulary.json";
import contextDefinitions from "../../../shared/vocabulary/contexts.json";

export const APP_NAME = "VOXIS";

export const APP_PHASE = 1;

export const MAX_SIGN_SEQUENCE_LENGTH = 60;

export const MVP_GLOSSES = Object.freeze(vocabulary.items.map((item) => item.gloss));
export const CONTEXTS = Object.freeze(Object.keys(contextDefinitions.contexts));
export const VOCABULARY_VERSION = vocabulary.version;
