import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"

export function ResignModal({ isOpen, onClose, employee }) {
  const [resignDate, setResignDate] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // TODO: Implement resignation logic
    console.log('Employee resigning:', { employee, resignDate })
    onClose()
  }

  if (!employee) return null

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>离职 - {employee.name}</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            type="date"
            placeholder="离职日期"
            value={resignDate}
            onChange={(e) => setResignDate(e.target.value)}
          />
          <Button type="submit">提交离职申请</Button>
        </form>
      </DialogContent>
    </Dialog>
  )
}

