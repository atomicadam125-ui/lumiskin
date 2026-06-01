import axios from "axios";

import { appConfig } from "@/constants/config";
import { useAuthStore } from "@/store/authStore";

export const api = axios.create({
  baseURL: appConfig.apiBaseUrl,
  timeout: 30000,
});

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().accessToken;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
