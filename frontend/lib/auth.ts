// Authentication utilities for the frontend.

import { createAuthClient } from "better-auth";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});

export function getToken(): string | null {
  if (typeof window !== "undefined") {
    return localStorage.getItem("token");
  }
  return null;
}

export function setToken(token: string): void {
  if (typeof window !== "undefined") {
    localStorage.setItem("token", token);
  }
}

export function removeToken(): void {
  if (typeof window !== "undefined") {
    localStorage.removeItem("token");
    localStorage.removeItem("userId");
  }
}

export function getUserId(): string | null {
  if (typeof window !== "undefined") {
    return localStorage.getItem("userId");
  }
  return null;
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
