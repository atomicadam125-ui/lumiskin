import * as FileSystem from "expo-file-system";

import type { CaptureAngle } from "@/store/analysisStore";
import type { CVAnalysisScores } from "@/types/api";

export const REQUIRED_CONFIDENCE = 80;

export const captureRequirements: Record<CaptureAngle, { title: string; instruction: string }> = {
  front: {
    title: "Front selfie",
    instruction: "Face the camera directly. Keep forehead, cheeks, chin, and jaw visible.",
  },
  left: {
    title: "Left profile",
    instruction: "Turn your face to the left about 45-70 degrees. Keep the left cheek and jaw visible.",
  },
  right: {
    title: "Right profile",
    instruction: "Turn your face to the right about 45-70 degrees. Keep the right cheek and jaw visible.",
  },
};

export const captureTips = [
  "Use bright, even natural light facing a window.",
  "Avoid direct sun, car shadows, colored lighting, and backlighting.",
  "Remove sunglasses, masks, heavy filters, and anything covering the cheeks or jaw.",
  "Hold the camera steady at eye level and keep your face inside the guide.",
  "Use clean skin or light skincare only when possible.",
];

export async function estimateImageConfidence(uri: string, cvScores?: CVAnalysisScores | null) {
  if (cvScores?.confidence !== undefined) {
    return cvScores.confidence;
  }

  const info = await FileSystem.getInfoAsync(uri);
  if (!info.exists) {
    return 0;
  }

  const size = "size" in info && typeof info.size === "number" ? info.size : 0;
  if (size >= 900_000) {
    return 84;
  }
  if (size >= 450_000) {
    return 76;
  }
  if (size >= 180_000) {
    return 62;
  }
  return 45;
}

export function qualityMessage(confidence: number) {
  if (confidence >= REQUIRED_CONFIDENCE) {
    return "Image quality passed.";
  }
  if (confidence >= 65) {
    return "Almost there. Try brighter, more even lighting and hold the camera steady.";
  }
  return "Retake needed. Use brighter light, center your face, and avoid shadows or blur.";
}
