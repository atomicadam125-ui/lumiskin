import Constants from "expo-constants";

const extra = Constants.expoConfig?.extra as
  | { apiBaseUrl?: string; cvBaseUrl?: string; privacyPolicyUrl?: string }
  | undefined;

export const appConfig = {
  apiBaseUrl: extra?.apiBaseUrl ?? "http://localhost:8000/api/v1",
  cvBaseUrl: extra?.cvBaseUrl ?? "http://localhost:8010/v1",
  privacyPolicyUrl: extra?.privacyPolicyUrl?.trim() || null,
};
