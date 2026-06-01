import * as SecureStore from "expo-secure-store";
import { create } from "zustand";

import type { Analysis, PhotoUpload, QuestionnaireInput, RecommendationResponse } from "@/types/api";

export type CaptureAngle = "front" | "left" | "right";

export type CapturedImage = {
  uri: string;
  name: string;
  type: string;
  angle: CaptureAngle;
  confidence: number;
};

type AngleImages = Record<CaptureAngle, CapturedImage | null>;
export type RoutineLog = {
  morning: boolean;
  sunscreen: boolean;
  evening: boolean;
  retinol: boolean;
};

type RoutineKey = keyof RoutineLog;
const ROUTINE_LOG_KEY = "lumiskin.routineLog";

type AnalysisState = {
  photoConsentAccepted: boolean;
  capturedImages: AngleImages;
  uploadedPhotos: Record<CaptureAngle, PhotoUpload | null>;
  questionnaire: QuestionnaireInput | null;
  goals: string[];
  latestAnalysis: Analysis | null;
  latestRecommendation: RecommendationResponse | null;
  routineLog: Record<string, RoutineLog>;
  setPhotoConsentAccepted: (accepted: boolean) => void;
  setCapturedImage: (angle: CaptureAngle, image: CapturedImage | null) => void;
  setUploadedPhoto: (angle: CaptureAngle, photo: PhotoUpload | null) => void;
  setQuestionnaire: (questionnaire: QuestionnaireInput | null) => void;
  setGoals: (goals: string[]) => void;
  setLatestAnalysis: (analysis: Analysis | null) => void;
  setLatestRecommendation: (recommendation: RecommendationResponse | null) => void;
  toggleRoutineItem: (date: string, key: RoutineKey) => void;
  hydrateRoutineLog: () => Promise<void>;
  resetSession: () => void;
};

export const useAnalysisStore = create<AnalysisState>((set) => ({
  photoConsentAccepted: false,
  capturedImages: { front: null, left: null, right: null },
  uploadedPhotos: { front: null, left: null, right: null },
  questionnaire: null,
  goals: [],
  latestAnalysis: null,
  latestRecommendation: null,
  routineLog: {},
  setPhotoConsentAccepted: (photoConsentAccepted) => set({ photoConsentAccepted }),
  setCapturedImage: (angle, image) =>
    set((state) => ({ capturedImages: { ...state.capturedImages, [angle]: image } })),
  setUploadedPhoto: (angle, photo) =>
    set((state) => ({ uploadedPhotos: { ...state.uploadedPhotos, [angle]: photo } })),
  setQuestionnaire: (questionnaire) => set({ questionnaire }),
  setGoals: (goals) => set({ goals }),
  setLatestAnalysis: (latestAnalysis) => set({ latestAnalysis }),
  setLatestRecommendation: (latestRecommendation) => set({ latestRecommendation }),
  toggleRoutineItem: (date, key) =>
    set((state) => {
      const current = state.routineLog[date] ?? {
        morning: false,
        sunscreen: false,
        evening: false,
        retinol: false,
      };
      const routineLog = {
        ...state.routineLog,
        [date]: { ...current, [key]: !current[key] },
      };
      void SecureStore.setItemAsync(ROUTINE_LOG_KEY, JSON.stringify(routineLog));
      return {
        routineLog,
      };
    }),
  hydrateRoutineLog: async () => {
    const raw = await SecureStore.getItemAsync(ROUTINE_LOG_KEY);
    if (!raw) {
      return;
    }
    set({ routineLog: JSON.parse(raw) as Record<string, RoutineLog> });
  },
  resetSession: () => {
    void SecureStore.deleteItemAsync(ROUTINE_LOG_KEY);
    set({
      photoConsentAccepted: false,
      capturedImages: { front: null, left: null, right: null },
      uploadedPhotos: { front: null, left: null, right: null },
      questionnaire: null,
      goals: [],
      latestAnalysis: null,
      latestRecommendation: null,
      routineLog: {},
    });
  },
}));
