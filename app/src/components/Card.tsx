import { PropsWithChildren } from "react";
import { StyleSheet, View, ViewProps } from "react-native";

import { colors, radii, spacing } from "@/constants/theme";

export function Card({ children, style, ...props }: PropsWithChildren<ViewProps>) {
  return (
    <View {...props} style={[styles.card, style]}>
      {children}
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.surface,
    borderRadius: radii.md,
    borderWidth: 1,
    borderColor: colors.subtle,
    padding: spacing.md,
    gap: spacing.sm,
    shadowColor: colors.ink,
    shadowOpacity: 0.05,
    shadowOffset: { width: 0, height: 8 },
    shadowRadius: 20,
    elevation: 2,
  },
});
