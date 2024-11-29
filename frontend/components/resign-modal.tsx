import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { toast } from "@/components/ui/use-toast"

export function ResignModal({ isOpen, onClose, employee }) {
  const [resignDate, setResignDate] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      // TODO: Implement actual resignation logic
      console.log('Employee resigning:', { employee, resignDate })
      
      // Simulating an API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      toast({
        title: "离职申请提交成功",
        description: `${employee.name}的离职申请已成功提交。`,
      })
      onClose()
    } catch (error) {
      toast({
        title: "离职申请提交失败",
        description: "发生错误，请稍后重试。",
        variant: "destructive",
      })
    }
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

