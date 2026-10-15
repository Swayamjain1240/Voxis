import { useCallback, useEffect, useRef, useState } from "react";

import {
  createAudioRecorder,
  getSupportedMimeType,
} from "../services/audioRecorder";
import { uploadSpeechAudio } from "../../../services/api";

function formatDuration(seconds) {
  const minutes = Math.floor(seconds / 60);
  const remainder = seconds % 60;

  return `${String(minutes).padStart(2, "0")}:${String(remainder).padStart(
    2,
    "0"
  )}`;
}

export default function useMicrophone() {
  const [status, setStatus] = useState("idle");
  const [error, setError] = useState("");
  const [duration, setDuration] = useState(0);
  const [audioBlob, setAudioBlob] = useState(null);
  const [audioUrl, setAudioUrl] = useState("");
  const [uploadStatus, setUploadStatus] = useState("idle");
  const [uploadError, setUploadError] = useState("");
  const [uploadResult, setUploadResult] = useState(null);

  const streamRef = useRef(null);
  const recorderRef = useRef(null);
  const timerRef = useRef(null);

  const isSupported =
    typeof navigator !== "undefined" &&
    Boolean(navigator.mediaDevices?.getUserMedia) &&
    typeof MediaRecorder !== "undefined";

  const stopTimer = useCallback(() => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
  }, []);

  const cleanupStream = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
  }, []);

  const resetAudio = useCallback(() => {
    setAudioBlob(null);
    setUploadStatus("idle");
    setUploadError("");
    setUploadResult(null);

    if (audioUrl) {
      URL.revokeObjectURL(audioUrl);
      setAudioUrl("");
    }
  }, [audioUrl]);

  const uploadAudio = useCallback(async () => {
    if (!audioBlob) {
      setUploadStatus("error");
      setUploadError("Record audio before uploading it.");
      return null;
    }

    try {
      setUploadStatus("uploading");
      setUploadError("");
      const result = await uploadSpeechAudio(audioBlob);
      setUploadResult(result);
      setUploadStatus("uploaded");
      return result;
    } catch (uploadRequestError) {
      setUploadStatus("error");
      setUploadError(
        uploadRequestError?.message ||
          "The audio upload could not be completed."
      );
      return null;
    }
  }, [audioBlob]);

  const startRecording = useCallback(async () => {
    if (!isSupported) {
      setError("This browser does not support microphone recording.");
      setStatus("error");
      return;
    }

    try {
      setError("");
      resetAudio();
      setDuration(0);
      setStatus("requesting");

      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          channelCount: 1,
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
        video: false,
      });

      streamRef.current = stream;

      const mimeType = getSupportedMimeType();

      const recorder = createAudioRecorder({
        stream,
        mimeType,

        onStart: () => {
          setStatus("recording");

          stopTimer();

          timerRef.current = window.setInterval(() => {
            setDuration((current) => current + 1);
          }, 1000);
        },

        onStop: (blob) => {
          const objectUrl = URL.createObjectURL(blob);

          setAudioBlob(blob);
          setAudioUrl(objectUrl);
          setStatus("stopped");

          stopTimer();
          cleanupStream();
        },

        onError: (recordingError) => {
          setError(recordingError?.message || "Recording failed.");
          setStatus("error");

          stopTimer();
          cleanupStream();
        },
      });

      recorderRef.current = recorder;
      recorder.start();
    } catch (recordingError) {
      const message =
        recordingError?.name === "NotAllowedError"
          ? "Microphone permission was denied."
          : recordingError?.message || "Unable to access microphone.";

      setError(message);
      setStatus("error");

      stopTimer();
      cleanupStream();
    }
  }, [
    cleanupStream,
    isSupported,
    resetAudio,
    stopTimer,
  ]);

  const stopRecording = useCallback(() => {
    if (recorderRef.current?.state === "recording") {
      recorderRef.current.stop();
    }
  }, []);

  useEffect(() => {
    return () => {
      stopTimer();
      cleanupStream();

      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
      }
    };
  }, [audioUrl, cleanupStream, stopTimer]);

  return {
    isSupported,
    isRecording: status === "recording",
    status,
    error,
    duration,
    durationLabel: formatDuration(duration),
    audioBlob,
    audioUrl,
    uploadStatus,
    uploadError,
    uploadResult,
    startRecording,
    stopRecording,
    uploadAudio,
  };
}
