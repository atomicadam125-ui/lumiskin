import { Ionicons } from "@expo/vector-icons";
import { Pressable, StyleSheet, ViewStyle } from "react-native";

import { AppText } from "@/components/AppText";
import { colors, radii, spacing } from "@/constants/theme";

type ButtonProps = {
  label: string;
  onPress: () => void;
  icon?: keyof typeof Ionicons.glyphMap;
  variant?: "primary" | "secondary" | "ghost";
  disabled?: boolean;
  style?: ViewStyle;
};

export function Button({
  label,
  onPress,
  icon,
  variant = "primary",
  disabled,
  style,
}: ButtonProps) {
  return (
    <Pressable
      accessibilityRole="button"
      disabled={disabled}
      onPress={onPress}
      style={({ pressed }) => [
        styles.button,
        styles[variant],
        disabled && styles.disabled,
        pressed && !disabled && styles.pressed,
        style,
      ]}
    >
      {icon ? (
        <Ionicons
          name={icon}
          size={18}
          color={variant === "primary" ? colors.surface : colors.ink}
        />
      ) : null}
      <AppText
        variant="body"
        style={[styles.label, variant === "primary" && styles.primaryLabel]}
      >
        {label}
      </AppText>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  button: {
    minHeight: 52,
    borderRadius: radii.sm,
    paddingHorizontal: spacing.md,
    alignItems: "center",
    justifyContent: "center",
    flexDirection: "row",
    gap: spacing.sm,
  },
  primary: {
    backgroundColor: colors.ink,
  },
  secondary: {
    backgroundColor: colors.mint,
  },
  ghost: {
    backgroundColor: "transparent",
    borderWidth: 1,
    borderColor: colors.subtle,
  },
  disabled: {
    opacity: 0.5,
  },
  pressed: {
    transform: [{ scale: 0.985 }],
  },
  label: {
    fontWeight: "800",
  },
  primaryLabel: {
    color: colors.surface,
  },
});
