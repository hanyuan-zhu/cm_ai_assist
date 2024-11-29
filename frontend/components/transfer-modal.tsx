import { useState, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"

export function TransferModal({ isOpen, onClose, employee }) {
  const [newCompany, setNewCompany] = useState('')
  const [newProject, setNewProject] = useState('')
  const [effectiveDate, setEffectiveDate] = useState('')
  const [companies, setCompanies] = useState([])
  const [projects, setProjects] = useState([])

  useEffect(() => {
    // TODO: Fetch companies and projects from API
    setCompanies(['公司A', '公司B', '公司C'])
    setProjects(['项目X', '项目Y', '项目Z'])
  }, [])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // TODO: Implement transfer logic
    console.log('Transferring employee:', { employee, newCompany, newProject, effectiveDate })
    onClose()
  }

  if (!employee) return null

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>调岗 - {employee.name}</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <Select onValueChange={setNewCompany}>
            <SelectTrigger>
              <SelectValue placeholder="选择新公司" />
            </SelectTrigger>
            <SelectContent>
              {companies.map((company) => (
                <SelectItem key={company} value={company}>{company}</SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Select onValueChange={setNewProject}>
            <SelectTrigger>
              <SelectValue placeholder="选择新项目" />
            </SelectTrigger>
            <SelectContent>
              {projects.map((project) => (
                <SelectItem key={project} value={project}>{project}</SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Input
            type="date"
            placeholder="生效日期"
            value={effectiveDate}
            onChange={(e) => setEffectiveDate(e.target.value)}
          />
          <Button type="submit">提交调岗申请</Button>
        </form>
      </DialogContent>
    </Dialog>
  )
}

