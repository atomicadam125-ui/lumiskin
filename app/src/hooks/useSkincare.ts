import { useMutation, useQuery } from "@tanstack/react-query";

import {
  analyzeImageLocally,
  createAnalysis,
  createQuestionnaire,
  generateRecommendation,
  getHistory,
  uploadImage,
} from "@/api/skincare";

export function useUploadImage() {
  return useMutation({ mutationFn: uploadImage });
}

export function useCreateQuestionnaire() {
  return useMutation({ mutationFn: createQuestionnaire });
}

export function useCreateAnalysis() {
  return useMutation({ mutationFn: createAnalysis });
}

export function useGenerateRecommendation() {
  return useMutation({ mutationFn: generateRecommendation });
}

export function useAnalyzeImageLocally() {
  return useMutation({ mutationFn: analyzeImageLocally });
}

export function useHistory() {
  return useQuery({
    queryKey: ["history"],
    queryFn: getHistory,
  });
}
