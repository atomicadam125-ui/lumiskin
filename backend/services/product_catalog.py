from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    key: str
    name: str
    brand: str
    category: str
    url: str
    best_for: tuple[str, ...]
    caution: str | None = None


K_BEAUTY_PRODUCTS = {
    "cosrx_low_ph_cleanser": Product(
        key="cosrx_low_ph_cleanser",
        name="Low pH Good Morning Gel Cleanser",
        brand="COSRX",
        category="cleanser",
        url="https://www.cosrx.com/products/low-ph-good-morning-gel-cleanser",
        best_for=("combination", "oily", "acne", "daily cleanse"),
        caution="Use once daily if your skin feels tight or dry.",
    ),
    "anua_heartleaf_cleansing_oil": Product(
        key="anua_heartleaf_cleansing_oil",
        name="Heartleaf Pore Control Cleansing Oil",
        brand="Anua",
        category="oil cleanser",
        url="https://anua.com/products/heartleaf-pore-control-cleansing-oil-200ml",
        best_for=("sunscreen removal", "makeup removal", "double cleanse", "pores"),
        caution="Skip if cleansing oils tend to trigger congestion for you.",
    ),
    "skin1004_centella_ampoule": Product(
        key="skin1004_centella_ampoule",
        name="Madagascar Centella Ampoule",
        brand="SKIN1004",
        category="soothing ampoule",
        url="https://www.skin1004.com/products/skin1004-madagascar-centella-ampoule",
        best_for=("redness", "barrier", "sensitivity", "calming"),
    ),
    "axis_y_dark_spot_serum": Product(
        key="axis_y_dark_spot_serum",
        name="Dark Spot Correcting Glow Serum",
        brand="AXIS-Y",
        category="brightening serum",
        url="https://www.axis-y.com/collections/best-seller/products/dark-spot-correcting-glow-serum",
        best_for=("post blemish marks", "pigmentation", "brightening", "uneven tone"),
    ),
    "beauty_of_joseon_glow_serum": Product(
        key="beauty_of_joseon_glow_serum",
        name="Glow Serum: Propolis + Niacinamide",
        brand="Beauty of Joseon",
        category="balancing serum",
        url="https://beautyofjoseon.com/products/glow-serum-propolis-niacinamide",
        best_for=("oiliness", "pores", "glow", "barrier"),
        caution="Avoid if you know you react to propolis or bee-derived ingredients.",
    ),
    "dr_g_red_blemish_cream": Product(
        key="dr_g_red_blemish_cream",
        name="R.E.D Blemish Clear Soothing Cream",
        brand="Dr.G",
        category="moisturizer",
        url="https://dr-g.com/products/dr-g-r-e-d-blemish-clear-soothing-cream",
        best_for=("combination", "redness", "lightweight moisture", "barrier"),
    ),
    "etude_soonjung_barrier_cream": Product(
        key="etude_soonjung_barrier_cream",
        name="SoonJung 2x Barrier Intensive Cream",
        brand="ETUDE",
        category="barrier cream",
        url="https://www.ulta.com/p/soonjung-2x-barrier-intensive-cream-pimprod2049666",
        best_for=("dryness", "barrier", "sensitivity", "night moisturizer"),
    ),
    "boj_relief_sun": Product(
        key="boj_relief_sun",
        name="Relief Sun: Rice + Probiotics SPF50+",
        brand="Beauty of Joseon",
        category="sunscreen",
        url="https://beautyofjoseon.com/products/relief-sun-rice-probiotics",
        best_for=("daily sunscreen", "pigmentation prevention", "glow"),
    ),
    "innisfree_retinol_cica": Product(
        key="innisfree_retinol_cica",
        name="Retinol Cica Moisture Recovery Serum",
        brand="innisfree",
        category="beginner retinol serum",
        url="https://us.innisfree.com/products/retinol-cica-moisture-recovery-serum",
        best_for=("beginner retinol", "texture", "post blemish marks", "age 25 plus"),
        caution=(
            "Start slowly. Mild dryness, flaking, or temporary purging can happen while skin "
            "adjusts."
        ),
    ),
    "cosrx_retinol_01": Product(
        key="cosrx_retinol_01",
        name="The Retinol 0.1 Cream",
        brand="COSRX",
        category="beginner retinol cream",
        url="https://www.cosrx.com/collections/well-aging/products/the-retinol-0-1-cream",
        best_for=("beginner retinol", "texture", "fine lines", "age 25 plus"),
        caution="Use only at night and pair with daily sunscreen.",
    ),
}
