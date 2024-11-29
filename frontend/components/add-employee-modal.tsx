import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { toast } from "@/components/ui/use-toast"

export function AddEmployeeModal({ isOpen, onClose }) {
  const [name, setName] = useState('')
  const [position, setPosition] = useState('')
  const [hireDate, setHireDate] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const response = await fetch('/api/employees', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, position, hireDate }),
      })

      if (!response.ok) {
        throw new Error('Failed to add employee')
      }

      const data = await response.json()
      if (data.success) {
        toast({
          title: "员工添加成功",
          description: `${name} 已成功添加到系统。`,
        })
        onClose()
      } else {
        throw new Error('Failed to add employee')
      }
    } catch (error) {
      console.error('Error adding employee:', error)
      toast({
        title: "添加失败",
        description: "添加员工时发生错误，请稍后重试。",
        variant: "destructive",
      })
    }
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
            required
          />
          <Input
            placeholder="岗位"
            value={position}
            onChange={(e) => setPosition(e.target.value)}
            required
          />
          <Input
            type="date"
            placeholder="入职日期"
            value={hireDate}
            onChange={(e) => setHireDate(e.target.value)}
            required
          />
          <Button type="submit">添加</Button>
        </form>
      </DialogContent>
    </Dialog>
  )
}

