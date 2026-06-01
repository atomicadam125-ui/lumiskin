import { LinearGradient } from "expo-linear-gradient";
import { router } from "expo-router";
import { useEffect } from "react";
import { ActivityIndicator, StyleSheet, View } from "react-native";

import { AppText } from "@/components/AppText";
import { colors, spacing } from "@/constants/theme";
import { useSessionBootstrap } from "@/hooks/useAuth";
import { useAuthStore } from "@/store/authStore";

export default function SplashScreen() {
  const hydrated = useAuthStore((state) => state.hydrated);
  const accessToken = useAuthStore((state) => state.accessToken);
  const session = useSessionBootstrap();

  useEffect(() => {
    if (!hydrated) {
      return;
    }
    if (!accessToken) {
      router.replace("/(auth)/login");
      return;
    }
    if (!session.isLoading) {
      router.replace(session.isError ? "/(auth)/login" : "/(app)/camera");
    }
  }, [accessToken, hydrated, session.isError, session.isLoading]);

  return (
    <LinearGradient colors={[colors.canvas, colors.mint]} style={styles.root}>
      <View style={styles.mark}>
        <AppText variant="hero">LumiSkin</AppText>
        <AppText muted>AI skincare analysis</AppText>
      </View>
      <ActivityIndicator color={colors.ink} />
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  root: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    gap: spacing.xl,
  },
  mark: {
    alignItems: "center",
    gap: spacing.xs,
  },
});
