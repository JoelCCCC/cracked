import {
  DashboardData,
  HistoryData,
  LevelDetail,
  SubmitResult,
  TrackSummary,
  User,
} from "@/types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ||
  (typeof window !== "undefined" ? "" : "http://localhost:8000");

const ACCESS_KEY = "cracked_access_token";
const REFRESH_KEY = "cracked_refresh_token";

export function getAccessToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(ACCESS_KEY);
}

export function getRefreshToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(REFRESH_KEY);
}

export function setTokens(access: string, refresh: string) {
  if (typeof window === "undefined") return;
  localStorage.setItem(ACCESS_KEY, access);
  localStorage.setItem(REFRESH_KEY, refresh);
}

export function clearTokens() {
  if (typeof window === "undefined") return;
  localStorage.removeItem(ACCESS_KEY);
  localStorage.removeItem(REFRESH_KEY);
}

async function refreshAccessToken(): Promise<string | null> {
  const refresh = getRefreshToken();
  if (!refresh) return null;

  try {
    const res = await fetch(`${API_BASE_URL}/api/auth/token/refresh/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh }),
    });
    if (!res.ok) {
      clearTokens();
      return null;
    }
    const data = await res.json();
    if (data.access) {
      localStorage.setItem(ACCESS_KEY, data.access);
      if (data.refresh) localStorage.setItem(REFRESH_KEY, data.refresh);
      return data.access;
    }
  } catch {
    clearTokens();
  }
  return null;
}

export async function request<T>(
  path: string,
  options: RequestInit = {},
  requiresAuth: boolean = true
): Promise<T> {
  const url = `${API_BASE_URL}${path}`;
  const headers = new Headers(options.headers || {});
  if (!headers.has("Content-Type") && !(options.body instanceof FormData)) {
    headers.set("Content-Type", "application/json");
  }

  let token = getAccessToken();
  if (requiresAuth && token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  let response = await fetch(url, { ...options, headers });

  if (response.status === 401 && requiresAuth) {
    // Attempt token refresh
    token = await refreshAccessToken();
    if (token) {
      headers.set("Authorization", `Bearer ${token}`);
      response = await fetch(url, { ...options, headers });
    }
  }

  if (!response.ok) {
    let errorData: any = null;
    try {
      errorData = await response.json();
    } catch {
      try {
        const text = await response.text();
        if (text) {
          // If response is HTML or text, pick a brief preview
          const cleanedText = text.replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim();
          errorData = { detail: cleanedText.slice(0, 200) };
        }
      } catch {
        // ignore
      }
    }

    let message = "";
    if (errorData) {
      if (typeof errorData === "string") {
        message = errorData;
      } else if (errorData.detail && typeof errorData.detail === "string") {
        message = errorData.detail;
      } else if (errorData.error && typeof errorData.error === "string") {
        message = errorData.error;
      } else if (Array.isArray(errorData.non_field_errors) && errorData.non_field_errors.length > 0) {
        message = errorData.non_field_errors.join(", ");
      } else if (Array.isArray(errorData)) {
        message = errorData.map((e) => (typeof e === "string" ? e : JSON.stringify(e))).join(", ");
      } else if (typeof errorData === "object") {
        const fieldErrors = Object.entries(errorData)
          .map(([field, errs]) => {
            const fieldLabel = field.replace(/_/g, " ");
            let errStr = "";
            if (Array.isArray(errs)) {
              errStr = errs.map((e) => (typeof e === "string" ? e : (e as any)?.message || JSON.stringify(e))).join(" ");
            } else if (typeof errs === "object" && errs !== null) {
              errStr = JSON.stringify(errs);
            } else {
              errStr = String(errs);
            }
            return `${fieldLabel}: ${errStr}`;
          });
        if (fieldErrors.length > 0) {
          message = fieldErrors.join(" | ");
        }
      }
    }

    if (!message) {
      message = `Request failed with status ${response.status}`;
    }

    const err: any = new Error(message);
    err.status = response.status;
    err.data = errorData;
    throw err;
  }

  return response.json();
}

export const api = {
  auth: {
    async register(data: {
      username: string;
      email: string;
      password: string;
      display_name?: string;
    }): Promise<{ user: User; access: string; refresh: string }> {
      const res = await request<{ user: User; access: string; refresh: string }>(
        "/api/auth/register/",
        {
          method: "POST",
          body: JSON.stringify(data),
        },
        false
      );
      setTokens(res.access, res.refresh);
      return res;
    },

    async login(data: {
      username: string;
      password: string;
    }): Promise<{ access: string; refresh: string }> {
      const res = await request<{ access: string; refresh: string }>(
        "/api/auth/token/",
        {
          method: "POST",
          body: JSON.stringify(data),
        },
        false
      );
      setTokens(res.access, res.refresh);
      return res;
    },

    async personalLogin(): Promise<{ user: User; access: string; refresh: string }> {
      const res = await request<{ user: User; access: string; refresh: string }>(
        "/api/auth/personal-login/",
        {
          method: "POST",
        },
        false
      );
      setTokens(res.access, res.refresh);
      return res;
    },

    async me(): Promise<User> {
      return request<User>("/api/auth/me/");
    },

    async updateProfile(data: Partial<User>): Promise<User> {
      return request<User>("/api/auth/me/", {
        method: "PATCH",
        body: JSON.stringify(data),
      });
    },

    logout() {
      clearTokens();
    },
  },

  curriculum: {
    async getPublicTracks(): Promise<TrackSummary[]> {
      return request<TrackSummary[]>("/api/tracks/public/", {}, false);
    },

    async getTracks(): Promise<TrackSummary[]> {
      return request<TrackSummary[]>("/api/tracks/");
    },

    async getTrack(slug: string): Promise<TrackSummary> {
      return request<TrackSummary>(`/api/tracks/${slug}/`);
    },

    async getLevel(id: number): Promise<LevelDetail> {
      return request<LevelDetail>(`/api/levels/${id}/`);
    },
  },

  progress: {
    async submitChallenge(
      challengeId: number,
      submission: Record<string, unknown>
    ): Promise<SubmitResult> {
      return request<SubmitResult>(`/api/challenges/${challengeId}/submit/`, {
        method: "POST",
        body: JSON.stringify(submission),
      });
    },

    async getDashboard(): Promise<DashboardData> {
      return request<DashboardData>("/api/dashboard/");
    },

    async getHistory(): Promise<HistoryData> {
      return request<HistoryData>("/api/history/");
    },

    async resetLevel(levelId: number): Promise<{ success: boolean; detail: string }> {
      return request<{ success: boolean; detail: string }>(
        `/api/levels/${levelId}/reset/`,
        { method: "POST" }
      );
    },
  },
};
