import { api } from './api/client'
import SlotPicker from './pages/SlotPicker.jsx'

export default function App() {
  return (
    <main className="min-h-screen bg-slate-50 p-6">
      <h1 className="mx-auto mb-6 max-w-2xl text-2xl font-bold text-teal-800">
        ระบบจองคิวตรวจสุขภาพ
      </h1>
      <SlotPicker client={api} />
    </main>
  )
}
