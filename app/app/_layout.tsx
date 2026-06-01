import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Stack } from "expo-router";
import { StatusBar } from "expo-status-bar";
import { useEffect, useState } from "react";

import { useAnalysisStore } from "@/store/analysisStore";
import { useAuthStore } from "@/store/authStore";

export default function RootLayout() {
  const [queryClient] = useState(() => new QueryClient());
  const hydrate = useAuthStore((state) => state.hydrate);
  const hydrateRoutineLog = useAnalysisStore((state) => state.hydrateRoutineLog);

  useEffect(() => {
    void hydrate();
    void hydrateRoutineLog();
  }, [hydrate, hydrateRoutineLog]);

  return (
    <QueryClientProvider client={queryClient}>
      <StatusBar style="dark" />
      <Stack screenOptions={{ headerShown: false }}>
        <Stack.Screen name="index" />
        <Stack.Screen name="(auth)" />
        <Stack.Screen name="(app)" />
      </Stack>
    </QueryClientProvider>
  );
}
