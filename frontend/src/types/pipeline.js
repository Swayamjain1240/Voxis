/**
 * Wire contracts: shared/contracts/*.schema.json (schema version 1.0.0).
 * REST responses use { success, data, meta }; services/api.js unwraps data.
 * All serialized timestamps are timezone-aware ISO-8601 strings.
 *
 * @typedef {Object} SpeechResult
 * @property {"speech_result"} type
 * @property {"1.0.0"} schema_version
 * @property {"1.0.0"} vocabulary_version
 * @property {string} transcript
 * @property {"en"} language
 * @property {number|null} confidence
 * @property {string[]} glosses
 * @property {"microphone"|"audio_file"|"api"} source
 * @property {string} timestamp
 *
 * @typedef {Object} ConversationMessage
 * @property {string} message_id
 * @property {"1.0.0"} schema_version
 * @property {"1.0.0"} vocabulary_version
 * @property {string} sender
 * @property {"speech"|"sign"|"text"|"system"} source
 * @property {"speech"|"sign"|"text"|"avatar"} modality
 * @property {string} text
 * @property {string[]} glosses
 * @property {string|null} context
 * @property {string} timestamp
 */
