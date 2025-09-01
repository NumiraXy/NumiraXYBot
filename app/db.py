from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
import os

# دیتابیس SQLite (برای شروع ساده)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./numira.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# تابع ساخت جدول‌ها
def init_db():
    Base.metadata.create_all(bind=engine)
