import type { RoutineLog } from "@/store/analysisStore";

export function todayKey(date = new Date()) {
  return date.toISOString().slice(0, 10);
}

export function completionPercent(log?: RoutineLog) {
  if (!log) {
    return 0;
  }
  const values = [log.morning, log.sunscreen, log.evening, log.retinol];
  return Math.round((values.filter(Boolean).length / values.length) * 100);
}

export function completedDays(routineLog: Record<string, RoutineLog>) {
  return Object.values(routineLog).filter((log) => completionPercent(log) >= 75).length;
}

export function retinolNight(day = new Date().getDate()) {
  return day % 3 === 0 || day % 7 === 0;
}

export function coachMessage(percent: number) {
  if (percent >= 100) {
    return "Perfect routine day. Keep tomorrow gentle and consistent.";
  }
  if (percent >= 75) {
    return "Strong day. Sunscreen and evening consistency are doing the heavy lifting.";
  }
  if (percent >= 50) {
    return "Good start. Finish the evening routine to protect your 30-day trend.";
  }
  return "Start with sunscreen and moisturizer today. Small wins compound.";
}
