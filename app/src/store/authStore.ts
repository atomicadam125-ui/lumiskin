import * as SecureStore from "expo-secure-store";
import { create } from "zustand";

import type { User } from "@/types/api";

const TOKEN_KEY = "lumiskin.accessToken";

type AuthState = {
  accessToken: string | null;
  user: User | null;
  hydrated: boolean;
  hydrate: () => Promise<void>;
  signIn: (token: string, user?: User | null) => Promise<void>;
  setUser: (user: User | null) => void;
  signOut: () => Promise<void>;
};

export const useAuthStore = create<AuthState>((set) => ({
  accessToken: null,
  user: null,
  hydrated: false,
  hydrate: async () => {
    const token = await SecureStore.getItemAsync(TOKEN_KEY);
    set({ accessToken: token, hydrated: true });
  },
  signIn: async (token, user = null) => {
    await SecureStore.setItemAsync(TOKEN_KEY, token);
    set({ accessToken: token, user });
  },
  setUser: (user) => set({ user }),
  signOut: async () => {
    await SecureStore.deleteItemAsync(TOKEN_KEY);
    set({ accessToken: null, user: null });
  },
}));
