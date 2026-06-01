from schemas.recommendation_engine import (
    AIConfidence,
    AvoidIngredient,
    CategoryScores,
    DermatologistConsultation,
    ExpectedResults,
    ImprovementOpportunity,
    ImprovementPotential,
    IngredientRecommendation,
    NinetyDayPlan,
    ProductRecommendation,
    RecommendationEngineResponse,
    RecommendationInput,
    RecommendedProduct,
    RoutineStep,
    SkinScore,
    SkinSnapshot,
    ThirtyDayProgress,
    TimelinePhase,
    WarningItem,
    WhatWeSeeItem,
)
from services.product_catalog import K_BEAUTY_PRODUCTS, Product

DISCLAIMER = (
    "This is educational cosmetic skincare guidance only and is not a medical diagnosis, "
    "treatment plan, or substitute for care from a licensed clinician."
)


class SkincareRecommendationEngine:
    def generate(self, payload: RecommendationInput) -> RecommendationEngineResponse:
        concerns = self._rank_concerns(payload)
        consultation = self._consultation_level(payload)
        score = self._skin_score(payload)
        confidence = self._ai_confidence(payload)
        improvement_potential = self._improvement_potential(score.overall_skin_score)
        products = self._products(payload)
        return RecommendationEngineResponse(
            skin_snapshot=self._skin_snapshot(payload, concerns, score, confidence),
            scores=score,
            current_skin_tier=score.current_tier,
            what_we_see=self._what_we_see(payload),
            biggest_improvement_opportunities=self._opportunities(concerns),
            ninety_day_plan=self._ninety_day_plan(payload),
            expected_results=self._expected_results(payload),
            improvement_potential=improvement_potential,
            timeline=improvement_potential.estimated_timeline,
            thirty_day_progress=self._thirty_day_progress(score.overall_skin_score, concerns),
            ai_confidence=AIConfidence(
                score=confidence,
                explanation=(
                    "Confidence is based on the completeness of the score profile and the clarity "
                    "of cosmetic signals. It is not a medical certainty."
                ),
            ),
            recommended_products=self._recommended_products(products),
            warnings=self._warnings(payload, consultation),
            disclaimer=DISCLAIMER,
            skin_summary=self._summary(payload, concerns),
            top_concerns=[concern for concern, _ in concerns[:3]],
            morning_routine=self._morning_routine(payload, products),
            evening_routine=self._evening_routine(payload, products),
            product_recommendations=products,
            ingredient_recommendations=self._ingredients(payload),
            ingredients_to_avoid=self._avoid(payload),
            lifestyle_suggestions=self._lifestyle(payload),
            dermatologist_consultation=consultation,
            medical_disclaimer=DISCLAIMER,
        )

    def _skin_score(self, payload: RecommendationInput) -> SkinScore:
        category_scores = CategoryScores(
            acne_control=100 - payload.acne_score,
            oil_balance=100 - payload.oiliness_score,
            pigmentation_evenness=100 - payload.pigmentation_score,
            texture_smoothness=100 - max(payload.wrinkle_score, round(payload.acne_score * 0.35)),
            hydration_barrier=100 - max(payload.dryness_score, round(payload.redness_score * 0.45)),
        )
        overall = round(
            category_scores.acne_control * 0.24
            + category_scores.oil_balance * 0.18
            + category_scores.pigmentation_evenness * 0.18
            + category_scores.texture_smoothness * 0.18
            + category_scores.hydration_barrier * 0.22
        )
        return SkinScore(
            overall_skin_score=max(0, min(100, overall)),
            category_scores=category_scores,
            current_tier=self._tier(overall),
        )

    def _tier(self, score: int) -> str:
        if score >= 95:
            return "Exceptional"
        if score >= 90:
            return "Excellent"
        if score >= 80:
            return "Healthy"
        if score >= 70:
            return "Average"
        if score >= 60:
            return "Needs Improvement"
        return "Significant Concerns"

    def _skin_snapshot(
        self,
        payload: RecommendationInput,
        concerns: list[tuple[str, int]],
        score: SkinScore,
        confidence: int,
    ) -> SkinSnapshot:
        return SkinSnapshot(
            headline=(
                f"{payload.skin_type.title()} skin with the biggest visible opportunity in "
                f"{concerns[0][0]}."
            ),
            skin_type=payload.skin_type,
            score=score,
            confidence=confidence,
        )

    def _what_we_see(self, payload: RecommendationInput) -> list[WhatWeSeeItem]:
        observations = []
        if payload.acne_score >= 25:
            observations.append(
                WhatWeSeeItem(
                    observation="Some visible congestion or breakout tendency.",
                    reasoning="Acne score is elevated enough to prioritize gentle pore support.",
                )
            )
        if payload.oiliness_score >= 35:
            observations.append(
                WhatWeSeeItem(
                    observation="A moderate oil-balance signal.",
                    reasoning="Oiliness score suggests a lightweight, non-stripping routine.",
                )
            )
        if payload.pigmentation_score >= 25:
            observations.append(
                WhatWeSeeItem(
                    observation="Mild uneven tone or post-blemish mark potential.",
                    reasoning=(
                        "Pigmentation score supports daily sunscreen and brightening support."
                    ),
                )
            )
        if payload.redness_score < 30 and payload.dryness_score < 30:
            observations.append(
                WhatWeSeeItem(
                    observation="Barrier comfort appears relatively stable.",
                    reasoning=(
                        "Redness and dryness scores are low, so actives can be "
                        "introduced carefully."
                    ),
                )
            )
        return observations[:4]

    def _opportunities(
        self, concerns: list[tuple[str, int]]
    ) -> list[ImprovementOpportunity]:
        return [
            ImprovementOpportunity(
                concern=concern,
                priority=index + 1,
                why_it_matters=self._opportunity_reason(concern),
            )
            for index, (concern, _) in enumerate(concerns[:3])
        ]

    def _opportunity_reason(self, concern: str) -> str:
        reasons = {
            "acne and congestion": (
                "Improving congestion can help skin look clearer and reduce the look of new marks."
            ),
            "excess oiliness": "Better oil balance can make pores and shine look more refined.",
            "uneven tone and pigmentation": (
                "More consistent tone can make skin look brighter and more even."
            ),
            "redness and visible irritation": (
                "Calming visible irritation can make skin look healthier and more comfortable."
            ),
            "dryness and barrier support": (
                "A stronger-feeling barrier helps skin look smoother and tolerate actives better."
            ),
            "fine lines and texture": "Texture support can help skin look smoother over time.",
        }
        return reasons.get(concern, "This area has the largest room for visible improvement.")

    def _ninety_day_plan(self, payload: RecommendationInput) -> list[NinetyDayPlan]:
        return [
            NinetyDayPlan(
                phase="Weeks 1-4",
                focus="Reset and consistency",
                actions=[
                    "Use a gentle cleanser, lightweight moisturizer, and sunscreen daily.",
                    "Introduce niacinamide or a calming serum before stronger actives.",
                    "Avoid harsh scrubs and avoid adding multiple new products at once.",
                ],
            ),
            NinetyDayPlan(
                phase="Weeks 5-8",
                focus="Targeted cosmetic treatment",
                actions=[
                    self._phase_two_action(payload),
                    "Keep sunscreen consistent to support clearer, more even-looking skin.",
                    "Track progress with the same front, left, and right photo angles.",
                ],
            ),
            NinetyDayPlan(
                phase="Months 3-6",
                focus="Refine and maintain",
                actions=[
                    "Adjust active frequency based on comfort and visible progress.",
                    "Keep barrier-supporting moisturizer in the routine.",
                    "Consider dermatologist guidance if concerns persist or worsen.",
                ],
            ),
        ]

    def _phase_two_action(self, payload: RecommendationInput) -> str:
        if payload.acne_score >= 50 or payload.oiliness_score >= 55:
            return "Add salicylic acid 2-3 nights weekly if skin is comfortable."
        if payload.pigmentation_score >= 35 or self._has_goal(payload, "brighten skin"):
            return "Use a brightening serum consistently while keeping sunscreen daily."
        return "Add one targeted serum based on the concern you most want to improve."

    def _expected_results(self, payload: RecommendationInput) -> ExpectedResults:
        return ExpectedResults(
            short_term=(
                "In 2-4 weeks, skin may feel more balanced and less tight or shiny with a "
                "consistent routine."
            ),
            medium_term=(
                "In 6-8 weeks, breakouts and post-blemish marks may look calmer if the routine "
                "is tolerated."
            ),
            long_term=(
                "In 3-6 months, the goal is clearer, smoother, more even-looking skin, not "
                "a guarantee of perfection."
            ),
            realistic_outcome=(
                "Results vary by genetics, hormones, stress, sleep, product tolerance, and "
                "consistency."
            ),
        )

    def _improvement_potential(self, current_score: int) -> ImprovementPotential:
        thirty_day_lift = self._estimated_30_day_lift(current_score)
        low = min(100, max(current_score + 5, round(current_score + (100 - current_score) * 0.45)))
        high = min(100, max(low, round(current_score + (100 - current_score) * 0.65)))
        return ImprovementPotential(
            estimated_potential_score_range=f"{low}-{high}",
            estimated_30_day_score_increase=thirty_day_lift,
            estimated_day_30_score=min(100, current_score + thirty_day_lift),
            estimated_timeline=[
                TimelinePhase(
                    phase="2-4 weeks",
                    expected_changes=[
                        "Better routine consistency",
                        "More balanced feel",
                        "Less visible irritation from over-cleansing",
                    ],
                ),
                TimelinePhase(
                    phase="6-8 weeks",
                    expected_changes=[
                        "Clearer-looking skin if breakouts respond",
                        "Early improvement in post-blemish marks",
                        "More predictable oil balance",
                    ],
                ),
                TimelinePhase(
                    phase="3-6 months",
                    expected_changes=[
                        "Smoother-looking texture",
                        "More even-looking tone",
                        "Stronger-looking skin barrier with consistent care",
                    ],
                ),
            ],
            note="AI-estimated improvement timeline, not a medical guarantee.",
        )

    def _estimated_30_day_lift(self, current_score: int) -> int:
        if current_score < 60:
            return 6
        if current_score < 70:
            return 5
        if current_score < 80:
            return 4
        if current_score < 90:
            return 3
        return 1

    def _thirty_day_progress(
        self, current_score: int, concerns: list[tuple[str, int]]
    ) -> ThirtyDayProgress:
        lift = self._estimated_30_day_lift(current_score)
        primary_focus = concerns[0][0] if concerns else "routine consistency"
        return ThirtyDayProgress(
            current_score=current_score,
            estimated_score_increase=lift,
            estimated_day_30_score=min(100, current_score + lift),
            focus=primary_focus,
            explanation=(
                f"With daily sunscreen, consistent Korean skincare basics, and slow active "
                f"introduction, the first 30 days are estimated to improve the score by +{lift} "
                "points. This is an AI-estimated cosmetic progress target, not a medical "
                "guarantee."
            ),
        )

    def _ai_confidence(self, payload: RecommendationInput) -> int:
        spread = max(
            payload.acne_score,
            payload.redness_score,
            payload.pigmentation_score,
            payload.wrinkle_score,
            payload.oiliness_score,
            payload.dryness_score,
        ) - min(
            payload.acne_score,
            payload.redness_score,
            payload.pigmentation_score,
            payload.wrinkle_score,
            payload.oiliness_score,
            payload.dryness_score,
        )
        return max(65, min(92, 86 - round(spread * 0.12) + min(len(payload.goals), 3)))

    def _rank_concerns(self, payload: RecommendationInput) -> list[tuple[str, int]]:
        concern_scores = [
            ("acne and congestion", payload.acne_score),
            ("excess oiliness", payload.oiliness_score),
            ("uneven tone and pigmentation", payload.pigmentation_score),
            ("redness and visible irritation", payload.redness_score),
            ("dryness and barrier support", payload.dryness_score),
            ("fine lines and texture", payload.wrinkle_score),
        ]

        goal_boosts = {
            "reduce acne": "acne and congestion",
            "clear acne": "acne and congestion",
            "brighten skin": "uneven tone and pigmentation",
            "reduce redness": "redness and visible irritation",
            "control oil": "excess oiliness",
            "hydrate": "dryness and barrier support",
            "anti aging": "fine lines and texture",
            "reduce wrinkles": "fine lines and texture",
        }
        boosted = dict(concern_scores)
        normalized_goals = {goal.lower().strip() for goal in payload.goals}
        for goal, concern in goal_boosts.items():
            if goal in normalized_goals:
                boosted[concern] = min(100, boosted[concern] + 12)

        return sorted(boosted.items(), key=lambda item: item[1], reverse=True)

    def _summary(self, payload: RecommendationInput, concerns: list[tuple[str, int]]) -> str:
        primary = concerns[0][0]
        secondary = concerns[1][0]
        return (
            f"Your profile suggests {payload.skin_type} skin with the strongest cosmetic focus "
            f"on {primary}, followed by {secondary}. The routine below prioritizes gentle, "
            "barrier-respecting steps and gradual introduction of active ingredients."
        )

    def _morning_routine(
        self, payload: RecommendationInput, products: list[ProductRecommendation]
    ) -> list[RoutineStep]:
        cleanser = self._find_product(products, "cosrx_low_ph_cleanser")
        brightening = self._find_product(products, "axis_y_dark_spot_serum")
        balancing = self._find_product(products, "beauty_of_joseon_glow_serum")
        treatment = brightening or balancing
        moisturizer = self._find_first_product(
            products, ("dr_g_red_blemish_cream", "etude_soonjung_barrier_cream")
        )
        sunscreen = self._find_product(products, "boj_relief_sun")

        return [
            self._routine_step_from_product(
                step=1,
                product=cleanser,
                category="cleanser",
                recommendation=self._morning_cleanser(payload),
                frequency=(
                    "Every morning if oily; otherwise use water rinse and save cleanser for night"
                ),
                rationale="Keeps the routine fresh without stripping the skin barrier.",
                how_to_use="Massage a small amount on damp skin for 30-45 seconds, then rinse.",
            ),
            self._routine_step_from_product(
                step=2,
                product=treatment,
                category="treatment serum",
                recommendation=self._morning_treatment(payload),
                frequency="Every morning if tolerated",
                rationale=(
                    "Supports oil balance, post-blemish marks, and brighter-looking skin "
                    "without starting the day with a harsh active."
                ),
                how_to_use="Apply a thin layer after cleansing, before moisturizer.",
            ),
            self._routine_step_from_product(
                step=3,
                product=moisturizer,
                category="moisturizer",
                recommendation=self._moisturizer(payload),
                frequency="Every morning",
                rationale="Helps the skin barrier tolerate sunscreen and evening actives.",
                how_to_use="Apply a light, even layer over the face and neck.",
            ),
            self._routine_step_from_product(
                step=4,
                product=sunscreen,
                category="sunscreen",
                recommendation="Korean SPF50+ sunscreen as the final morning step.",
                frequency="Every morning; reapply every 2 hours with outdoor exposure",
                rationale=(
                    "Sunscreen is the highest-priority step for post-blemish marks, uneven tone, "
                    "texture prevention, and retinol routines."
                ),
                how_to_use=(
                    "Use two finger lengths for face and neck as the last step. Reapply after "
                    "sweating, swimming, or extended direct sun."
                ),
            ),
        ]

    def _evening_routine(
        self, payload: RecommendationInput, products: list[ProductRecommendation]
    ) -> list[RoutineStep]:
        oil_cleanser = self._find_product(products, "anua_heartleaf_cleansing_oil")
        gel_cleanser = self._find_product(products, "cosrx_low_ph_cleanser")
        retinol = self._find_first_product(products, ("innisfree_retinol_cica", "cosrx_retinol_01"))
        balancing = self._find_product(products, "beauty_of_joseon_glow_serum")
        moisturizer = self._find_first_product(
            products, ("dr_g_red_blemish_cream", "etude_soonjung_barrier_cream")
        )

        steps = []
        if oil_cleanser is not None:
            steps.append(
                self._routine_step_from_product(
                    step=1,
                    product=oil_cleanser,
                    category="first cleanse",
                    recommendation="Oil cleanse to remove sunscreen and makeup cleanly.",
                    frequency="Nightly when wearing sunscreen or makeup",
                    rationale="Removing sunscreen fully helps reduce the look of congestion.",
                    how_to_use=(
                        "Massage onto dry skin for 45-60 seconds, add water to emulsify, "
                        "then rinse before gel cleanser."
                    ),
                )
            )

        steps.append(
            self._routine_step_from_product(
                step=len(steps) + 1,
                product=gel_cleanser,
                category="cleanser",
                recommendation="Gentle second cleanse without a tight after-feel.",
                frequency="Nightly",
                rationale="Clears daily buildup while keeping the barrier comfortable.",
                how_to_use="Use on damp skin for 30-45 seconds, then rinse with lukewarm water.",
            )
        )

        if retinol is not None:
            steps.append(
                self._routine_step_from_product(
                    step=len(steps) + 1,
                    product=retinol,
                    category="beginner retinol",
                    recommendation=(
                        "Beginner Korean retinol for smoother-looking texture, clearer-looking "
                        "pores, and early fine-line prevention."
                    ),
                    frequency=(
                        "Weeks 1-2: 2 nights weekly. Weeks 3-4: 3 nights weekly if comfortable."
                    ),
                    rationale=(
                        "Over age 25, a slow retinol routine can support texture and visible "
                        "aging while staying beginner-friendly."
                    ),
                    how_to_use=(
                        "Apply a pea-sized amount on completely dry skin after cleansing. Follow "
                        "with moisturizer. Do not use on the same night as exfoliating acids."
                    ),
                )
            )
        elif balancing is not None:
            steps.append(
                self._routine_step_from_product(
                    step=len(steps) + 1,
                    product=balancing,
                    category="balancing serum",
                    recommendation="Gentle balancing serum on non-retinol nights.",
                    frequency="3-5 nights weekly",
                    rationale=(
                        "Supports oil balance and barrier comfort while actives stay gradual."
                    ),
                    how_to_use="Apply 1-2 pumps after cleansing and before moisturizer.",
                )
            )

        steps.append(
            self._routine_step_from_product(
                step=len(steps) + 1,
                product=moisturizer,
                category="moisturizer",
                recommendation=self._night_moisturizer(payload),
                frequency="Nightly, including retinol nights",
                rationale="Moisturizer reduces dryness risk and helps maintain consistency.",
                how_to_use=(
                    "Apply a generous layer after treatment. On retinol nights, add extra around "
                    "the nose, mouth, and under-eye orbital bone."
                ),
            )
        )
        return steps

    def _ingredients(self, payload: RecommendationInput) -> list[IngredientRecommendation]:
        ingredients = [
            IngredientRecommendation(
                ingredient="niacinamide",
                why="Helps with the look of oiliness, pores, uneven tone, and barrier support.",
                how_to_use="Use once daily in a serum or moisturizer, ideally at 2-5%.",
            )
        ]

        if payload.acne_score >= 50 or payload.oiliness_score >= 60:
            ingredients.append(
                IngredientRecommendation(
                    ingredient="salicylic acid",
                    why=(
                        "Oil-soluble exfoliant that can improve the look of clogged pores "
                        "and breakouts."
                    ),
                    how_to_use=(
                        "Use 2-4 nights weekly; reduce frequency if dryness or stinging appears."
                    ),
                )
            )
        if payload.pigmentation_score >= 35 or self._has_goal(payload, "brighten skin"):
            ingredients.append(
                IngredientRecommendation(
                    ingredient="vitamin C or azelaic acid",
                    why="Can support a brighter-looking, more even skin tone.",
                    how_to_use=(
                        "Use vitamin C in the morning or azelaic acid once daily if tolerated."
                    ),
                )
            )
        if payload.dryness_score >= 35 or payload.skin_type == "dry":
            ingredients.append(
                IngredientRecommendation(
                    ingredient="ceramides and glycerin",
                    why="Support hydration and the skin barrier.",
                    how_to_use="Use in moisturizer morning and evening.",
                )
            )
        if payload.wrinkle_score >= 35 or payload.age >= 25:
            ingredients.append(
                IngredientRecommendation(
                    ingredient="retinol or retinal",
                    why="Supports smoother-looking texture and fine lines over time.",
                    how_to_use=(
                        "Use at night 1-3 times weekly to start; avoid during pregnancy "
                        "unless cleared."
                    ),
                )
            )

        return ingredients[:5]

    def _products(self, payload: RecommendationInput) -> list[ProductRecommendation]:
        selected_keys = [
            "cosrx_low_ph_cleanser",
            "beauty_of_joseon_glow_serum",
            "dr_g_red_blemish_cream",
            "boj_relief_sun",
        ]

        if payload.acne_score >= 45 or payload.oiliness_score >= 55:
            selected_keys.insert(1, "anua_heartleaf_cleansing_oil")
        if payload.pigmentation_score >= 30 or self._has_goal(payload, "brighten skin"):
            selected_keys.insert(2, "axis_y_dark_spot_serum")
        if payload.redness_score >= 35 or payload.skin_type == "sensitive":
            selected_keys.insert(2, "skin1004_centella_ampoule")
        if payload.dryness_score >= 40 or payload.skin_type == "dry":
            selected_keys = [
                key if key != "dr_g_red_blemish_cream" else "etude_soonjung_barrier_cream"
                for key in selected_keys
            ]
        if payload.age >= 25 and payload.redness_score < 65 and payload.dryness_score < 65:
            retinol_key = (
                "cosrx_retinol_01"
                if payload.wrinkle_score >= 35
                else "innisfree_retinol_cica"
            )
            selected_keys.insert(-1, retinol_key)

        deduped = list(dict.fromkeys(selected_keys))
        return [self._product_response(K_BEAUTY_PRODUCTS[key], payload) for key in deduped[:8]]

    def _product_response(
        self, product: Product, payload: RecommendationInput
    ) -> ProductRecommendation:
        return ProductRecommendation(
            name=product.name,
            brand=product.brand,
            category=product.category,
            step=self._product_step(product),
            url=product.url,
            why=self._product_reason(product, payload),
            how_to_use=self._product_usage(product),
            caution=product.caution,
        )

    def _recommended_products(
        self, products: list[ProductRecommendation]
    ) -> list[RecommendedProduct]:
        return [
            RecommendedProduct(
                product_name=product.name,
                brand=product.brand,
                category=product.category,
                step=product.step,
                url=product.url,
                why_chosen=product.why,
                how_often=product.how_to_use,
                caution=product.caution,
            )
            for product in products
        ]

    def _product_step(self, product: Product) -> str:
        if "sunscreen" in product.category:
            return "Morning final step"
        if product.category in {"cleanser", "oil cleanser"}:
            return "Cleanse"
        if "serum" in product.category or "ampoule" in product.category:
            return "Treatment"
        return "Moisturize"

    def _product_reason(self, product: Product, payload: RecommendationInput) -> str:
        if product.key == "boj_relief_sun":
            return "Daily sunscreen is essential when working on tone, marks, texture, or glow."
        if product.key == "axis_y_dark_spot_serum":
            return "Fits the brightening goal and visible post-blemish or uneven tone concerns."
        if product.key == "beauty_of_joseon_glow_serum":
            return "Niacinamide-based option for oil balance, pores, and a healthier-looking glow."
        if product.key == "skin1004_centella_ampoule":
            return "Simple calming ampoule for visible redness, sensitivity, or barrier support."
        if product.key == "anua_heartleaf_cleansing_oil":
            return "Useful as a first cleanse when wearing sunscreen or makeup."
        if product.key == "innisfree_retinol_cica":
            return (
                "Beginner-friendly Korean retinol choice for users over 25 who want smoother, "
                "clearer-looking texture with a slow introduction."
            )
        if product.key == "cosrx_retinol_01":
            return (
                "Low-strength Korean retinol cream for early fine-line and texture support when "
                "introduced slowly."
            )
        if payload.oiliness_score >= 55:
            return "Lightweight K-beauty option that supports oil-prone or combination skin."
        return "Gentle K-beauty staple that fits this routine without being overly aggressive."

    def _product_usage(self, product: Product) -> str:
        usage = {
            "cosrx_low_ph_cleanser": (
                "Use once daily at night, or morning and night if skin feels oily."
            ),
            "anua_heartleaf_cleansing_oil": (
                "Massage onto dry skin at night, emulsify with water, then follow "
                "with gel cleanser."
            ),
            "skin1004_centella_ampoule": "Apply 2-4 drops after cleansing, morning or evening.",
            "axis_y_dark_spot_serum": "Apply a thin layer to uneven tone or marks once daily.",
            "beauty_of_joseon_glow_serum": "Use 1-2 pumps after cleansing, before moisturizer.",
            "dr_g_red_blemish_cream": "Use as moisturizer morning and evening.",
            "etude_soonjung_barrier_cream": (
                "Use as moisturizer, especially at night or on recovery days."
            ),
            "boj_relief_sun": "Apply generously every morning and reapply with outdoor exposure.",
            "innisfree_retinol_cica": (
                "Use at night 2 times weekly for 2 weeks, then 3 times weekly if comfortable."
            ),
            "cosrx_retinol_01": (
                "Use a pea-sized amount at night 1-2 times weekly, then increase slowly."
            ),
        }
        return usage[product.key]

    def _find_product(
        self, products: list[ProductRecommendation], key: str
    ) -> ProductRecommendation | None:
        for product in products:
            if K_BEAUTY_PRODUCTS[key].name == product.name:
                return product
        return None

    def _find_first_product(
        self, products: list[ProductRecommendation], keys: tuple[str, ...]
    ) -> ProductRecommendation | None:
        for key in keys:
            product = self._find_product(products, key)
            if product is not None:
                return product
        return None

    def _routine_step_from_product(
        self,
        *,
        step: int,
        product: ProductRecommendation | None,
        category: str,
        recommendation: str,
        frequency: str,
        rationale: str,
        how_to_use: str,
    ) -> RoutineStep:
        return RoutineStep(
            step=step,
            category=category,
            recommendation=(
                f"{product.brand} {product.name}: {recommendation}" if product else recommendation
            ),
            frequency=frequency,
            rationale=rationale,
            product_name=product.name if product else None,
            brand=product.brand if product else None,
            product_url=product.url if product else None,
            how_to_use=how_to_use,
            caution=product.caution if product else None,
        )

    def _avoid(self, payload: RecommendationInput) -> list[AvoidIngredient]:
        avoid = [
            AvoidIngredient(
                ingredient="harsh physical scrubs",
                reason="Can aggravate redness, dryness, and active breakouts.",
            ),
            AvoidIngredient(
                ingredient="high-fragrance leave-on products",
                reason=(
                    "May increase cosmetic irritation risk, especially when using active "
                    "ingredients."
                ),
            ),
        ]
        if payload.redness_score >= 45 or payload.skin_type == "sensitive":
            avoid.append(
                AvoidIngredient(
                    ingredient="stacking exfoliating acids and retinoids on the same night",
                    reason="This can make the skin look and feel irritated or over-exfoliated.",
                )
            )
        if payload.oiliness_score >= 60 or payload.acne_score >= 50:
            avoid.append(
                AvoidIngredient(
                    ingredient="very heavy occlusive products across acne-prone areas",
                    reason="May feel greasy and can worsen the look of congestion for some users.",
                )
            )
        return avoid

    def _warnings(
        self,
        payload: RecommendationInput,
        consultation: DermatologistConsultation,
    ) -> list[WarningItem]:
        warnings = [
            WarningItem(
                title="Educational cosmetic guidance",
                message=(
                    "This plan is not a diagnosis or prescription. Patch test and introduce "
                    "one new product at a time."
                ),
                severity="info",
            ),
            WarningItem(
                title="Sunscreen consistency",
                message=(
                    "Brightening and post-blemish mark routines work best with daily sunscreen."
                ),
                severity="info",
            ),
        ]
        if payload.redness_score >= 45 or payload.dryness_score >= 45:
            warnings.append(
                WarningItem(
                    title="Barrier caution",
                    message=(
                        "Avoid stacking exfoliants or retinoid-style products while skin looks "
                        "irritated or dry."
                    ),
                    severity="caution",
                )
            )
        if payload.age >= 25:
            warnings.append(
                WarningItem(
                    title="Retinol adjustment period",
                    message=(
                        "Mild dryness, flaking, or a temporary purge-like increase in visible "
                        "congestion can be normal when starting retinol. Go slowly, moisturize, "
                        "use sunscreen every morning, and stop or seek professional guidance if "
                        "irritation is severe, painful, swollen, or persistent."
                    ),
                    severity="caution",
                )
            )
        if consultation.level in {"consider", "recommended", "urgent"}:
            warnings.append(
                WarningItem(
                    title="Professional guidance",
                    message=consultation.rationale,
                    severity="important" if consultation.level == "recommended" else "caution",
                )
            )
        return warnings

    def _lifestyle(self, payload: RecommendationInput) -> list[str]:
        suggestions = [
            "Introduce one new active ingredient at a time and patch test when possible.",
            "Use sunscreen consistently, especially when targeting pigmentation or texture.",
            "Take progress photos every 4 weeks in similar lighting instead of judging day to day.",
        ]
        if payload.acne_score >= 60 or payload.oiliness_score >= 60:
            suggestions.append("Cleanse after heavy sweating and avoid picking at blemishes.")
        if payload.dryness_score >= 35 or payload.redness_score >= 45:
            suggestions.append(
                "Keep the routine simple during irritation: cleanser, moisturizer, sunscreen."
            )
        return suggestions

    def _consultation_level(self, payload: RecommendationInput) -> DermatologistConsultation:
        if payload.acne_score >= 85 or payload.redness_score >= 85:
            return DermatologistConsultation(
                level="recommended",
                rationale=(
                    "Scores are high enough that professional guidance may be useful, especially "
                    "if symptoms are painful, sudden, persistent, or worsening."
                ),
            )
        if (
            payload.acne_score >= 65
            or payload.pigmentation_score >= 70
            or payload.redness_score >= 65
        ):
            return DermatologistConsultation(
                level="consider",
                rationale=(
                    "A dermatologist can help personalize options if over-the-counter cosmetic "
                    "routines are not enough after consistent use."
                ),
            )
        return DermatologistConsultation(
            level="routine",
            rationale="No urgent cosmetic signal is detected from the provided scores.",
        )

    def _morning_cleanser(self, payload: RecommendationInput) -> str:
        if payload.oiliness_score >= 60:
            return "Gentle gel cleanser focused on oil control without a tight after-feel."
        if payload.dryness_score >= 45 or payload.skin_type == "dry":
            return "Hydrating cream cleanser or a water rinse if skin feels dry in the morning."
        return "Gentle low-foam cleanser."

    def _morning_treatment(self, payload: RecommendationInput) -> str:
        if payload.pigmentation_score >= 35 or self._has_goal(payload, "brighten skin"):
            return "Antioxidant serum such as vitamin C, or niacinamide if vitamin C is irritating."
        if payload.redness_score >= 45:
            return "Calming serum with niacinamide, panthenol, centella, or green tea."
        return "Lightweight niacinamide serum."

    def _moisturizer(self, payload: RecommendationInput) -> str:
        if payload.oiliness_score >= 60 and payload.dryness_score < 40:
            return "Lightweight non-comedogenic gel-cream moisturizer."
        return "Barrier-supporting moisturizer with humectants and ceramides."

    def _night_moisturizer(self, payload: RecommendationInput) -> str:
        if payload.dryness_score >= 40 or payload.redness_score >= 45:
            return "Richer barrier cream with ceramides, glycerin, or panthenol."
        return self._moisturizer(payload)

    def _has_goal(self, payload: RecommendationInput, goal: str) -> bool:
        return goal in {item.lower().strip() for item in payload.goals}
