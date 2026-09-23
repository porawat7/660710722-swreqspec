import { useEffect, useState } from 'react'

const today = () => new Date().toISOString().slice(0, 10)

export default function SlotPicker({ client, initialPackageCode = '' }) {
  const [packageCode, setPackageCode] = useState(initialPackageCode)
  const [dateFrom, setDateFrom] = useState(today)
  const [slots, setSlots] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!packageCode) {
      setSlots([])
      return
    }

    let active = true
    setLoading(true)
    setError('')
    // รองรับ FR-BKG-01 และ FR-BKG-06 ด้วยการโหลดช่วงเวลาใหม่ตามแพ็กเกจ
    client
      .getSlots({ dateFrom, packageCode })
      .then((result) => {
        if (active) setSlots(Array.isArray(result) ? result : result.slots ?? [])
      })
      .catch((requestError) => {
        if (active) setError(requestError.message)
      })
      .finally(() => {
        if (active) setLoading(false)
      })

    return () => {
      active = false
    }
  }, [client, dateFrom, packageCode])

  return (
    <section className="mx-auto max-w-2xl rounded-xl bg-white p-6 shadow-sm">
      <h2 className="text-xl font-semibold text-slate-900">เลือกแพ็กเกจและช่วงเวลาตรวจ</h2>
      <div className="mt-5 grid gap-4 sm:grid-cols-2">
        <label className="grid gap-2 text-sm font-medium text-slate-700">
          รหัสแพ็กเกจ
          <input
            aria-label="รหัสแพ็กเกจ"
            className="rounded border border-slate-300 px-3 py-2"
            value={packageCode}
            onChange={(event) => setPackageCode(event.target.value)}
            placeholder="กรอกรหัสแพ็กเกจ"
          />
        </label>
        <label className="grid gap-2 text-sm font-medium text-slate-700">
          เริ่มค้นหาตั้งแต่วันที่
          <input
            aria-label="เริ่มค้นหาตั้งแต่วันที่"
            className="rounded border border-slate-300 px-3 py-2"
            type="date"
            value={dateFrom}
            onChange={(event) => setDateFrom(event.target.value)}
          />
        </label>
      </div>

      {loading && <p className="mt-6 text-slate-600">กำลังโหลดช่วงเวลาว่าง...</p>}
      {error && <p className="mt-6 text-red-700">{error}</p>}
      {!loading && !error && packageCode && slots.length === 0 && (
        <p className="mt-6 text-slate-600">ไม่พบช่วงเวลาสำหรับแพ็กเกจนี้</p>
      )}
      {slots.length > 0 && (
        <ul className="mt-6 grid gap-3" aria-label="ช่วงเวลาตรวจ">
          {slots.map((slot) => (
            <li
              className="flex items-center justify-between rounded border border-slate-200 p-4"
              key={slot.id}
            >
              <span>
                <span className="block font-medium text-slate-900">
                  {slot.slot_date} เวลา {slot.start_time}
                </span>
                <span className="text-sm text-slate-600">แพ็กเกจ {slot.package_code}</span>
              </span>
              <span className="text-sm text-slate-700">
                ที่นั่งคงเหลือ {slot.remaining}
              </span>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
