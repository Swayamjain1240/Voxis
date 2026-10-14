function readEnv(name, fallback = "") {
  const value = import.meta.env[name];
  return typeof value === "string" ? value.trim() : fallback;
}

export const frontendConfig = Object.freeze({
  appName: readEnv("VITE_APP_NAME", "VOXIS"),
  apiBaseUrl: readEnv(
    "VITE_API_BASE_URL",
    "http://127.0.0.1:8000/api/v1"
  ),
  avatarModelUrl: readEnv("VITE_AVATAR_MODEL_URL"),
  mediaPipeModelUrl: readEnv("VITE_MEDIAPIPE_MODEL_URL"),
  mediaPipeWasmRoot: readEnv("VITE_MEDIAPIPE_WASM_ROOT"),
});

export const mediaPipeConfig = Object.freeze({
  modelAssetPath: frontendConfig.mediaPipeModelUrl,
  wasmRoot: frontendConfig.mediaPipeWasmRoot,
  configured: Boolean(
    frontendConfig.mediaPipeModelUrl &&
      frontendConfig.mediaPipeWasmRoot
  ),
});
