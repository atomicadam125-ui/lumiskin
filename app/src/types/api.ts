export type User = {
  id: string;
  email: string;
  full_name: string | null;
  is_active: boolean;
  created_at: string;
};

export type AuthResponse = {
  access_token: string;
  token_type: "bearer";
};

export type PhotoUpload = {
  id: string;
  s3_key: string;
  original_filename: string | null;
  content_type: string;
  size_bytes: number;
  image_width: number | null;
  image_height: number | null;
  created_at: string;
};

export type QuestionnaireInput = {
  skin_type: "oily" | "dry" | "combination" | "normal" | "sensitive";
  sensitivity_level: number;
  acne_frequency: "rarely" | "sometimes" | "often" | "persistent";
  current_products: string[];
  allergies: string[];
  sun_exposure_level: number;
  sleep_quality: number;
  stress_level: number;
};

export type Analysis = {
  id: string;
  user_id: string;
  photo_id: string;
  questionnaire_id: string | null;
  status: string;
  scores: Record<string, { score: number; severity: string }>;
  skin_profile: Record<string, unknown>;
  model_versions: Record<string, string>;
  created_at: string;
};

export type RecommendationInput = {
  age: number;
  gender: "female" | "male" | "non_binary" | "prefer_not_to_say" | "other";
  skin_type: QuestionnaireInput["skin_type"];
  goals: string[];
  acne_score: number;
  redness_score: number;
  pigmentation_score: number;
  wrinkle_score: number;
  oiliness_score: number;
  dryness_score: number;
};

export type CVAnalysisScores = Omit<
  RecommendationInput,
  "age" | "gender" | "skin_type" | "goals"
> & {
  confidence: number;
};

export type RecommendationResponse = {
  skin_snapshot: SkinSnapshot;
  scores: SkinSnapshot["score"];
  current_skin_tier: SkinSnapshot["score"]["current_tier"];
  what_we_see: { observation: string; reasoning: string }[];
  biggest_improvement_opportunities: {
    concern: string;
    why_it_matters: string;
    priority: number;
  }[];
  ninety_day_plan: { phase: string; focus: string; actions: string[] }[];
  expected_results: {
    short_term: string;
    medium_term: string;
    long_term: string;
    realistic_outcome: string;
  };
  improvement_potential: {
    estimated_potential_score_range: string;
    estimated_30_day_score_increase: number;
    estimated_day_30_score: number;
    estimated_timeline: { phase: string; expected_changes: string[] }[];
    note: string;
  };
  timeline: { phase: string; expected_changes: string[] }[];
  thirty_day_progress: {
    current_score: number;
    estimated_score_increase: number;
    estimated_day_30_score: number;
    focus: string;
    explanation: string;
  };
  ai_confidence: { score: number; explanation: string };
  recommended_products: RecommendedProduct[];
  warnings: { title: string; message: string; severity: "info" | "caution" | "important" }[];
  disclaimer: string;
  skin_summary: string;
  top_concerns: string[];
  morning_routine: RoutineStep[];
  evening_routine: RoutineStep[];
  product_recommendations: ProductRecommendation[];
  ingredient_recommendations: IngredientRecommendation[];
  ingredients_to_avoid: { ingredient: string; reason: string }[];
  lifestyle_suggestions: string[];
  dermatologist_consultation: { level: string; rationale: string };
  medical_disclaimer: string;
};

export type SkinSnapshot = {
  headline: string;
  skin_type: QuestionnaireInput["skin_type"];
  confidence: number;
  score: {
    overall_skin_score: number;
    current_tier:
      | "Exceptional"
      | "Excellent"
      | "Healthy"
      | "Average"
      | "Needs Improvement"
      | "Significant Concerns";
    category_scores: {
      acne_control: number;
      oil_balance: number;
      pigmentation_evenness: number;
      texture_smoothness: number;
      hydration_barrier: number;
    };
  };
};

export type RoutineStep = {
  step: number;
  category: string;
  recommendation: string;
  frequency: string;
  rationale: string;
  product_name: string | null;
  brand: string | null;
  product_url: string | null;
  how_to_use: string | null;
  caution: string | null;
};

export type IngredientRecommendation = {
  ingredient: string;
  why: string;
  how_to_use: string;
};

export type ProductRecommendation = {
  name: string;
  brand: string;
  category: string;
  step: string;
  url: string;
  why: string;
  how_to_use: string;
  caution: string | null;
};

export type RecommendedProduct = {
  product_name: string;
  brand: string;
  category: string;
  step: string;
  url: string;
  why_chosen: string;
  how_often: string;
  caution: string | null;
};

export type UserHistory = {
  photos: PhotoUpload[];
  questionnaires: Array<QuestionnaireInput & { id: string; created_at: string; user_id: string }>;
  analyses: Analysis[];
  recommendations: unknown[];
};
