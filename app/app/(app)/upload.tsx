import * as ImagePicker from "expo-image-picker";
import { router } from "expo-router";
import { Image, Pressable, StyleSheet, View } from "react-native";

import { analyzeImageLocally } from "@/api/skincare";
import { AppText } from "@/components/AppText";
import { Button } from "@/components/Button";
import { Card } from "@/components/Card";
import { Header } from "@/components/Header";
import { Screen } from "@/components/Screen";
import { colors, radii, spacing } from "@/constants/theme";
import { CaptureAngle, useAnalysisStore } from "@/store/analysisStore";
import {
  REQUIRED_CONFIDENCE,
  captureRequirements,
  captureTips,
  estimateImageConfidence,
  qualityMessage,
} from "@/utils/imageQuality";

const angles: CaptureAngle[] = ["front", "left", "right"];

export default function UploadImageScreen() {
  const capturedImages = useAnalysisStore((state) => state.capturedImages);
  const photoConsentAccepted = useAnalysisStore((state) => state.photoConsentAccepted);
  const setPhotoConsentAccepted = useAnalysisStore((state) => state.setPhotoConsentAccepted);
  const setCapturedImage = useAnalysisStore((state) => state.setCapturedImage);
  const allPassed = angles.every(
    (angle) => (capturedImages[angle]?.confidence ?? 0) >= REQUIRED_CONFIDENCE,
  );

  async function pickImage(angle: CaptureAngle) {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 1,
      allowsEditing: true,
      aspect: [3, 4],
    });
    if (result.canceled) {
      return;
    }

    const asset = result.assets[0];
    const image = {
      uri: asset.uri,
      name: asset.fileName ?? `${angle}-selfie.jpg`,
      type: asset.mimeType ?? "image/jpeg",
      angle,
      confidence: 0,
    };
    const cvScores = await analyzeImageLocally(image).catch(() => null);
    const confidence = await estimateImageConfidence(asset.uri, cvScores);
    setCapturedImage(angle, { ...image, confidence });
  }

  return (
    <Screen>
      <Header
        title="Upload three angles"
        subtitle="Front, left profile, and right profile are required before analysis."
      />
      <Card>
        <AppText variant="subtitle">Private photo analysis</AppText>
        <AppText muted>
          Uploads are used for cosmetic skin analysis, progress tracking, and routine generation.
          This is educational guidance, not medical diagnosis.
        </AppText>
        <Pressable
          accessibilityRole="checkbox"
          accessibilityState={{ checked: photoConsentAccepted }}
          onPress={() => setPhotoConsentAccepted(true)}
          style={styles.consentRow}
        >
          <View style={styles.checkbox}>
            <AppText variant="caption">OK</AppText>
          </View>
          <AppText>I consent to photo upload and AI cosmetic analysis.</AppText>
        </Pressable>
      </Card>
      <Card>
        <AppText variant="subtitle">Photo conditions</AppText>
        {captureTips.map((tip) => (
          <AppText key={tip} variant="caption" muted>
            - {tip}
          </AppText>
        ))}
      </Card>
      {angles.map((angle) => {
        const image = capturedImages[angle];
        const passed = (image?.confidence ?? 0) >= REQUIRED_CONFIDENCE;
        return (
          <Card key={angle}>
            <AppText variant="subtitle">{captureRequirements[angle].title}</AppText>
            <AppText muted>{captureRequirements[angle].instruction}</AppText>
            {image ? (
              <Image source={{ uri: image.uri }} style={styles.image} />
            ) : (
              <View style={styles.empty}>
                <AppText muted>No image selected</AppText>
              </View>
            )}
            <AppText variant="caption" muted>
              Confidence: {image ? `${image.confidence}/100` : "not checked"}
            </AppText>
            <AppText variant="caption" style={passed ? styles.pass : styles.fail}>
              {qualityMessage(image?.confidence ?? 0)}
            </AppText>
            <Button
              label={image ? "Replace photo" : "Choose photo"}
              icon="image-outline"
              variant={passed ? "secondary" : "primary"}
              disabled={!photoConsentAccepted}
              onPress={() => void pickImage(angle)}
            />
          </Card>
        );
      })}
      <Button
        label="Continue"
        icon="arrow-forward-outline"
        disabled={!allPassed}
        onPress={() => router.push("/(app)/questionnaire")}
      />
    </Screen>
  );
}

const styles = StyleSheet.create({
  image: {
    width: "100%",
    aspectRatio: 3 / 4,
    borderRadius: radii.md,
    backgroundColor: colors.subtle,
  },
  empty: {
    minHeight: 220,
    borderRadius: radii.md,
    backgroundColor: colors.mint,
    alignItems: "center",
    justifyContent: "center",
  },
  pass: {
    color: colors.sage,
  },
  fail: {
    color: colors.danger,
  },
  consentRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.sm,
  },
  checkbox: {
    width: 26,
    height: 26,
    borderRadius: radii.sm,
    backgroundColor: colors.mint,
    alignItems: "center",
    justifyContent: "center",
  },
});
