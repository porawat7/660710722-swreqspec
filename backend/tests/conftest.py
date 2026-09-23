from collections.abc import Iterator

import pytest
from sqlalchemy import inspect
from sqlalchemy.engine import Engine
from sqlalchemy.pool import StaticPool
from sqlalchemy import create_engine

from app.db.models import Base


@pytest.fixture
def database_engine() -> Iterator[Engine]:
    """เตรียมฐานข้อมูลทดสอบสำหรับตรวจ schema ของ T-01."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


def test_t01_creates_required_tables_without_national_id(database_engine: Engine) -> None:
    """ยืนยันว่า schema มีตารางที่ต้องใช้และไม่เก็บเลขบัตรประชาชนตาม IF-HIS-01."""
    table_names = set(inspect(database_engine).get_table_names())

    assert table_names == {"slots", "bookings", "audit_logs"}
    assert "national_id" not in {
        column["name"] for column in inspect(database_engine).get_columns("bookings")
    }
