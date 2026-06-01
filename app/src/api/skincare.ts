import { api, cvApi } from "@/api/client";
import type {
  Analysis,
  CVAnalysisScores,
  PhotoUpload,
  QuestionnaireInput,
  RecommendationInput,
  RecommendationResponse,
  UserHistory,
} from "@/types/api";

export async function uploadImage(image: { uri: string; name: string; type: string }) {
  const form = new FormData();
  form.append("file", {
    uri: image.uri,
    name: image.name,
    type: image.type,
  } as unknown as string);

  const response = await api.post<PhotoUpload>("/uploads/images", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
}

export async function createQuestionnaire(payload: QuestionnaireInput) {
  const response = await api.post<QuestionnaireInput & { id: string }>("/questionnaires", payload);
  return response.data;
}

export async function createAnalysis(payload: {
  photo_id: string;
  photo_ids?: string[];
  questionnaire_id?: string;
  scores?: CVAnalysisScores;
  model_versions?: Record<string, string>;
}) {
  const response = await api.post<Analysis>("/analyses", payload);
  return response.data;
}

export async function generateRecommendation(payload: RecommendationInput) {
  const response = await api.post<RecommendationResponse>("/recommendations/generate", payload);
  return response.data;
}

export async function analyzeImageLocally(image: { uri: string; name: string; type: string }) {
  const form = new FormData();
  form.append("file", {
    uri: image.uri,
    name: image.name,
    type: image.type,
  } as unknown as string);

  const response = await cvApi.post<CVAnalysisScores>("/analyze", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
}

export async function getHistory() {
  const response = await api.get<UserHistory>("/history");
  return response.data;
}
