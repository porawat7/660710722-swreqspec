# RTM: Traceability Matrix

อ้างอิง: [spec.md](./spec.md), [plan.md](./plan.md), [tasks.md](./tasks.md), [test-cases.md](./test-cases.md)

สถานะสรุป:
- ผ่าน: มีหลักฐานจากโค้ดหรือ test ที่สอดคล้องกับข้อกำหนด
- บางส่วน: มีการ implement หรือ test บางส่วน แต่ยังไม่ครบตาม AC/FR
- ยังไม่ครอบคลุม: ไม่มีหลักฐานใน code/test หรือยังรอ task/คำถาม
- รอ Q-xx: ข้อกำหนดยังติด Open Question

## 1. Matrix ตามรอยข้อกำหนด

| ID | ประเภท | ข้อกำหนด/AC | หลักฐาน | สถานะ | หมายเหตุ |
|---|---|---|---|---|---|
| FR-BKG-01 | Functional | แสดงช่วงเวลาว่างภายใน 30 วัน พร้อมจำนวนที่นั่งคงเหลือ | [backend/app/slots/router.py](../../backend/app/slots/router.py), [backend/app/slots/service.py](../../backend/app/slots/service.py), [backend/tests/test_AC_BKG_05.py](../../backend/tests/test_AC_BKG_05.py) | บางส่วน | API GET /slots มีอยู่และ filter ตาม package_code แต่ยังไม่มี test case ครบสำหรับทุกเงื่อนไขของ FR-BKG-01 |
| FR-BKG-02 | Functional | ปฏิเสธการจองเมื่อมีคิวที่ยังไม่ได้ใช้ในวันเดียวกัน | ไม่มีหลักฐาน | ยังไม่ครอบคลุม | task T-04 รอทำ |
| FR-BKG-03 | Functional | แจ้งช่วงเวลาเต็มและเสนอ 3 ตัวเลือกใกล้เคียง | [frontend/src/pages/ConfirmBooking.jsx](../../frontend/src/pages/ConfirmBooking.jsx) | บางส่วน | UI ปรับให้แสดงข้อความ "ช่วงเวลาเต็ม" และ 3 ตัวเลือกตาม spec แล้ว แต่ยังต้องใช้ test ที่ถูกต้องจากแถว AC-BKG-03 เนื่องจากไฟล์ test ปัจจุบันมี assertion นอก test block |
| FR-BKG-04 | Functional | บันทึกการจอง ตัดที่นั่ง ออกหมายเลขคิว และส่งคำขอส่งข้อความยืนยัน | [backend/app/booking/service.py](../../backend/app/booking/service.py), [backend/app/booking/router.py](../../backend/app/booking/router.py), [backend/tests/test_AC_BKG_01.py](../../backend/tests/test_AC_BKG_01.py) | ผ่าน | มี test สำหรับ AC-BKG-01 และกฎปฏิเสธเมื่อ `remaining <= 0` แล้ว; queue format ยังติด Q-02 |
| FR-BKG-05 | Functional | หากส่งข้อความไม่สำเร็จ ต้องบันทึกการจองและส่งซ้ำภายใน 5 นาที | ไม่มีหลักฐาน | ยังไม่ครอบคลุม | task T-07 รอทำ |
| FR-BKG-06 | Functional | คำนวณช่วงว่างใหม่ตามแพ็กเกจที่เลือก | [backend/app/slots/service.py](../../backend/app/slots/service.py) | บางส่วน | โครงฟังก์ชันเห็นได้ แต่ยังไม่มี AC ที่ครอบคลุม specific flow ครบ |
| NFR-PERF-01 | Non-functional | p95 ไม่เกิน 2 วินาที สำหรับ 200 คน | [backend/tests/test_AC_BKG_05.py](../../backend/tests/test_AC_BKG_05.py) | ผ่าน | test แบบย่อส่วนผ่านตามค่า p95 |
| NFR-REL-02 | Non-functional | ส่งซ้ำภายใน 5 นาที | ไม่มีหลักฐาน | ยังไม่ครอบคลุม | task T-07 รอทำ |
| NFR-SEC-01 | Non-functional | TLS 1.2 ขึ้นไป | ไม่มีหลักฐานในโค้ด | ยังไม่ครอบคลุม | ไม่มีการตั้งค่า TLS ในสภาพแวดล้อม local test |
| NFR-USE-01 | Non-functional | ผู้ใช้ใหม่จองสำเร็จภายใน 3 นาที | ไม่มีหลักฐาน | ยังไม่ครอบคลุม | ยังไม่มี human usability test |
| CON-TECH-01 | Constraint | ใช้ PostgreSQL ตามมาตรฐานฝ่าย IT | [backend/app/config.py](../../backend/app/config.py), [backend/app/db/session.py](../../backend/app/db/session.py), [backend/app/db/models.py](../../backend/app/db/models.py) | ผ่าน | การตั้งค่า DATABASE_URL และ migration เตรียมไว้สำหรับ PostgreSQL |
| DOM-PDPA-01 | Constraint | audit log ทุกการเข้าถึงข้อมูลการจอง | ไม่มีหลักฐาน | ยังไม่ครอบคลุม | task T-08 รอทำ |
| IF-IDP-01 | Interface | ต้องได้รับผลยืนยันตัวตนก่อนเข้าถึงข้อมูลผู้รับบริการ | [backend/app/auth/idp.py](../../backend/app/auth/idp.py), [backend/app/booking/router.py](../../backend/app/booking/router.py) | ผ่าน | 401 เมื่อไม่มี token/ไม่ยืนยันตัวตน |
| IF-HIS-01 | Interface | ค้นข้อมูลผู้รับบริการจาก HIS ด้วยเลขบัตรประชาชนและใช้ HN ภายในระบบ | ไม่มีหลักฐาน | ยังไม่ครอบคลุม | task T-09 รอทำ |
| IF-NOT-01 | Interface | ส่งข้อความยืนยันผ่านระบบแจ้งเตือนแบบ asynchronous | ไม่มีหลักฐาน | ยังไม่ครอบคลุม | task T-07 รอทำ |
| AC-BKG-01 | Acceptance Criteria | ยืนยันตัวตนแล้วและช่วง 09.00 มีที่นั่งว่าง 1 ที่ จองสำเร็จ | [backend/tests/test_AC_BKG_01.py](../../backend/tests/test_AC_BKG_01.py) | ผ่าน | มี test สำหรับทางปกติ/ขอบ/ทางผิดแล้วเห็นว่าผ่าน |
| AC-BKG-02 | Acceptance Criteria | ปฏิเสธและแสดงหมายเลขคิวเดิมเมื่อมีคิวที่ยังไม่ได้ใช้ | ไม่มีหลักฐาน | ยังไม่ครอบคลุม | ไม่มี test case ที่สถานะใช้ได้ และ task T-04 ยังไม่เริ่ม |
| AC-BKG-03 | Acceptance Criteria | แจ้งช่วงเวลาเต็มและแสดง 3 ตัวเลือกที่ใกล้ที่สุด | [frontend/src/pages/ConfirmBooking.jsx](../../frontend/src/pages/ConfirmBooking.jsx), [frontend/src/__tests__/AC-BKG-03.test.jsx](../../frontend/src/__tests__/AC-BKG-03.test.jsx) | บางส่วน | UI ปรับให้สอดคล้องกับ spec แล้ว แต่ test file ปัจจุบันมี assertion ที่อยู่นอก test block ทำให้ verifier ไม่สามารถยืนยัน pass ได้ โดยไม่แก้ test ตามเงื่อนไข |
| AC-BKG-04 | Acceptance Criteria | จองถูกบันทึกและมีคิวส่งซ้ำภายใน 5 นาที | ไม่มีหลักฐาน | ยังไม่ครอบคลุม | task T-07 รอทำ |
| AC-BKG-05 | Acceptance Criteria | p95 <= 2 วินาที | [backend/tests/test_AC_BKG_05.py](../../backend/tests/test_AC_BKG_05.py) | ผ่าน | test แบบย่อส่วนผ่าน |
| AC-BKG-06 | Acceptance Criteria | มี audit log ระบุผู้เข้าถึง เวลา และรหัสผู้รับบริการ | ไม่มีหลักฐาน | ยังไม่ครอบคลุม | task T-08 รอทำ |

## 2. ข้อค้นพบ (Findings)

1. Q-02 ยังไม่ได้รับคำตอบจากเจ้าหน้าที่เวชระเบียน
   - ส่งผลต่อรูปแบบและการรีเซ็ตหมายเลขคิวใน FR-BKG-04 และ AC-BKG-01
   - ปัจจุบัน code ใช้รูปแบบ `A001` เป็นชั่วคราวและยังไม่สามารถ validate รูปแบบจริงได้

2. AC-BKG-02, AC-BKG-03, AC-BKG-04, AC-BKG-06 ยังไม่มีหลักฐานจาก test หรือ implementation ที่สมบูรณ์
   - สอดคล้องกับ task status ใน [tasks.md](./tasks.md) ที่ระบุ T-04, T-05, T-07, T-08 ยังเป็น "พร้อมทำ" หรือ "รอทำ"

3. บางส่วนของ requirement ได้รับการ implement แล้วแต่ยังไม่ครบตาม spec
   - GET /slots, IDP verification, booking creation มีอยู่
   - อย่างไรก็ตาม still missing: duplicate-day rejection, alternative slots, retry queue, audit logs, HIS lookup

## 3. สรุปการตรวจ

- ส่วนที่พร้อมใช้งานและมีหลักฐาน: FR-BKG-01 (บางส่วน), FR-BKG-04, IF-IDP-01, NFR-PERF-01, CON-TECH-01
- ส่วนที่ยังไม่สมบูรณ์ตาม spec: FR-BKG-02, FR-BKG-03, FR-BKG-05, FR-BKG-06, DOM-PDPA-01, IF-HIS-01, IF-NOT-01, NFR-REL-02, NFR-SEC-01, NFR-USE-01
- เปิดใช้งาน/validate ได้ในสภาพแวดล้อมปัจจุบัน: AC-BKG-01 และ AC-BKG-05

## 4. ข้อเสนอต่อไป

- ตัดสินเรื่อง Q-02 ก่อนเดินต่อเรื่อง queue format การแสดงผลและการออกเลขคิว
- ดำเนิน task ตาม [tasks.md](./tasks.md) สำหรับ T-04, T-05, T-07, T-08, T-09
- เมื่อข้อมูลใน [test-cases.md](./test-cases.md) ถูกยืนยันเป็น "ใช้ได้" แล้ว ให้สร้าง test ตาม AC ที่เหลือต่อไป
