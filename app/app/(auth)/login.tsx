import { router } from "expo-router";
import { Controller, useForm } from "react-hook-form";
import { Alert, StyleSheet, View } from "react-native";

import { AppText } from "@/components/AppText";
import { AppleSignInButton } from "@/components/AppleSignInButton";
import { Button } from "@/components/Button";
import { Card } from "@/components/Card";
import { Screen } from "@/components/Screen";
import { TextField } from "@/components/TextField";
import { spacing } from "@/constants/theme";
import { useLogin } from "@/hooks/useAuth";

type LoginForm = { email: string; password: string };

export default function LoginScreen() {
  const login = useLogin();
  const { control, handleSubmit } = useForm<LoginForm>({
    defaultValues: { email: "", password: "" },
  });

  const onSubmit = handleSubmit((values) => {
    login.mutate(values, {
      onError: () => Alert.alert("Unable to sign in", "Check your email and password."),
    });
  });

  return (
    <Screen>
      <View style={styles.hero}>
        <AppText variant="hero">Welcome back</AppText>
        <AppText muted>Continue your skin health progress with a fresh analysis.</AppText>
      </View>
      <Card>
        <Controller
          control={control}
          name="email"
          rules={{ required: "Email is required" }}
          render={({ field, fieldState }) => (
            <TextField
              label="Email"
              autoCapitalize="none"
              keyboardType="email-address"
              value={field.value}
              onChangeText={field.onChange}
              error={fieldState.error?.message}
            />
          )}
        />
        <Controller
          control={control}
          name="password"
          rules={{ required: "Password is required" }}
          render={({ field, fieldState }) => (
            <TextField
              label="Password"
              secureTextEntry
              value={field.value}
              onChangeText={field.onChange}
              error={fieldState.error?.message}
            />
          )}
        />
        <Button
          label={login.isPending ? "Signing in..." : "Sign in"}
          icon="log-in-outline"
          onPress={onSubmit}
          disabled={login.isPending}
        />
        <AppleSignInButton />
      </Card>
      <Button
        label="Create account"
        variant="ghost"
        onPress={() => router.push("/(auth)/register")}
      />
    </Screen>
  );
}

const styles = StyleSheet.create({
  hero: {
    marginTop: spacing.xl,
    gap: spacing.sm,
  },
});
