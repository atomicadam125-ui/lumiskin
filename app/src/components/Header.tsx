import { StyleSheet, View } from "react-native";

import { AppText } from "@/components/AppText";
import { spacing } from "@/constants/theme";

type HeaderProps = {
  title: string;
  subtitle?: string;
};

export function Header({ title, subtitle }: HeaderProps) {
  return (
    <View style={styles.wrap}>
      <AppText variant="title">{title}</AppText>
      {subtitle ? (
        <AppText muted>
          {subtitle}
        </AppText>
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: {
    gap: spacing.xs,
    marginBottom: spacing.sm,
  },
});
