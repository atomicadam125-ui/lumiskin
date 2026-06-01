import { Pressable, StyleSheet, View } from "react-native";

import { AppText } from "@/components/AppText";
import { Button } from "@/components/Button";
import { Card } from "@/components/Card";
import { Header } from "@/components/Header";
import { MetricCard } from "@/components/MetricCard";
import { Screen } from "@/components/Screen";
import { colors, spacing } from "@/constants/theme";
import { useHistory } from "@/hooks/useSkincare";
import { useAnalysisStore } from "@/store/analysisStore";
import {
  coachMessage,
  completedDays,
  completionPercent,
  retinolNight,
  todayKey,
} from "@/utils/routineCoach";

export default function ProgressTrackingScreen() {
  const history = useHistory();
  const routineLog = useAnalysisStore((state) => state.routineLog);
  const toggleRoutineItem = useAnalysisStore((state) => state.toggleRoutineItem);
  const latest = history.data?.analyses?.[0];
  const previous = history.data?.analyses?.[1];
  const metrics = [
    { key: "acne", label: "Acne" },
    { key: "redness", label: "Redness" },
    { key: "oiliness", label: "Oiliness" },
    { key: "dryness", label: "Dryness" },
  ];
  const dateKey = todayKey();
  const today = routineLog[dateKey] ?? {
    morning: false,
    sunscreen: false,
    evening: false,
    retinol: false,
  };
  const percent = completionPercent(today);
  const dayCount = Math.min(30, Math.max(1, completedDays(routineLog) + 1));

  return (
    <Screen>
      <Header title="30-day skin coach" subtitle="Build the routine that improves your trend." />
      <Card>
        <AppText variant="subtitle">Day {dayCount} of 30</AppText>
        <AppText variant="hero">{percent}%</AppText>
        <AppText muted>{coachMessage(percent)}</AppText>
        <View style={styles.checklist}>
          <CheckItem
            label="AM routine"
            active={today.morning}
            onPress={() => toggleRoutineItem(dateKey, "morning")}
          />
          <CheckItem
            label="Sunscreen"
            active={today.sunscreen}
            onPress={() => toggleRoutineItem(dateKey, "sunscreen")}
          />
          <CheckItem
            label="PM routine"
            active={today.evening}
            onPress={() => toggleRoutineItem(dateKey, "evening")}
          />
          <CheckItem
            label={retinolNight() ? "Retinol night" : "Recovery night"}
            active={today.retinol}
            onPress={() => toggleRoutineItem(dateKey, "retinol")}
          />
        </View>
      </Card>
      <Card>
        <AppText variant="subtitle">Photo history</AppText>
        <AppText muted>
          {history.data?.photos.length ?? 0} uploaded selfies in your timeline.
        </AppText>
      </Card>
      <View style={styles.metrics}>
        {metrics.map((metric) => {
          const current = score(latest, metric.key);
          const last = score(previous, metric.key);
          const delta = current !== null && last !== null ? current - last : null;
          return (
            <MetricCard
              key={metric.key}
              label={`${metric.label}${delta !== null ? ` (${delta >= 0 ? "+" : ""}${delta})` : ""}`}
              value={current ?? 0}
              tone="sage"
            />
          );
        })}
      </View>
      <Card>
        <AppText variant="subtitle">Consistency note</AppText>
        <AppText muted>
          Weekly check-ins and monthly photos in similar lighting make trend changes easier to
          interpret without obsessing over day-to-day texture.
        </AppText>
      </Card>
      <Button
        label={history.isRefetching ? "Refreshing..." : "Refresh history"}
        icon="refresh-outline"
        variant="secondary"
        onPress={() => void history.refetch()}
      />
    </Screen>
  );
}

function CheckItem({
  label,
  active,
  onPress,
}: {
  label: string;
  active: boolean;
  onPress: () => void;
}) {
  return (
    <Pressable
      accessibilityRole="checkbox"
      accessibilityState={{ checked: active }}
      onPress={onPress}
      style={[styles.checkItem, active && styles.checkItemActive]}
    >
      <AppText style={active ? styles.checkItemText : undefined}>
        {active ? "Done: " : ""}
        {label}
      </AppText>
    </Pressable>
  );
}

function score(analysis: unknown, key: string) {
  const item = analysis as { scores?: Record<string, { score?: number }> } | undefined;
  const raw = item?.scores?.[key]?.score;
  if (typeof raw !== "number") {
    return null;
  }
  return Math.round(raw <= 1 ? raw * 100 : raw);
}

const styles = StyleSheet.create({
  metrics: {
    flexDirection: "row",
    flexWrap: "wrap",
    justifyContent: "space-between",
    rowGap: spacing.sm,
  },
  checklist: {
    gap: spacing.sm,
  },
  checkItem: {
    minHeight: 46,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: colors.subtle,
    paddingHorizontal: spacing.md,
    alignItems: "center",
    flexDirection: "row",
    backgroundColor: colors.surface,
  },
  checkItemActive: {
    backgroundColor: colors.ink,
    borderColor: colors.ink,
  },
  checkItemText: {
    color: colors.surface,
  },
});
