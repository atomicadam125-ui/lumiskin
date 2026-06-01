import * as AppleAuthentication from "expo-apple-authentication";
import { Platform, StyleSheet } from "react-native";

import { useAppleLogin } from "@/hooks/useAuth";

export function AppleSignInButton() {
  const appleLogin = useAppleLogin();

  if (Platform.OS !== "ios") {
    return null;
  }

  async function signIn() {
    const available = await AppleAuthentication.isAvailableAsync();
    if (!available) {
      return;
    }

    const credential = await AppleAuthentication.signInAsync({
      requestedScopes: [
        AppleAuthentication.AppleAuthenticationScope.FULL_NAME,
        AppleAuthentication.AppleAuthenticationScope.EMAIL,
      ],
    });

    if (!credential.identityToken) {
      return;
    }

    const fullName = [credential.fullName?.givenName, credential.fullName?.familyName]
      .filter(Boolean)
      .join(" ");

    appleLogin.mutate({
      identity_token: credential.identityToken,
      full_name: fullName || undefined,
    });
  }

  return (
    <AppleAuthentication.AppleAuthenticationButton
      buttonType={AppleAuthentication.AppleAuthenticationButtonType.SIGN_IN}
      buttonStyle={AppleAuthentication.AppleAuthenticationButtonStyle.BLACK}
      cornerRadius={8}
      style={styles.button}
      onPress={signIn}
    />
  );
}

const styles = StyleSheet.create({
  button: {
    height: 52,
    width: "100%",
  },
});
