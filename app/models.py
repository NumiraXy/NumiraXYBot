# app/models.py
from datetime import datetime
import enum

from sqlalchemy import (
    Column, Integer, BigInteger, String, DateTime, Boolean,
    ForeignKey, Numeric, Enum, Text, UniqueConstraint, Index
)
from sqlalchemy.orm import relationship

from .db import Base
from .constants import PACKAGES

# -------- Enums --------
class PackageKey(enum.Enum):
    ATOM = "ATOM"
    MOLECULE = "MOLECULE"
    UNIVERSE = "UNIVERSE"

class Side(enum.Enum):
    LEFT = "L"
    RIGHT = "R"

class WithdrawStatus(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    PAID = "PAID"
    REJECTED = "REJECTED"
    CANCELED = "CANCELED"

class CommissionType(enum.Enum):
    REFERRAL = "REFERRAL"
    BINARY = "BINARY"
    RANK = "RANK"

class TokenSymbol(enum.Enum):
    XYRIS = "XYRIS"
    XYRON = "XYRON"

# -------- Core Models --------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    # Telegram identity
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    username = Column(String(64), index=True)
    first_name = Column(String(64))
    last_name = Column(String(64))

    # TON wallet
    ton_wallet = Column(String(128), index=True)  # user TON address (optional at signup)

    # Package (None until the user pays)
    package_key = Column(Enum(PackageKey), nullable=True)

    # Binary tree placement
    parent_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    side_in_parent = Column(Enum(Side), nullable=True)  # L or R
    left_child_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    right_child_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Two distinct referral codes (left/right)
    left_ref_code = Column(String(32), unique=True, index=True)
    right_ref_code = Column(String(32), unique=True, index=True)

    # Volumes with carry-forward (TON)
    left_volume_ton = Column(Numeric(20, 4), default=0)   # total + carry
    right_volume_ton = Column(Numeric(20, 4), default=0)

    # Rank
    rank_code = Column(String(8), default="R0", index=True)

    # Balances
    commission_balance_ton = Column(Numeric(20, 9), default=0)  # available for withdraw
    xyris_balance = Column(Numeric(20, 0), default=0)           # shown inside app only (not on-chain yet)
    xyron_balance = Column(Numeric(20, 0), default=0)

    # Status
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships (self-referential)
    parent = relationship("User", remote_side=[id], backref="children", foreign_keys=[parent_id])
    left_child = relationship("User", foreign_keys=[left_child_id], post_update=True, uselist=False)
    right_child = relationship("User", foreign_keys=[right_child_id], post_update=True, uselist=False)

    __table_args__ = (
        Index("ix_users_parent_side", "parent_id", "side_in_parent"),
    )

class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    package_key = Column(Enum(PackageKey), nullable=False)
    ton_paid = Column(Numeric(20, 4), nullable=False)      # amount user paid in TON
    tx_hash = Column(String(128))                          # optional, if you store payment proof
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="purchases")

class CommissionLedger(Base):
    """
    Stores TON commissions (referral, binary, rank).
    """
    __tablename__ = "commission_ledger"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    source_user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=True)  # who triggered this commission
    kind = Column(Enum(CommissionType), nullable=False)
    amount_ton = Column(Numeric(20, 9), nullable=False)
    meta = Column(Text)  # JSON string (e.g., {"package":"ATOM","levels":...})
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", foreign_keys=[user_id], backref="commissions")
    source_user = relationship("User", foreign_keys=[source_user_id])

class TokenLedger(Base):
    """
    Tracks in-app token accruals (XYRIS/XYRON) not on-chain yet.
    """
    __tablename__ = "token_ledger"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    token = Column(Enum(TokenSymbol), nullable=False)
    amount = Column(Numeric(20, 0), nullable=False)  # integer units
    reason = Column(String(32))                      # e.g., "package_reward", "rank_reward"
    meta = Column(Text)                              # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="token_entries")

class WithdrawRequest(Base):
    __tablename__ = "withdraw_requests"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    amount_ton = Column(Numeric(20, 9), nullable=False)
    status = Column(Enum(WithdrawStatus), default=WithdrawStatus.PENDING, index=True)
    requested_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime)
    payout_tx_hash = Column(String(128))  # TON tx hash when paid
    note = Column(Text)                   # optional admin note

    user = relationship("User", backref="withdraw_requests")

class VolumeLog(Base):
    """
    Optional: atomic records for left/right volume increments per user.
    Useful for audits and exact binary calculations by level.
    """
    __tablename__ = "volume_log"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    leg = Column(Enum(Side), nullable=False)                # L or R
    ton_amount = Column(Numeric(20, 4), nullable=False)
    depth_level = Column(Integer, nullable=True)            # optional: depth from the buyer
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="volume_events")
