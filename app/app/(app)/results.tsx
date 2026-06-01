import { router } from "expo-router";
import { StyleSheet, View } from "react-native";

import { AppText } from "@/components/AppText";
import { Button } from "@/components/Button";
import { Card } from "@/components/Card";
import { Header } from "@/components/Header";
import { MetricCard } from "@/components/MetricCard";
import { ProductCard } from "@/components/ProductCard";
import { RoutineStep } from "@/components/RoutineStep";
import { Screen } from "@/components/Screen";
import { spacing } from "@/constants/theme";
import { useAnalysisStore } from "@/store/analysisStore";
import { analysisToRecommendationInput, metricEntries } from "@/utils/scores";

export default function ResultsDashboardScreen() {
  const analysis = useAnalysisStore((state) => state.latestAnalysis);
  const questionnaire = useAnalysisStore((state) => state.questionnaire);
  const goals = useAnalysisStore((state) => state.goals);
  const recommendation = useAnalysisStore((state) => state.latestRecommendation);

  if (!recommendation) {
    return (
      <Screen>
        <Header title="No results yet" subtitle="Run your first skin analysis to see a dashboard." />
        <Button label="Start scan" icon="camera-outline" onPress={() => router.push("/(app)/camera")} />
      </Screen>
    );
  }

  const scores = analysisToRecommendationInput(analysis, {
    age: 28,
    gender: "female",
    skin_type: questionnaire?.skin_type ?? "combination",
    goals,
  });

  return (
    <Screen>
      <Header title="Results dashboard" subtitle={recommendation.skin_summary} />
      <Card>
        <AppText variant="subtitle">Your 30-day focus</AppText>
        <AppText variant="hero">
          {recommendation.thirty_day_progress.current_score} to{" "}
          {recommendation.thirty_day_progress.estimated_day_30_score}
        </AppText>
        <AppText>
          +{recommendation.thirty_day_progress.estimated_score_increase} point AI-estimated goal:
          {` ${recommendation.thirty_day_progress.focus}`}
        </AppText>
        <AppText muted>
          Start with sunscreen every morning, keep the evening routine simple, and introduce retinol
          slowly on scheduled nights.
        </AppText>
        <Button
          label="Open today's routine"
          icon="checkmark-circle-outline"
          onPress={() => router.push("/(app)/progress")}
        />
      </Card>
      <Card>
        <AppText variant="subtitle">Skin Snapshot</AppText>
        <AppText variant="hero">
          {recommendation.skin_snapshot.score.overall_skin_score}
        </AppText>
        <AppText>{recommendation.skin_snapshot.score.current_tier}</AppText>
        <AppText muted>{recommendation.skin_snapshot.headline}</AppText>
      </Card>
      <View style={styles.metrics}>
        {metricEntries(scores).map((metric) => (
          <MetricCard key={metric.label} {...metric} />
        ))}
      </View>
      <Card>
        <AppText variant="subtitle">What We See</AppText>
        {recommendation.what_we_see.map((item) => (
          <View key={item.observation} style={styles.stack}>
            <AppText>{item.observation}</AppText>
            <AppText variant="caption" muted>
              {item.reasoning}
            </AppText>
          </View>
        ))}
      </Card>
      <Card>
        <AppText variant="subtitle">Biggest Improvement Opportunities</AppText>
        {recommendation.biggest_improvement_opportunities.map((item) => (
          <View key={item.concern} style={styles.stack}>
            <AppText>
              {item.priority}. {item.concern}
            </AppText>
            <AppText variant="caption" muted>
              {item.why_it_matters}
            </AppText>
          </View>
        ))}
      </Card>
      <Card>
        <AppText variant="subtitle">90-Day Plan</AppText>
        {recommendation.ninety_day_plan.map((phase) => (
          <View key={phase.phase} style={styles.stack}>
            <AppText>{phase.phase}: {phase.focus}</AppText>
            {phase.actions.map((action) => (
              <AppText key={action} variant="caption" muted>
                - {action}
              </AppText>
            ))}
          </View>
        ))}
      </Card>
      <Card>
        <AppText variant="subtitle">30-Day Progress Estimate</AppText>
        <AppText>
          {recommendation.thirty_day_progress.current_score} to{" "}
          {recommendation.thirty_day_progress.estimated_day_30_score} in 30 days
        </AppText>
        <AppText>
          Estimated improvement: +{recommendation.thirty_day_progress.estimated_score_increase} points
        </AppText>
        <AppText variant="caption" muted>
          Focus: {recommendation.thirty_day_progress.focus}
        </AppText>
        <AppText variant="caption" muted>
          {recommendation.thirty_day_progress.explanation}
        </AppText>
      </Card>
      <Card>
        <AppText variant="subtitle">Top concerns</AppText>
        {recommendation.top_concerns.map((concern) => (
          <AppText key={concern}>- {concern}</AppText>
        ))}
      </Card>
      <Card>
        <AppText variant="subtitle">Recommended Korean products</AppText>
        <AppText muted>
          Product links open the brand or retailer page. Patch test and introduce one product at a time.
        </AppText>
        {recommendation.recommended_products.map((product) => (
          <ProductCard key={`${product.brand}-${product.product_name}`} product={product} />
        ))}
      </Card>
      <Card>
        <AppText variant="subtitle">Morning routine</AppText>
        {recommendation.morning_routine.map((step) => (
          <RoutineStep key={`${step.step}-${step.category}`} step={step} />
        ))}
      </Card>
      <Card>
        <AppText variant="subtitle">Evening routine</AppText>
        {recommendation.evening_routine.map((step) => (
          <RoutineStep key={`${step.step}-${step.category}`} step={step} />
        ))}
      </Card>
      <Card>
        <AppText variant="subtitle">Consultation level</AppText>
        <AppText>{recommendation.dermatologist_consultation.level}</AppText>
        <AppText muted>{recommendation.dermatologist_consultation.rationale}</AppText>
      </Card>
      <Card>
        <AppText variant="subtitle">Expected Results</AppText>
        <AppText muted>{recommendation.expected_results.short_term}</AppText>
        <AppText muted>{recommendation.expected_results.medium_term}</AppText>
        <AppText muted>{recommendation.expected_results.long_term}</AppText>
        <AppText variant="caption">{recommendation.expected_results.realistic_outcome}</AppText>
      </Card>
      <Card>
        <AppText variant="subtitle">Improvement Potential</AppText>
        <AppText>
          Estimated range: {recommendation.improvement_potential.estimated_potential_score_range}
        </AppText>
        <AppText variant="caption" muted>
          {recommendation.improvement_potential.note}
        </AppText>
      </Card>
      <Card>
        <AppText variant="subtitle">Warnings</AppText>
        {recommendation.warnings.map((warning) => (
          <View key={warning.title} style={styles.stack}>
            <AppText>{warning.title}</AppText>
            <AppText variant="caption" muted>
              {warning.message}
            </AppText>
          </View>
        ))}
      </Card>
      <Card>
        <AppText variant="subtitle">AI Confidence</AppText>
        <AppText>{recommendation.ai_confidence.score}/100</AppText>
        <AppText muted>{recommendation.ai_confidence.explanation}</AppText>
      </Card>
      <Card>
        <AppText variant="caption" muted>
          {recommendation.medical_disclaimer}
        </AppText>
      </Card>
    </Screen>
  );
}

const styles = StyleSheet.create({
  metrics: {
    flexDirection: "row",
    flexWrap: "wrap",
    justifyContent: "space-between",
    rowGap: spacing.sm,
  },
  stack: {
    gap: spacing.xs,
  },
});
