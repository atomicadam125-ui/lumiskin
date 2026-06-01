import { router } from "expo-router";
import { Controller, useForm } from "react-hook-form";
import { Alert, StyleSheet, View } from "react-native";

import { AppText } from "@/components/AppText";
import { Button } from "@/components/Button";
import { Card } from "@/components/Card";
import { Screen } from "@/components/Screen";
import { TextField } from "@/components/TextField";
import { spacing } from "@/constants/theme";
import { useRegister, useSkipLocalAuth } from "@/hooks/useAuth";

type RegisterForm = { full_name: string; email: string; password: string };

export default function RegisterScreen() {
  const register = useRegister();
  const skipLocalAuth = useSkipLocalAuth();
  const { control, handleSubmit } = useForm<RegisterForm>({
    defaultValues: { full_name: "", email: "", password: "" },
  });

  const onSubmit = handleSubmit((values) => {
    register.mutate(values, {
      onSuccess: () => router.replace("/(auth)/login"),
      onError: () => Alert.alert("Registration failed", "Please try another email."),
    });
  });

  return (
    <Screen>
      <View style={styles.hero}>
        <AppText variant="hero">Create your profile</AppText>
        <AppText muted>Personalized routines start with a secure account.</AppText>
      </View>
      <Card>
        <Controller
          control={control}
          name="full_name"
          render={({ field }) => (
            <TextField label="Name" value={field.value} onChangeText={field.onChange} />
          )}
        />
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
          rules={{ minLength: { value: 8, message: "Use at least 8 characters" } }}
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
          label={register.isPending ? "Creating..." : "Register"}
          icon="sparkles-outline"
          onPress={onSubmit}
          disabled={register.isPending}
        />
      </Card>
      {__DEV__ ? (
        <Button
          label="Skip login/signup"
          icon="play-forward-outline"
          variant="secondary"
          onPress={() => void skipLocalAuth()}
        />
      ) : null}
    </Screen>
  );
}

const styles = StyleSheet.create({
  hero: {
    marginTop: spacing.xl,
    gap: spacing.sm,
  },
});
