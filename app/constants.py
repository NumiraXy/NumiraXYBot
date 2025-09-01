# ==== Project meta ====
PROJECT_NAME = "Numira"
PLATFORM_BRAND = "Numira XY"

# ==== Tokens (distribution + supply) ====
TOKENS = {
    "XYRIS": {"name": "XYRIS", "symbol": "XYRIS", "total_supply": 44_000_000},
    "XYRON": {"name": "XYRON", "symbol": "XYRON", "total_supply": 11_000_000_000},
}

# ==== Binary rule ====
# هر 10 تون در دست راست + 10 تون در دست چپ = 1 سیکل باینری
BINARY_CYCLE_UNIT_TON = 10

# ==== Packages ====
# direct_referral = درصد رفرال مستقیم
# binary_tiers = [(از لول, تا لول, درصد باینری)] — همیشه بر اساس دستِ کوچک
PACKAGES = [
    {
        "key": "ATOM",
        "name": "Atom",
        "ton": 10,
        "badge": "A",
        "color": "#8A6BFF",
        "direct_referral": 0.08,  # 8%
        "binary_tiers": [
            (1, 30, 0.07),      # 7%
            (31, 100, 0.05),    # 5%
            (101, 1000, 0.03),  # 3%
        ],
        "token_rewards": {"XYRIS": 2, "XYRON": 300},  # پاداش شروع
    },
    {
        "key": "MOLECULE",
        "name": "Molecule",
        "ton": 30,
        "badge": "M",
        "color": "#6C5CE7",
        "direct_referral": 0.10,  # 10%
        "binary_tiers": [
            (1, 30, 0.10),        # 10%
            (31, 100, 0.08),      # 8%
            (101, 1000, 0.05),    # 5%
            (1001, 10**9, 0.03),  # 3%
        ],
        "token_rewards": {"XYRIS": 6, "XYRON": 1000},
    },
    {
        "key": "UNIVERSE",
        "name": "Universe",
        "ton": 100,
        "badge": "U",
        "color": "#2B1544",  # مشکی-بنفش لوکس
        "direct_referral": 0.12,  # 12%
        "binary_tiers": [
            (1, 30, 0.12),        # 12%
            (31, 100, 0.10),      # 10%
            (101, 1000, 0.08),    # 8%
            (1001, 10**9, 0.05),  # 5%
        ],
        "token_rewards": {"XYRIS": 20, "XYRON": 3500},
    },
]

# ایندکس‌های کمکی
PACKAGE_INDEX = {p["name"]: p for p in PACKAGES}
PACKAGE_BY_KEY = {p["key"]: p for p in PACKAGES}

# ==== Ranks (9 levels) با Carry Forward ====
# need_left/right بر حسب TON تعادلی؛ rewards مطابق آخرین جدول تو
RANKS = [
    {"code": "R1", "name": "Primordial Spark", "need_left": 50,     "need_right": 50,     "rewards": {"TON": 3,    "XYRIS": 2,     "XYRON": 400}},
    {"code": "R2", "name": "Sacred Flame",     "need_left": 250,    "need_right": 250,    "rewards": {"TON": 15,   "XYRIS": 5,     "XYRON": 1000}},
    {"code": "R3", "name": "Celestial River",  "need_left": 1000,   "need_right": 1000,   "rewards": {"TON": 50,   "XYRIS": 20,    "XYRON": 5000}},
    {"code": "R4", "name": "Storm of Creation","need_left": 3000,   "need_right": 3000,   "rewards": {"TON": 150,  "XYRIS": 50,    "XYRON": 20000}},
    {"code": "R5", "name": "Ocean of Infinity","need_left": 10000,  "need_right": 10000,  "rewards": {"TON": 500,  "XYRIS": 100,   "XYRON": 60000}},
    {"code": "R6", "name": "Radiant Star",     "need_left": 30000,  "need_right": 30000,  "rewards": {"TON": 1000, "XYRIS": 300,   "XYRON": 140000}},
    {"code": "R7", "name": "Galactic Core",    "need_left": 100000, "need_right": 100000, "rewards": {"TON": 5000, "XYRIS": 1000,  "XYRON": 500000}},
    {"code": "R8", "name": "Cosmic Ascension", "need_left": 250000, "need_right": 250000, "rewards": {"TON": 7500, "XYRIS": 10000, "XYRON": 1000000}},
    {"code": "R9", "name": "Eternal Origin",   "need_left": 500000, "need_right": 500000, "rewards": {"TON": 35000,"XYRIS": 0,     "XYRON": 5000000}},
]

RANK_INDEX = {r["code"]: r for r in RANKS}

# ==== UI colors (برای داشبورد گرافیکی داخل تلگرام/وب) ====
UI_COLORS = {
    "bg_dark": "#0D0516",
    "bg_grad_1": "#1A0B2E",
    "bg_grad_2": "#2F0E4F",
    "accent": "#B388FF",
    "ok": "#54D1B6",
    "warn": "#FFB020",
    "err": "#F86A6A",
}
