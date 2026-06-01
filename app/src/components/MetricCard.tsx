import { StyleSheet, View } from "react-native";

import { AppText } from "@/components/AppText";
import { colors, radii, spacing } from "@/constants/theme";

type MetricCardProps = {
  label: string;
  value: number;
  tone?: "sage" | "coral" | "amber" | "blue";
};

export function MetricCard({ label, value, tone = "sage" }: MetricCardProps) {
  const color = colors[tone];
  return (
    <View style={styles.card}>
      <View style={[styles.bar, { backgroundColor: color, width: `${Math.max(value, 6)}%` }]} />
      <AppText variant="caption" muted>
        {label}
      </AppText>
      <AppText variant="title">{value}</AppText>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    width: "48%",
    minHeight: 108,
    backgroundColor: colors.surface,
    borderRadius: radii.md,
    borderWidth: 1,
    borderColor: colors.subtle,
    padding: spacing.md,
    overflow: "hidden",
    gap: spacing.xs,
  },
  bar: {
    position: "absolute",
    left: 0,
    bottom: 0,
    height: 5,
  },
});
