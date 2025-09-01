from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(String, unique=True, index=True)
    username = Column(String, nullable=True)
    wallet_address = Column(String, unique=True, nullable=True)
    package_key = Column(String, nullable=True)  # ATOM / MOLECULE / UNIVERSE
    left_volume = Column(Float, default=0.0)
    right_volume = Column(Float, default=0.0)
    rank_code = Column(String, default="R1")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    referrals = relationship("Referral", back_populates="parent")


class Referral(Base):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("users.id"))
    child_id = Column(Integer, ForeignKey("users.id"))
    side = Column(String)  # "L" یا "R"

    parent = relationship("User", foreign_keys=[parent_id], back_populates="referrals")


class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tx_type = Column(String)  # deposit / withdraw / bonus / purchase
    amount_ton = Column(Float, nullable=False)
    status = Column(String, default="pending")  # pending / confirmed / failed
    tx_hash = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class WithdrawRequest(Base):
    __tablename__ = "withdraw_requests"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount_ton = Column(Float, nullable=False)
    status = Column(String, default="pending")  # pending / approved / paid / rejected
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)
