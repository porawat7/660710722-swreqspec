# Tasks: จองคิวตรวจสุขภาพ (Booking)

- Feature: จองคิวตรวจสุขภาพ (Booking)
- Spec ID: SPEC-BKG-001
- อ้างอิง: [spec.md](./spec.md), [plan.md](./plan.md)
- วันที่: 2569-09-23

สรุป: มีทั้งหมด 16 tasks โดยเรียงจากฐานข้อมูล บริการ/API หน้าจอ และการเชื่อมต่อ/ทดสอบ
มี 4 tasks ที่ต้องรอคำตอบ Q-02 เรื่องรูปแบบและวิธีออกหมายเลขคิว

## รายการ task

### T-01 สร้างตารางข้อมูลการจองและช่วงเวลา
- รองรับ: FR-BKG-01, FR-BKG-02, FR-BKG-04, FR-BKG-06, CON-TECH-01, IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-02 ถึง T-05
- ไฟล์ที่แตะ: `backend/app/db/models.py`, `backend/app/db/session.py`, `backend/app/db/migrations/001_init.py`, `backend/tests/conftest.py`
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: migration สร้างตาราง `slots`, `bookings` และ `audit_logs` ได้ และตาราง `bookings` ไม่มีฟิลด์เลขบัตรประชาชน
- สถานะ: พร้อมทำ

### T-02 สร้างบริการค้นหาช่วงเวลาว่าง
- รองรับ: FR-BKG-01, FR-BKG-06, ASM-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-06 และ T-12
- ไฟล์ที่แตะ: `backend/app/slots/service.py`, `backend/app/slots/router.py`, `backend/tests/test_slots.py`
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: `GET /slots` คืนช่วงเวลา จำนวนที่นั่งคงเหลือ และคำนวณรายการใหม่เมื่อเปลี่ยน `package_code`
- สถานะ: พร้อมทำ

### T-03 ตรวจผลยืนยันตัวตนก่อนเข้าถึงข้อมูลผู้รับบริการ
- รองรับ: IF-IDP-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-06 และ T-07
- ไฟล์ที่แตะ: `backend/app/auth/idp.py`, `backend/app/main.py`, `backend/tests/test_idp.py`
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: endpoint ที่แตะข้อมูลผู้รับบริการตรวจผลยืนยันตัวตนก่อนดำเนินการต่อ
- สถานะ: พร้อมทำ

### T-04 สร้างตัวเชื่อมค้นหา HN จาก HIS
- รองรับ: IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-06 และ T-07
- ไฟล์ที่แตะ: `backend/app/his/client.py`, `backend/app/booking/router.py`, `backend/tests/test_his.py`
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: `GET /patients/lookup` ส่งเลขบัตรไปค้น HIS และคืน HN โดยไม่มีการเก็บเลขบัตรในข้อมูลการจอง
- สถานะ: พร้อมทำ

### T-05 สร้าง API จองและการตัดที่นั่งแบบไม่เกินโควตา
- รองรับ: FR-BKG-04, ASM-01
- ตรวจด้วย: AC-BKG-01
- ไฟล์ที่แตะ: `backend/app/booking/service.py`, `backend/app/booking/router.py`, `backend/tests/test_AC_BKG_01.py`
- ต้องทำหลัง: T-01, T-03, T-04
- เสร็จเมื่อ: `test_AC_BKG_01` ผ่าน โดยบันทึกการจองและทำให้ `remaining` ของช่วง 09.00 น. เป็น 0
- สถานะ: พร้อมทำ

### T-06 ป้องกันการจองซ้ำในวันเดียวกัน
- รองรับ: FR-BKG-02, ASM-02, ASM-04
- ตรวจด้วย: AC-BKG-02
- ไฟล์ที่แตะ: `backend/app/booking/service.py`, `backend/tests/test_AC_BKG_02.py`
- ต้องทำหลัง: T-02, T-05
- เสร็จเมื่อ: `test_AC_BKG_02` ผ่าน โดยปฏิเสธการจองซ้ำและคืนหมายเลขคิวเดิม
- สถานะ: พร้อมทำ

### T-07 เสนอช่วงเวลาใกล้เคียงเมื่อช่วงเวลาเต็ม
- รองรับ: FR-BKG-03, ASM-02
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: `backend/app/slots/service.py`, `backend/app/booking/router.py`, `backend/tests/test_AC_BKG_03.py`
- ต้องทำหลัง: T-02, T-05
- เสร็จเมื่อ: `test_AC_BKG_03` ผ่าน โดยคืนสถานะเต็ม พร้อมช่วงว่าง 3 ช่วงในวันเดียวกันหรือวันถัดไป และไม่สร้างการจองซ้อน
- สถานะ: พร้อมทำ

### T-08 กำหนดและออกหมายเลขคิว
- รองรับ: FR-BKG-04, Q-02
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-09 และ T-10
- ไฟล์ที่แตะ: `backend/app/booking/service.py`, `backend/app/db/models.py`, `backend/tests/test_queue_number.py`
- ต้องทำหลัง: T-05, T-06
- เสร็จเมื่อ: ระบบออกหมายเลขคิวตามกติกาที่เจ้าหน้าที่เวชระเบียนตอบใน Q-02 และ test รูปแบบ/ลำดับหมายเลขผ่าน
- สถานะ: รอ Q-02

### T-09 สร้างคิวส่งข้อความยืนยันแบบ asynchronous
- รองรับ: FR-BKG-05, IF-NOT-01, ASM-03, NFR-REL-02
- ตรวจด้วย: AC-BKG-04
- ไฟล์ที่แตะ: `backend/app/notify/queue.py`, `backend/app/booking/service.py`, `backend/tests/test_AC_BKG_04.py`
- ต้องทำหลัง: T-05, T-08
- เสร็จเมื่อ: `test_AC_BKG_04` ผ่าน โดยการจองยังถูกบันทึก มีหมายเลขคิว และมีงาน retry ตามกำหนดภายใน 5 นาที
- สถานะ: รอ Q-02

### T-10 บันทึก audit log ทุกการเข้าถึงข้อมูลการจอง
- รองรับ: DOM-PDPA-01
- ตรวจด้วย: AC-BKG-06
- ไฟล์ที่แตะ: `backend/app/audit/middleware.py`, `backend/app/db/models.py`, `backend/tests/test_AC_BKG_06.py`
- ต้องทำหลัง: T-01, T-03, T-05
- เสร็จเมื่อ: `test_AC_BKG_06` ผ่าน โดย log มีผู้เข้าถึง เวลา และ HN และกำหนดการเก็บรักษาไม่น้อยกว่า 1 ปี
- สถานะ: พร้อมทำ

### T-11 เข้ารหัสการรับส่งข้อมูลการจอง
- รองรับ: NFR-SEC-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-16
- ไฟล์ที่แตะ: `backend/app/config.py`, `backend/tests/test_tls.py`, เอกสารการตั้งค่า deployment ตามโครงใน `plan.md`
- ต้องทำหลัง: T-05
- เสร็จเมื่อ: การตั้งค่า endpoint การจองบังคับใช้ TLS 1.2 ขึ้นไปและ test ตรวจค่าการตั้งค่าผ่าน
- สถานะ: พร้อมทำ

### T-12 ทดสอบประสิทธิภาพการค้นหาช่วงเวลา
- รองรับ: NFR-PERF-01, FR-BKG-01
- ตรวจด้วย: AC-BKG-05
- ไฟล์ที่แตะ: `backend/tests/test_AC_BKG_05.py`
- ต้องทำหลัง: T-02
- เสร็จเมื่อ: `test_AC_BKG_05` วัดผู้ใช้พร้อมกัน 200 คนและรายงาน p95 ไม่เกิน 2 วินาที หรือระบุผลการทดสอบบนเครื่องจริงแยกจาก Codespace
- สถานะ: พร้อมทำ

### T-13 สร้างหน้าเลือกแพ็กเกจและช่วงเวลา
- รองรับ: FR-BKG-01, FR-BKG-06
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-14 และ T-16
- ไฟล์ที่แตะ: `frontend/src/pages/SlotPicker.jsx`, `frontend/src/api/client.js`, `frontend/src/App.jsx`, `frontend/src/__tests__/SlotPicker.test.jsx`
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: หน้าจอแสดงช่วงเวลาและที่นั่งคงเหลือ และโหลดข้อมูลใหม่เมื่อเปลี่ยนแพ็กเกจด้วย API จำลอง
- สถานะ: เสร็จ รอทีมตรวจ

### T-14 สร้างหน้ายืนยันและตัวเลือกช่วงเวลาใหม่
- รองรับ: FR-BKG-03
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: `frontend/src/pages/ConfirmBooking.jsx`, `frontend/src/__tests__/AC-BKG-03.test.jsx`
- ต้องทำหลัง: T-13
- เสร็จเมื่อ: `AC-BKG-03.test.jsx` ผ่าน โดยแสดง “ช่วงเวลาเต็ม” และตัวเลือกช่วงเวลาว่าง 3 รายการจาก API จำลอง
- สถานะ: พร้อมทำ

### T-15 สร้างหน้าแสดงผลการจอง
- รองรับ: FR-BKG-04, FR-BKG-05
- ตรวจด้วย: AC-BKG-01, AC-BKG-04
- ไฟล์ที่แตะ: `frontend/src/pages/BookingResult.jsx`, `frontend/src/__tests__/BookingResult.test.jsx`
- ต้องทำหลัง: T-08, T-09
- เสร็จเมื่อ: หน้าจอแสดงหมายเลขคิวทั้งกรณีส่งข้อความสำเร็จและกรณีส่งข้อความไม่สำเร็จ
- สถานะ: รอ Q-02

### T-16 ทดสอบการใช้งานและเชื่อมหน้าจอกับ API จริง
- รองรับ: NFR-USE-01, FR-BKG-01, FR-BKG-03, FR-BKG-04, FR-BKG-05, IF-IDP-01, IF-HIS-01, IF-NOT-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานตรวจระบบรวมของ T-05 ถึง T-15
- ไฟล์ที่แตะ: `frontend/src/api/client.js`, `frontend/src/App.jsx`, `frontend/src/__tests__/integration.test.jsx`, `backend/tests/test_integration.py`
- ต้องทำหลัง: T-02, T-03, T-04, T-05, T-07, T-09, T-10, T-11, T-12, T-13, T-14, T-15
- เสร็จเมื่อ: หน้าจอเรียก API จริงได้ครบ flow และผลทดสอบผู้ใช้ใหม่ 10 คนมีอย่างน้อย 8 คนจองสำเร็จภายใน 3 นาทีโดยไม่ขอความช่วยเหลือ
- สถานะ: รอ Q-02

## ตารางตรวจความครบ

### Acceptance Criteria

| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-BKG-01 | T-05, T-15 |
| AC-BKG-02 | T-06 |
| AC-BKG-03 | T-07, T-14 |
| AC-BKG-04 | T-09, T-15 |
| AC-BKG-05 | T-12 |
| AC-BKG-06 | T-10 |

### Constraint ID

| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| CON-TECH-01 | T-01 |
| DOM-PDPA-01 | T-10 |
| IF-IDP-01 | T-03, T-16 |
| IF-HIS-01 | T-04, T-16 |
| IF-NOT-01 | T-09, T-16 |

## สิ่งที่ยังไม่ทำ

- Q-02: หมายเลขคิวรีเซ็ตรายวันหรือนับต่อเนื่อง และมีรูปแบบอย่างไร (เช่น `A001`) ต้องถามเจ้าหน้าที่เวชระเบียน
  - รออยู่ที่: T-08, T-09, T-15, T-16
