import Constants from "expo-constants";

const extra = Constants.expoConfig?.extra as
  | { apiBaseUrl?: string; privacyPolicyUrl?: string }
  | undefined;

export const appConfig = {
  apiBaseUrl:
    process.env.EXPO_PUBLIC_API_BASE_URL ??
    extra?.apiBaseUrl ??
    "http://localhost:8000/api/v1",
  privacyPolicyUrl: extra?.privacyPolicyUrl?.trim() || null,
};
