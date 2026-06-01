import { CameraView, useCameraPermissions } from "expo-camera";
import { router } from "expo-router";
import { useMemo, useRef, useState } from "react";
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

export default function CameraCaptureScreen() {
  const [permission, requestPermission] = useCameraPermissions();
  const cameraRef = useRef<CameraView>(null);
  const capturedImages = useAnalysisStore((state) => state.capturedImages);
  const photoConsentAccepted = useAnalysisStore((state) => state.photoConsentAccepted);
  const setPhotoConsentAccepted = useAnalysisStore((state) => state.setPhotoConsentAccepted);
  const setCapturedImage = useAnalysisStore((state) => state.setCapturedImage);
  const [ready, setReady] = useState(false);
  const [currentAngle, setCurrentAngle] = useState<CaptureAngle>("front");
  const [checking, setChecking] = useState(false);
  const currentCapture = capturedImages[currentAngle];
  const allPassed = angles.every(
    (angle) => (capturedImages[angle]?.confidence ?? 0) >= REQUIRED_CONFIDENCE,
  );

  const nextAngle = useMemo(() => {
    return angles.find((angle) => (capturedImages[angle]?.confidence ?? 0) < REQUIRED_CONFIDENCE);
  }, [capturedImages]);

  async function capture() {
    const photo = await cameraRef.current?.takePictureAsync({ quality: 1 });
    if (!photo?.uri) {
      return;
    }

    setChecking(true);
    const probeImage = {
      uri: photo.uri,
      name: `${currentAngle}-selfie.jpg`,
      type: "image/jpeg",
      angle: currentAngle,
      confidence: 0,
    };
    const cvScores = await analyzeImageLocally(probeImage).catch(() => null);
    const confidence = await estimateImageConfidence(photo.uri, cvScores);
    setCapturedImage(currentAngle, { ...probeImage, confidence });
    setChecking(false);
  }

  function continueFlow() {
    if (allPassed) {
      router.push("/(app)/questionnaire");
      return;
    }
    if (nextAngle) {
      setCurrentAngle(nextAngle);
    }
  }

  if (!permission?.granted) {
    return (
      <Screen>
        <Header title="Camera access" subtitle="Three clear angles are required for analysis." />
        <Card>
          <AppText muted>
            Capture a front selfie plus left and right side profiles. Each image must reach at least
            80 confidence before analysis can continue.
          </AppText>
          <Button label="Allow camera" icon="camera-outline" onPress={requestPermission} />
        </Card>
      </Screen>
    );
  }

  return (
    <Screen scroll={false}>
      <Header
        title={captureRequirements[currentAngle].title}
        subtitle={captureRequirements[currentAngle].instruction}
      />
      {!photoConsentAccepted ? (
        <Card>
          <AppText variant="subtitle">Private photo analysis</AppText>
          <AppText muted>
            Your face photos are uploaded only to analyze cosmetic skin signals, save progress,
            and generate an educational routine. This is not medical diagnosis.
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
      ) : null}
      <View style={styles.statusRow}>
        {angles.map((angle) => {
          const confidence = capturedImages[angle]?.confidence ?? 0;
          const passed = confidence >= REQUIRED_CONFIDENCE;
          return (
            <View key={angle} style={[styles.statusPill, passed && styles.statusPillPassed]}>
              <AppText variant="caption" style={passed && styles.statusTextPassed}>
                {angle} {confidence || "--"}
              </AppText>
            </View>
          );
        })}
      </View>
      <View style={styles.preview}>
        {currentCapture ? (
          <Image source={{ uri: currentCapture.uri }} style={StyleSheet.absoluteFill} />
        ) : (
          <CameraView
            ref={cameraRef}
            style={StyleSheet.absoluteFill}
            facing="front"
            onCameraReady={() => setReady(true)}
          />
        )}
        <View style={styles.frame} />
      </View>
      <Card>
        <AppText variant="subtitle">
          Confidence: {currentCapture ? `${currentCapture.confidence}/100` : "not captured"}
        </AppText>
        <AppText muted>{qualityMessage(currentCapture?.confidence ?? 0)}</AppText>
        {captureTips.map((tip) => (
          <AppText key={tip} variant="caption" muted>
            - {tip}
          </AppText>
        ))}
      </Card>
      <View style={styles.actions}>
        {currentCapture ? (
          <Button
            label="Retake this angle"
            icon="refresh-outline"
            variant="secondary"
            onPress={() => setCapturedImage(currentAngle, null)}
          />
        ) : (
          <Button
            label={checking ? "Checking quality..." : "Capture and check"}
            icon="radio-button-on-outline"
            onPress={capture}
            disabled={!ready || checking || !photoConsentAccepted}
          />
        )}
        <Button
          label={allPassed ? "Continue" : nextAngle ? `Next: ${nextAngle}` : "Continue"}
          icon="arrow-forward-outline"
          disabled={!allPassed && !nextAngle}
          onPress={continueFlow}
        />
        <Button
          label="Upload instead"
          variant="ghost"
          icon="image-outline"
          onPress={() => router.push("/(app)/upload")}
        />
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  statusRow: {
    flexDirection: "row",
    gap: spacing.sm,
  },
  statusPill: {
    flex: 1,
    borderWidth: 1,
    borderColor: colors.subtle,
    borderRadius: radii.sm,
    paddingVertical: spacing.xs,
    alignItems: "center",
    backgroundColor: colors.surface,
  },
  statusPillPassed: {
    backgroundColor: colors.mint,
    borderColor: colors.sage,
  },
  statusTextPassed: {
    color: colors.ink,
  },
  preview: {
    flex: 1,
    minHeight: 300,
    borderRadius: radii.lg,
    overflow: "hidden",
    backgroundColor: colors.ink,
  },
  frame: {
    position: "absolute",
    left: "12%",
    right: "12%",
    top: "12%",
    bottom: "12%",
    borderRadius: 180,
    borderWidth: 2,
    borderColor: colors.surface,
    opacity: 0.75,
  },
  actions: {
    gap: spacing.sm,
    paddingBottom: spacing.md,
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
