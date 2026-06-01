import { useEffect } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { router } from "expo-router";

import * as AuthApi from "@/api/auth";
import { useAuthStore } from "@/store/authStore";

export function useSessionBootstrap() {
  const accessToken = useAuthStore((state) => state.accessToken);
  const setUser = useAuthStore((state) => state.setUser);

  const query = useQuery({
    queryKey: ["me", accessToken],
    queryFn: AuthApi.getMe,
    enabled: Boolean(accessToken),
    retry: false,
  });

  useEffect(() => {
    if (query.data) {
      setUser(query.data);
    }
  }, [query.data, setUser]);

  return query;
}

export function useLogin() {
  const queryClient = useQueryClient();
  const signIn = useAuthStore((state) => state.signIn);
  const setUser = useAuthStore((state) => state.setUser);

  return useMutation({
    mutationFn: AuthApi.login,
    onSuccess: async (tokens) => {
      await signIn(tokens.access_token);
      const user = await AuthApi.getMe();
      setUser(user);
      await queryClient.invalidateQueries({ queryKey: ["me"] });
      router.replace("/(app)/camera");
    },
  });
}

export function useAppleLogin() {
  const queryClient = useQueryClient();
  const signIn = useAuthStore((state) => state.signIn);
  const setUser = useAuthStore((state) => state.setUser);

  return useMutation({
    mutationFn: AuthApi.loginWithApple,
    onSuccess: async (tokens) => {
      await signIn(tokens.access_token);
      const user = await AuthApi.getMe();
      setUser(user);
      await queryClient.invalidateQueries({ queryKey: ["me"] });
      router.replace("/(app)/camera");
    },
  });
}

export function useRegister() {
  return useMutation({ mutationFn: AuthApi.register });
}

export function useLogout() {
  const queryClient = useQueryClient();
  const signOut = useAuthStore((state) => state.signOut);

  return async () => {
    await signOut();
    queryClient.clear();
    router.replace("/(auth)/login");
  };
}

export function useDeleteAccount() {
  const queryClient = useQueryClient();
  const signOut = useAuthStore((state) => state.signOut);

  return useMutation({
    mutationFn: AuthApi.deleteAccount,
    onSuccess: async () => {
      await signOut();
      queryClient.clear();
      router.replace("/(auth)/login");
    },
  });
}
