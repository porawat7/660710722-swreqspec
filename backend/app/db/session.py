import os

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


def create_database_engine(database_url: str) -> Engine:
    """สร้าง engine สำหรับฐานข้อมูลตาม CON-TECH-01."""
    return create_engine(database_url, future=True)


def create_session_factory(database_url: str) -> sessionmaker[Session]:
    """สร้าง session factory จาก URL ที่กำหนดโดยสภาพแวดล้อมการทำงาน."""
    engine = create_database_engine(database_url)
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def create_configured_session_factory() -> sessionmaker[Session]:
    """อ่าน DATABASE_URL เพื่อเชื่อมต่อฐานข้อมูลของระบบตาม CON-TECH-01."""
    database_url = os.environ["DATABASE_URL"]
    return create_session_factory(database_url)
