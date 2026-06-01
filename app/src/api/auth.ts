import { api } from "@/api/client";
import type { AuthResponse, User } from "@/types/api";

export async function register(payload: {
  email: string;
  password: string;
  full_name?: string;
}): Promise<User> {
  const response = await api.post<User>("/auth/register", payload);
  return response.data;
}

export async function login(payload: { email: string; password: string }): Promise<AuthResponse> {
  const response = await api.post<AuthResponse>("/auth/login", payload);
  return response.data;
}

export async function loginWithApple(payload: {
  identity_token: string;
  full_name?: string;
}): Promise<AuthResponse> {
  const response = await api.post<AuthResponse>("/auth/apple", payload);
  return response.data;
}

export async function getMe(): Promise<User> {
  const response = await api.get<User>("/auth/me");
  return response.data;
}

export async function deleteAccount(): Promise<void> {
  await api.delete("/auth/me");
}
