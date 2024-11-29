import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"

export function AddEmployeeModal({ isOpen, onClose }) {
  const [name, setName] = useState('')
  const [position, setPosition] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // TODO: Implement employee addition logic
    console.log('Adding employee:', { name, position })
    onClose()
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>添加新员工</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            placeholder="姓名"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <Input
            placeholder="岗位"
            value={position}
            onChange={(e) => setPosition(e.target.value)}
          />
          <Button type="submit">添加</Button>
        </form>
      </DialogContent>
    </Dialog>
  )
}

