import type { Analysis, CVAnalysisScores, RecommendationInput } from "@/types/api";

export function analysisToRecommendationInput(
  analysis: Analysis | null,
  overrides: Pick<RecommendationInput, "age" | "gender" | "skin_type" | "goals">,
): RecommendationInput {
  const score = (key: string, fallback: number) => {
    const raw = analysis?.scores?.[key]?.score;
    if (typeof raw !== "number") {
      return fallback;
    }
    return Math.round(raw <= 1 ? raw * 100 : raw);
  };

  return {
    ...overrides,
    acne_score: score("acne", 72),
    redness_score: score("redness", 30),
    pigmentation_score: score("hyperpigmentation", 40),
    wrinkle_score: score("fine_lines", 15),
    oiliness_score: score("oiliness", 70),
    dryness_score: score("dryness", 20),
  };
}

export function metricEntries(input: RecommendationInput) {
  return [
    { label: "Acne", value: input.acne_score, tone: "coral" as const },
    { label: "Redness", value: input.redness_score, tone: "amber" as const },
    { label: "Pigmentation", value: input.pigmentation_score, tone: "blue" as const },
    { label: "Wrinkles", value: input.wrinkle_score, tone: "sage" as const },
    { label: "Oiliness", value: input.oiliness_score, tone: "amber" as const },
    { label: "Dryness", value: input.dryness_score, tone: "blue" as const },
  ];
}

export function fuseCaptureScores(scores: Array<CVAnalysisScores | null>) {
  const usable = scores.filter((score): score is CVAnalysisScores => Boolean(score));
  if (!usable.length) {
    return null;
  }

  const totalConfidence = usable.reduce((sum, score) => sum + Math.max(score.confidence, 1), 0);
  const weighted = (key: keyof Omit<CVAnalysisScores, "confidence">) =>
    Math.round(
      usable.reduce((sum, score) => sum + score[key] * Math.max(score.confidence, 1), 0) /
        totalConfidence,
    );

  return {
    acne_score: weighted("acne_score"),
    redness_score: weighted("redness_score"),
    pigmentation_score: weighted("pigmentation_score"),
    wrinkle_score: weighted("wrinkle_score"),
    oiliness_score: weighted("oiliness_score"),
    dryness_score: weighted("dryness_score"),
    confidence: Math.round(
      usable.reduce((sum, score) => sum + score.confidence, 0) / usable.length,
    ),
  };
}
