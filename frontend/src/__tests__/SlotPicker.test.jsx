import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { vi } from 'vitest'
import SlotPicker from '../pages/SlotPicker.jsx'

test('แสดงช่วงเวลาและจำนวนที่นั่งคงเหลือตามแพ็กเกจ และโหลดใหม่เมื่อเปลี่ยนแพ็กเกจ', async () => {
  const client = {
    getSlots: vi.fn(({ packageCode }) =>
      Promise.resolve([
        {
          id: packageCode,
          slot_date: '2569-10-01',
          start_time: '09:00',
          package_code: packageCode,
          remaining: packageCode === 'package-a' ? 2 : 4,
        },
      ]),
    ),
  }

  render(<SlotPicker client={client} initialPackageCode="package-a" />)

  expect(await screen.findByText('ที่นั่งคงเหลือ 2')).toBeTruthy()
  expect(client.getSlots).toHaveBeenCalledWith(
    expect.objectContaining({ packageCode: 'package-a' }),
  )

  fireEvent.change(screen.getByLabelText('รหัสแพ็กเกจ'), {
    target: { value: 'package-b' },
  })

  expect(await screen.findByText('ที่นั่งคงเหลือ 4')).toBeTruthy()
  await waitFor(() =>
    expect(client.getSlots).toHaveBeenLastCalledWith(
      expect.objectContaining({ packageCode: 'package-b' }),
    ),
  )
})
