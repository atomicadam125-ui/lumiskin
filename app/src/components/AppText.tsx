import { PropsWithChildren } from "react";
import { StyleSheet, Text, TextProps } from "react-native";

import { colors } from "@/constants/theme";

type AppTextProps = PropsWithChildren<
  TextProps & {
    variant?: "hero" | "title" | "subtitle" | "body" | "caption";
    muted?: boolean;
  }
>;

export function AppText({ children, style, variant = "body", muted, ...props }: AppTextProps) {
  return (
    <Text
      {...props}
      style={[styles.base, styles[variant], muted && styles.muted, style]}
    >
      {children}
    </Text>
  );
}

const styles = StyleSheet.create({
  base: {
    color: colors.ink,
  },
  hero: {
    fontSize: 34,
    lineHeight: 40,
    fontWeight: "800",
  },
  title: {
    fontSize: 24,
    lineHeight: 31,
    fontWeight: "700",
  },
  subtitle: {
    fontSize: 18,
    lineHeight: 24,
    fontWeight: "700",
  },
  body: {
    fontSize: 15,
    lineHeight: 22,
    fontWeight: "500",
  },
  caption: {
    fontSize: 12,
    lineHeight: 17,
    fontWeight: "600",
  },
  muted: {
    color: colors.muted,
  },
});
