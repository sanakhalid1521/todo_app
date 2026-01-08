// Authentication utilities for the frontend.

// Authentication utilities for managing tokens and user data in localStorage/sessionStorage

export function getToken(): string | null {
  if (typeof window !== "undefined") {
    return localStorage.getItem("token") || sessionStorage.getItem("token");
  }
  return null;
}

export function setToken(token: string): void {
  if (typeof window !== "undefined") {
    // Store in both localStorage and sessionStorage depending on preference
    localStorage.setItem("token", token);
    sessionStorage.setItem("token", token);
  }
}

export function removeToken(): void {
  if (typeof window !== "undefined") {
    localStorage.removeItem("token");
    sessionStorage.removeItem("token");
    localStorage.removeItem("userId");
    localStorage.removeItem("userEmail");
    localStorage.removeItem("userName");
  }
}

export function getUserId(): string | null {
  if (typeof window !== "undefined") {
    return localStorage.getItem("userId") || "user-demo";
  }
  return "user-demo"; // Default fallback
}

export function setUserId(userId: string): void {
  if (typeof window !== "undefined") {
    localStorage.setItem("userId", userId);
  }
}

export function getUserEmail(): string | null {
  if (typeof window !== "undefined") {
    return localStorage.getItem("userEmail") || "demo@example.com";
  }
  return "demo@example.com"; // Default fallback
}

export function setUserEmail(email: string): void {
  if (typeof window !== "undefined") {
    localStorage.setItem("userEmail", email);
  }
}

export function getUserName(): string | null {
  if (typeof window !== "undefined") {
    return localStorage.getItem("userName") || "Demo User";
  }
  return "Demo User"; // Default fallback
}

export function setUserName(name: string): void {
  if (typeof window !== "undefined") {
    localStorage.setItem("userName", name);
  }
}

export function isAuthenticated(): boolean {
  return !!getToken();
}

export function logout(): void {
  removeToken();
  if (typeof window !== "undefined") {
    window.location.href = "/signin";
  }
}
