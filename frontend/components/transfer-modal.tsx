import { useState, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { toast } from "@/components/ui/use-toast"
import { transferEmployee, getCompanies, getProjects } from '@/lib/api'
import { Employee, Project, Company } from '@/lib/types'

interface TransferModalProps {
  isOpen: boolean
  onClose: () => void
  employee: Employee | null
}

export function TransferModal({ isOpen, onClose, employee }: TransferModalProps) {
  const [newCompany, setNewCompany] = useState<string>('')
  const [newProject, setNewProject] = useState<string>('')
  const [effectiveDate, setEffectiveDate] = useState<string>('')
  const [companies, setCompanies] = useState<Company[]>([])
  const [projects, setProjects] = useState<Project[]>([])

  // 获取公司列表
  useEffect(() => {
    const fetchCompanies = async () => {
      try {
        const { companies: companyList } = await getCompanies()
        setCompanies(companyList)
      } catch (error) {
        toast({ 
          title: "获取公司列表失败", 
          description: error instanceof Error ? error.message : "未知错误", 
          variant: "destructive" 
        })
      }
    }
    if (isOpen) {
      fetchCompanies()
    }
  }, [isOpen])

  // 获取项目列表
  const handleCompanyChange = async (companyId: string) => {
    setNewCompany(companyId)
    setNewProject('')
    
    if (!companyId) {
      setProjects([])
      return
    }
    
    try {
      const { projects: projectList } = await getProjects(Number(companyId))
      setProjects(projectList)
    } catch (error) {
      toast({
        title: "获取项目列表失败",
        description: error instanceof Error ? error.message : "未知错误",
        variant: "destructive"
      })
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!employee || !newCompany || !newProject || !effectiveDate) {
      toast({
        title: "请填写完整信息",
        description: "请选择新公司、新项目并设置生效日期",
        variant: "destructive"
      })
      return
    }

    try {
      const response = await transferEmployee(
        employee.id,
        Number(newCompany),
        Number(newProject),
        effectiveDate
      )

      if (response.success) {
        toast({
          title: "调岗申请提交成功",
          description: `${employee.name}的调岗申请已成功提交。`,
        })
        onClose()
      } else {
        throw new Error(response.message)
      }
    } catch (error) {
      toast({
        title: "调岗申请提交失败",
        description: error instanceof Error ? error.message : "发生错误，请稍后重试。",
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
          <div className="space-y-2">
            <label>新公司</label>
            <Select
              value={newCompany}
              onValueChange={handleCompanyChange}
            >
              <SelectTrigger>
                <SelectValue placeholder="选择新公司" />
              </SelectTrigger>
              <SelectContent>
                {companies.map(company => (
                  <SelectItem key={company.id} value={String(company.id)}>
                    {company.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <label>新项目</label>
            <Select
              value={newProject}
              onValueChange={setNewProject}
              disabled={!newCompany}
            >
              <SelectTrigger>
                <SelectValue placeholder="选择新项目" />
              </SelectTrigger>
              <SelectContent>
                {projects.map(project => (
                  <SelectItem key={project.id} value={String(project.id)}>
                    {project.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <label>生效日期</label>
            <Input
              type="date"
              value={effectiveDate}
              onChange={(e) => setEffectiveDate(e.target.value)}
            />
          </div>

          <Button type="submit">提交调岗申请</Button>
        </form>
      </DialogContent>
    </Dialog>
  )
}

