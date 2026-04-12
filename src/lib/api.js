const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function runScan({ domain, email, name }) {
  const response = await fetch(`${API_URL}/scan`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ domain, email, name }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || "Scan failed. Please try again.");
  }

  return response.json();
}
