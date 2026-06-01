import { router } from "expo-router";
import { useEffect, useRef, useState } from "react";
import { ActivityIndicator, StyleSheet, View } from "react-native";

import {
  createAnalysis,
  createQuestionnaire,
  generateRecommendation,
  analyzeImageLocally,
  uploadImage,
} from "@/api/skincare";
import { AppText } from "@/components/AppText";
import { Button } from "@/components/Button";
import { Card } from "@/components/Card";
import { Screen } from "@/components/Screen";
import { colors, spacing } from "@/constants/theme";
import { useAnalysisStore } from "@/store/analysisStore";
import { analysisToRecommendationInput, fuseCaptureScores } from "@/utils/scores";

const steps = [
  "Uploading front and side profile photos",
  "Running AI analysis",
  "Building routine",
  "Finalizing dashboard",
];

export default function AnalysisLoadingScreen() {
  const started = useRef(false);
  const [step, setStep] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const capturedImages = useAnalysisStore((state) => state.capturedImages);
  const questionnaire = useAnalysisStore((state) => state.questionnaire);
  const goals = useAnalysisStore((state) => state.goals);
  const setUploadedPhoto = useAnalysisStore((state) => state.setUploadedPhoto);
  const setLatestAnalysis = useAnalysisStore((state) => state.setLatestAnalysis);
  const setLatestRecommendation = useAnalysisStore((state) => state.setLatestRecommendation);

  useEffect(() => {
    if (started.current) {
      return;
    }
    started.current = true;

    async function runAnalysis() {
      const frontImage = capturedImages.front;
      const leftImage = capturedImages.left;
      const rightImage = capturedImages.right;
      if (!frontImage || !leftImage || !rightImage || !questionnaire) {
        router.replace("/(app)/camera");
        return;
      }

      try {
        setStep(0);
        const [frontPhoto, leftPhoto, rightPhoto] = await Promise.all([
          uploadImage(frontImage),
          uploadImage(leftImage),
          uploadImage(rightImage),
        ]);
        setUploadedPhoto("front", frontPhoto);
        setUploadedPhoto("left", leftPhoto);
        setUploadedPhoto("right", rightPhoto);

        setStep(1);
        const angleScores = await Promise.all([
          analyzeImageLocally(frontImage).catch(() => null),
          analyzeImageLocally(leftImage).catch(() => null),
          analyzeImageLocally(rightImage).catch(() => null),
        ]);
        const cvScores = fuseCaptureScores(angleScores);
        const savedQuestionnaire = await createQuestionnaire(questionnaire);
        const analysis = await createAnalysis({
          photo_id: frontPhoto.id,
          questionnaire_id: savedQuestionnaire.id,
          photo_ids: [frontPhoto.id, leftPhoto.id, rightPhoto.id],
          scores: cvScores ?? undefined,
          model_versions: { capture_angles: "front,left,right" },
        });
        setLatestAnalysis(analysis);

        setStep(2);
        const recommendation = await generateRecommendation(
          analysisToRecommendationInput(analysis, {
            age: 28,
            gender: "female",
            skin_type: questionnaire.skin_type,
            goals,
          }),
        );
        setLatestRecommendation(recommendation);

        setStep(3);
        setTimeout(() => router.replace("/(app)/results"), 500);
      } catch {
        setError("Analysis could not be completed. Please try another image.");
      }
    }

    void runAnalysis();
  }, [
    capturedImages,
    goals,
    questionnaire,
    setLatestAnalysis,
    setLatestRecommendation,
    setUploadedPhoto,
  ]);

  return (
    <Screen scroll={false}>
      <View style={styles.center}>
        <Card style={styles.card}>
          <ActivityIndicator size="large" color={colors.ink} />
          <AppText variant="title">Analyzing your skin</AppText>
          <AppText muted>{error ?? steps[step]}</AppText>
          {error ? (
            <View style={styles.errorActions}>
              <Button
                label="Try another image"
                icon="camera-outline"
                variant="secondary"
                onPress={() => router.replace("/(app)/camera")}
              />
              <Button
                label="Review upload"
                icon="image-outline"
                variant="ghost"
                onPress={() => router.replace("/(app)/upload")}
              />
            </View>
          ) : null}
        </Card>
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  center: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  },
  card: {
    width: "100%",
    alignItems: "center",
    paddingVertical: spacing.xl,
  },
  errorActions: {
    width: "100%",
    gap: spacing.sm,
    marginTop: spacing.md,
  },
});
