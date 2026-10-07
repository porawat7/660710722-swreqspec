# test ของ T-03: จองคิวสำเร็จ
# AC-BKG-01 (FR-BKG-04)
from tests.conftest import AUTH


def test_AC_BKG_01(client, make_slot):
    """AC-BKG-01: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง จองแล้วต้องสำเร็จ"""
    slot = make_slot(start="09:00", remaining=1)

    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    assert res.status_code == 201


# Given: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
# When: ผู้ใช้กดยืนยันการจองช่วง 09.00 น.
# Then: บันทึกการจองสำเร็จ; แสดงหมายเลขคิว (รอ Q-02); ที่นั่งว่างของช่วงนั้นเป็น 0

def test_TC_BKG_01_1_booking_success(client, make_slot, db):
    slot = make_slot(start="09:00", remaining=1)

    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    assert res.status_code == 201
    assert res.json()["queue_no"]
    db_slot = db.get(type(slot), slot.id)
    assert db_slot.remaining == 0


# Given: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่างเท่ากับ 1 ที่ตรงขอบก่อนยืนยัน
# When: ผู้ใช้กดยืนยันการจองช่วง 09.00 น.
# Then: บันทึกการจองสำเร็จ; แสดงหมายเลขคิว (รอ Q-02); ที่นั่งว่างของช่วงนั้นลดจาก 1 เป็น 0 อย่างแม่นยำ

def test_TC_BKG_01_2_booking_at_capacity_limit(client, make_slot, db):
    slot = make_slot(start="09:00", remaining=1)

    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    assert res.status_code == 201
    assert res.json()["queue_no"]
    db_slot = db.get(type(slot), slot.id)
    assert db_slot.remaining == 0


# Given: ยืนยันตัวตนยังไม่สำเร็จ หรือไม่มีผลยืนยันตัวตนจากระบบยืนยันตัวตน
# When: ผู้ใช้พยายามยืนยันการจองช่วง 09.00 น.
# Then: ไม่บันทึกการจอง; ไม่ตัดจำนวนที่นั่งของช่วง 09.00 น.; ห้ามแสดงหมายเลขคิว

def test_TC_BKG_01_3_booking_requires_verified_identity(client, make_slot, db):
    slot = make_slot(start="09:00", remaining=1)

    res = client.post("/bookings", json={"slot_id": slot.id})

    assert res.status_code == 401
    assert "ยังไม่ได้ยืนยันตัวตน" in res.json()["detail"]
    db_slot = db.get(type(slot), slot.id)
    assert db_slot.remaining == 1
