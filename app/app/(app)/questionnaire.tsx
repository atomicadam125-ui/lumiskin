import { router } from "expo-router";
import { useState } from "react";
import { Pressable, StyleSheet, View } from "react-native";

import { AppText } from "@/components/AppText";
import { Button } from "@/components/Button";
import { Card } from "@/components/Card";
import { Header } from "@/components/Header";
import { Screen } from "@/components/Screen";
import { colors, radii, spacing } from "@/constants/theme";
import { useAnalysisStore } from "@/store/analysisStore";
import type { QuestionnaireInput } from "@/types/api";

const skinTypes: QuestionnaireInput["skin_type"][] = [
  "combination",
  "oily",
  "dry",
  "normal",
  "sensitive",
];
const acneOptions: QuestionnaireInput["acne_frequency"][] = [
  "sometimes",
  "rarely",
  "often",
  "persistent",
];
const goals = ["reduce acne", "brighten skin", "calm redness", "smooth texture"];

export default function QuestionnaireScreen() {
  const capturedImages = useAnalysisStore((state) => state.capturedImages);
  const setQuestionnaire = useAnalysisStore((state) => state.setQuestionnaire);
  const setGoals = useAnalysisStore((state) => state.setGoals);
  const [skinType, setSkinType] = useState<QuestionnaireInput["skin_type"]>("combination");
  const [acneFrequency, setAcneFrequency] =
    useState<QuestionnaireInput["acne_frequency"]>("sometimes");
  const [selectedGoals, setSelectedGoals] = useState<string[]>(["reduce acne", "brighten skin"]);
  const [sensitivity, setSensitivity] = useState(3);
  const [sun, setSun] = useState(3);
  const [sleep, setSleep] = useState(3);
  const [stress, setStress] = useState(3);
  const hasRequiredPhotos = (["front", "left", "right"] as const).every(
    (angle) => (capturedImages[angle]?.confidence ?? 0) >= 80,
  );

  function submit() {
    setGoals(selectedGoals);
    setQuestionnaire({
      skin_type: skinType,
      acne_frequency: acneFrequency,
      sensitivity_level: sensitivity,
      sun_exposure_level: sun,
      sleep_quality: sleep,
      stress_level: stress,
      current_products: [],
      allergies: [],
    });
    router.push("/(app)/loading");
  }

  return (
    <Screen>
      <Header title="Skin questionnaire" subtitle="A little context improves your routine." />
      {!hasRequiredPhotos ? (
        <Card>
          <AppText muted>
            Capture or upload front, left profile, and right profile photos with 80+ confidence
            before starting analysis.
          </AppText>
          <Button
            label="Go to camera"
            icon="camera-outline"
            onPress={() => router.push("/(app)/camera")}
          />
        </Card>
      ) : null}
      <Card>
        <AppText variant="subtitle">Skin type</AppText>
        <OptionGrid values={skinTypes} selected={[skinType]} onToggle={(value) => setSkinType(value)} />
      </Card>
      <Card>
        <AppText variant="subtitle">Primary goals</AppText>
        <OptionGrid
          values={goals}
          selected={selectedGoals}
          onToggle={(value) =>
            setSelectedGoals((current) =>
              current.includes(value)
                ? current.filter((item) => item !== value)
                : [...current, value],
            )
          }
        />
      </Card>
      <Card>
        <AppText variant="subtitle">Breakout frequency</AppText>
        <OptionGrid
          values={acneOptions}
          selected={[acneFrequency]}
          onToggle={(value) => setAcneFrequency(value)}
        />
      </Card>
      <Card>
        <Scale label="Sensitivity" value={sensitivity} onChange={setSensitivity} />
        <Scale label="Sun exposure" value={sun} onChange={setSun} />
        <Scale label="Sleep quality" value={sleep} onChange={setSleep} />
        <Scale label="Stress level" value={stress} onChange={setStress} />
      </Card>
      <Button
        label="Start analysis"
        icon="sparkles-outline"
        disabled={!hasRequiredPhotos}
        onPress={submit}
      />
    </Screen>
  );
}

function OptionGrid<T extends string>({
  values,
  selected,
  onToggle,
}: {
  values: T[];
  selected: string[];
  onToggle: (value: T) => void;
}) {
  return (
    <View style={styles.options}>
      {values.map((value) => {
        const active = selected.includes(value);
        return (
          <Pressable
            key={value}
            onPress={() => onToggle(value)}
            style={[styles.option, active && styles.optionActive]}
          >
            <AppText variant="caption" style={active && styles.optionTextActive}>
              {value}
            </AppText>
          </Pressable>
        );
      })}
    </View>
  );
}

function Scale({
  label,
  value,
  onChange,
}: {
  label: string;
  value: number;
  onChange: (value: number) => void;
}) {
  return (
    <View style={styles.scale}>
      <AppText variant="caption" muted>
        {label}
      </AppText>
      <View style={styles.dots}>
        {[1, 2, 3, 4, 5].map((item) => (
          <Pressable
            key={item}
            onPress={() => onChange(item)}
            style={[styles.dot, item <= value && styles.dotActive]}
          />
        ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  options: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: spacing.sm,
  },
  option: {
    borderRadius: radii.sm,
    borderWidth: 1,
    borderColor: colors.subtle,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    backgroundColor: colors.surface,
  },
  optionActive: {
    backgroundColor: colors.ink,
    borderColor: colors.ink,
  },
  optionTextActive: {
    color: colors.surface,
  },
  scale: {
    gap: spacing.xs,
  },
  dots: {
    flexDirection: "row",
    gap: spacing.sm,
  },
  dot: {
    flex: 1,
    height: 10,
    borderRadius: radii.sm,
    backgroundColor: colors.subtle,
  },
  dotActive: {
    backgroundColor: colors.sage,
  },
});
