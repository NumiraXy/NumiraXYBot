
"""
Global configuration for Numira platform
(keep all sensitive values in environment variables, not plain text!)
"""

import os
from datetime import time

# ==== Security ====
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")  # for sessions, JWT, etc.

# ==== Database ====
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///numira.db")

# ==== Telegram bot ====
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "PUT-YOUR-TOKEN-HERE")

# ==== TON blockchain ====
MOTHER_WALLET_ADDRESS = os.getenv("MOTHER_WALLET_ADDRESS", "PUT-WALLET-HERE")

# Withdraw only possible on Mondays & Thursdays (UTC)
WITHDRAW_DAYS = ["MONDAY", "THURSDAY"]

# Cut-off time for withdrawal requests (UTC)
WITHDRAW_CUTOFF = time(18, 0, 0)  # 18:00 UTC = 20:00 Europe time

# ==== App branding ====
APP_NAME = "Numira"
APP_BRAND = "Numira XY"
