/**
 * Shared Speech -> Sign pipeline shape.
 *
 * @typedef {Object} SpeechResult
 * @property {string} text
 * @property {string} language
 * @property {number|null} confidence
 * @property {string} source
 * @property {number} timestamp
 */

/**
 * Shared gloss sequence shape.
 *
 * @typedef {Object} GlossSequence
 * @property {string[]} glosses
 * @property {number[]} confidence
 * @property {"speech"|"sign"} source
 * @property {number} timestamp
 */

/**
 * Future avatar request.
 *
 * @typedef {Object} AvatarAnimationRequest
 * @property {string} gloss
 * @property {number} index
 */
