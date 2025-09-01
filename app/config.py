# app/config.py
"""
Global configuration for Numira platform.
Keep secrets out of the repo: put them in a local .env (NOT public).
"""

import os
from datetime import time
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی از فایل .env (اگر وجود داشته باشد)
load_dotenv()

# ==== Security ====
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")  # برای session / jwt در آینده

# ==== Database ====
# مقدار پیش‌فرض sqlite برای تست محلی
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///numira.db")

# ==== Telegram bot ====
# نام متغیر: TELEGRAM_BOT_TOKEN (ثابت می‌ماند؛ لطفاً در .env همین نام استفاده شود)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", None)

# ==== TON blockchain ====
MOTHER_WALLET_ADDRESS = os.getenv("MOTHER_WALLET_ADDRESS", "")

# ==== Withdraw settings ====
# روزهای مجاز برداشت: کاما-جدا (حروف بزرگ یا کوچک مشکلی ندارد)
WITHDRAW_DAYS = [d.strip().upper() for d in os.getenv("WITHDRAW_DAYS", "MONDAY,THURSDAY").split(",")]

# تایمِ قطع درخواست برداشت (UTC) — از فرمت HH:MM:SS استفاده می‌کنیم
_withdraw_cutoff_str = os.getenv("WITHDRAW_CUTOFF", "18:00:00")
h, m, s = [int(x) for x in _withdraw_cutoff_str.split(":")]
WITHDRAW_CUTOFF = time(h, m, s)

# ==== App branding ====
APP_NAME = os.getenv("APP_NAME", "Numira")
APP_BRAND = os.getenv("APP_BRAND", "Numira XY")
