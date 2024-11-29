import { useState, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { toast } from "@/components/ui/use-toast"

export function TransferModal({ isOpen, onClose, employee }) {
  const [newCompany, setNewCompany] = useState('')
  const [newProject, setNewProject] = useState('')
  const [effectiveDate, setEffectiveDate] = useState('')
  const [companies, setCompanies] = useState([])
  const [projects, setProjects] = useState([])

  useEffect(() => {
    // TODO: Fetch companies from API
    setCompanies(['公司A', '公司B', '公司C'])
  }, [])

  useEffect(() => {
    if (newCompany) {
      // TODO: Fetch projects for the selected company from API
      setProjects(
        newCompany === '公司A' ? ['项目X', '项目Y'] :
        newCompany === '公司B' ? ['项目Z', '项目W'] :
        ['项目V', '项目U']
      )
    } else {
      setProjects([])
    }
  }, [newCompany])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      // TODO: Implement actual transfer logic here
      console.log('Transferring employee:', { employee, newCompany, newProject, effectiveDate })
      
      // Simulating an API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      toast({
        title: "调岗申请提交成功",
        description: `${employee.name}的调岗申请已成功提交。`,
      })
      onClose()
    } catch (error) {
      toast({
        title: "调岗申请提交失败",
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
          <Select onValueChange={setNewProject} disabled={!newCompany}>
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

