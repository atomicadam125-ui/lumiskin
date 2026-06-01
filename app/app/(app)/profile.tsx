import { Ionicons } from "@expo/vector-icons";
import { Alert, Linking, StyleSheet, View } from "react-native";

import { AppText } from "@/components/AppText";
import { Button } from "@/components/Button";
import { Card } from "@/components/Card";
import { Header } from "@/components/Header";
import { Screen } from "@/components/Screen";
import { colors, radii, spacing } from "@/constants/theme";
import { appConfig } from "@/constants/config";
import { useDeleteAccount, useLogout } from "@/hooks/useAuth";
import { useAuthStore } from "@/store/authStore";

export default function ProfileSettingsScreen() {
  const user = useAuthStore((state) => state.user);
  const logout = useLogout();
  const deleteAccount = useDeleteAccount();

  function confirmDeleteAccount() {
    Alert.alert(
      "Delete account",
      "This will deactivate your account and remove access to your saved skincare history.",
      [
        { text: "Cancel", style: "cancel" },
        {
          text: "Delete",
          style: "destructive",
          onPress: () => deleteAccount.mutate(),
        },
      ],
    );
  }

  return (
    <Screen>
      <Header title="Profile settings" subtitle="Manage your account and analysis preferences." />
      <Card>
        <View style={styles.avatar}>
          <Ionicons name="person-outline" size={28} color={colors.ink} />
        </View>
        <AppText variant="subtitle">{user?.full_name ?? "Skincare member"}</AppText>
        <AppText muted>{user?.email ?? "Signed in securely"}</AppText>
      </Card>
      <Card>
        <AppText variant="subtitle">Privacy controls</AppText>
        <SettingRow label="Private S3 image storage" value="Enabled" />
        <SettingRow label="JWT session protection" value="Enabled" />
        <SettingRow label="Medical disclaimer" value="Always shown" />
        {appConfig.privacyPolicyUrl ? (
          <Button
            label="Privacy policy"
            icon="document-text-outline"
            variant="secondary"
            onPress={() => void Linking.openURL(appConfig.privacyPolicyUrl!)}
          />
        ) : null}
      </Card>
      <Card>
        <AppText variant="subtitle">Preferences</AppText>
        <SettingRow label="Routine style" value="Gentle" />
        <SettingRow label="Progress cadence" value="Monthly" />
        <SettingRow label="Recommendation mode" value="Educational" />
      </Card>
      <Button label="Sign out" icon="log-out-outline" variant="ghost" onPress={logout} />
      <Button
        label={deleteAccount.isPending ? "Deleting..." : "Delete account"}
        icon="trash-outline"
        variant="ghost"
        disabled={deleteAccount.isPending}
        onPress={confirmDeleteAccount}
      />
    </Screen>
  );
}

function SettingRow({ label, value }: { label: string; value: string }) {
  return (
    <View style={styles.row}>
      <AppText>{label}</AppText>
      <AppText muted>{value}</AppText>
    </View>
  );
}

const styles = StyleSheet.create({
  avatar: {
    width: 58,
    height: 58,
    borderRadius: radii.lg,
    backgroundColor: colors.mint,
    alignItems: "center",
    justifyContent: "center",
  },
  row: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    gap: spacing.md,
    paddingVertical: spacing.sm,
  },
});
