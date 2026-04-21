const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

type ConfigPayload = {
  api_key: string;
  limit: number;
  window: number;
  strategy: string;
};

export async function sendConfig(payload: ConfigPayload) {
  const response = await fetch(`${API_BASE_URL}/config`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.detail ?? data.error ?? "Unable to send configuration");
  }
  return data;
}

export async function checkLimit(apiKey: string) {
  const response = await fetch(`${API_BASE_URL}/check`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": apiKey,
    },
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.detail ?? data.error ?? "Failed to check limit");
  }

  return data;
}