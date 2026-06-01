import { Ionicons } from "@expo/vector-icons";
import { Linking, Pressable, StyleSheet, View } from "react-native";

import { AppText } from "@/components/AppText";
import { colors, radii, spacing } from "@/constants/theme";
import type { RecommendedProduct } from "@/types/api";

export function ProductCard({ product }: { product: RecommendedProduct }) {
  return (
    <Pressable
      accessibilityRole="link"
      onPress={() => void Linking.openURL(product.url)}
      style={({ pressed }) => [styles.card, pressed && styles.pressed]}
    >
      <View style={styles.icon}>
        <Ionicons name="leaf-outline" size={20} color={colors.ink} />
      </View>
      <View style={styles.copy}>
        <AppText variant="caption" muted>
          {product.step} / {product.category}
        </AppText>
        <AppText variant="subtitle">
          {product.brand} {product.product_name}
        </AppText>
        <AppText muted>{product.why_chosen}</AppText>
        <AppText variant="caption">{product.how_often}</AppText>
        {product.caution ? (
          <AppText variant="caption" muted>
            {product.caution}
          </AppText>
        ) : null}
      </View>
      <Ionicons name="open-outline" size={18} color={colors.muted} />
    </Pressable>
  );
}

const styles = StyleSheet.create({
  card: {
    flexDirection: "row",
    gap: spacing.md,
    borderWidth: 1,
    borderColor: colors.subtle,
    borderRadius: radii.md,
    padding: spacing.md,
    backgroundColor: colors.surface,
  },
  pressed: {
    opacity: 0.75,
  },
  icon: {
    width: 38,
    height: 38,
    borderRadius: radii.sm,
    backgroundColor: colors.mint,
    alignItems: "center",
    justifyContent: "center",
  },
  copy: {
    flex: 1,
    gap: 4,
  },
});
