import { useCallback, useState } from "react";

export default function useAsync(
  asyncFunction
) {
  const [status, setStatus] =
    useState("idle");
  const [error, setError] =
    useState(null);

  const execute = useCallback(
    async (...args) => {
      try {
        setStatus("loading");
        setError(null);

        const result =
          await asyncFunction(
            ...args
          );

        setStatus("success");

        return result;
      } catch (requestError) {
        setStatus("error");
        setError(requestError);

        throw requestError;
      }
    },
    [asyncFunction]
  );

  return {
    execute,
    status,
    error,
    isLoading:
      status === "loading",
  };
}
