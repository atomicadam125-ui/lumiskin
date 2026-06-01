import { StyleSheet, View } from "react-native";

import { AppText } from "@/components/AppText";
import { colors, radii, spacing } from "@/constants/theme";
import type { RoutineStep as RoutineStepType } from "@/types/api";

export function RoutineStep({ step }: { step: RoutineStepType }) {
  return (
    <View style={styles.row}>
      <View style={styles.index}>
        <AppText variant="caption">{step.step}</AppText>
      </View>
      <View style={styles.copy}>
        <AppText variant="subtitle">{step.category}</AppText>
        {step.product_name ? (
          <AppText>
            {step.brand} {step.product_name}
          </AppText>
        ) : null}
        <AppText>{step.recommendation}</AppText>
        <AppText variant="caption" muted>
          {step.frequency}
        </AppText>
        {step.how_to_use ? (
          <AppText variant="caption" muted>
            How to use: {step.how_to_use}
          </AppText>
        ) : null}
        {step.caution ? (
          <AppText variant="caption" muted>
            Caution: {step.caution}
          </AppText>
        ) : null}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  row: {
    flexDirection: "row",
    gap: spacing.md,
    paddingVertical: spacing.sm,
  },
  index: {
    width: 30,
    height: 30,
    borderRadius: radii.sm,
    backgroundColor: colors.mint,
    alignItems: "center",
    justifyContent: "center",
  },
  copy: {
    flex: 1,
    gap: 3,
  },
});
