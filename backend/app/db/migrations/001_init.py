from sqlalchemy import Engine

from app.db.models import Base


def upgrade(engine: Engine) -> None:
    """สร้างตารางข้อมูลที่รองรับ FR-BKG-01, FR-BKG-02, FR-BKG-04 และ IF-HIS-01."""
    Base.metadata.create_all(engine)
