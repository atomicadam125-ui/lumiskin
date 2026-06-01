import { StyleSheet, TextInput, TextInputProps, View } from "react-native";

import { AppText } from "@/components/AppText";
import { colors, radii, spacing } from "@/constants/theme";

type TextFieldProps = TextInputProps & {
  label: string;
  error?: string;
};

export function TextField({ label, error, style, ...props }: TextFieldProps) {
  return (
    <View style={styles.wrap}>
      <AppText variant="caption" muted>
        {label}
      </AppText>
      <TextInput
        {...props}
        placeholderTextColor={colors.muted}
        style={[styles.input, error && styles.errorInput, style]}
      />
      {error ? (
        <AppText variant="caption" style={styles.error}>
          {error}
        </AppText>
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: {
    gap: spacing.xs,
  },
  input: {
    minHeight: 52,
    borderRadius: radii.sm,
    borderWidth: 1,
    borderColor: colors.subtle,
    backgroundColor: colors.surface,
    paddingHorizontal: spacing.md,
    fontSize: 15,
    color: colors.ink,
  },
  errorInput: {
    borderColor: colors.danger,
  },
  error: {
    color: colors.danger,
  },
});
