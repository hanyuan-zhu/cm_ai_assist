'use client'

import { useState, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import { TransferModal } from './transfer-modal'
import { ResignModal } from './resign-modal'
import { getActiveEmployees } from '@/lib/api'
import { Employee } from '@/lib/types'
import { toast } from "@/components/ui/use-toast"

interface EmployeeListProps {
  refreshKey: number
}

export function EmployeeList({ refreshKey }: EmployeeListProps) {
  const [employees, setEmployees] = useState<Employee[]>([])
  const [isTransferModalOpen, setIsTransferModalOpen] = useState(false)
  const [isResignModalOpen, setIsResignModalOpen] = useState(false)
  const [selectedEmployee, setSelectedEmployee] = useState<Employee | null>(null)
  const [refresh, setRefresh] = useState(0)

  useEffect(() => {
    const fetchEmployees = async () => {
      try {
        const res = await getActiveEmployees()
        setEmployees(res.employees) // 直接使用 res.employees 而不是 res.data
      } catch (error) {
        toast({ 
          title: "获取员工列表失败", 
          description: error instanceof Error ? error.message : "未知错误",
          variant: "destructive" 
        })
      }
    }
    fetchEmployees()
  }, [refreshKey]) // 添加 refreshKey 依赖

  const handleTransfer = (employee: Employee) => {
    setSelectedEmployee(employee)
    setIsTransferModalOpen(true)
  }

  const handleResign = (employee: Employee) => {
    setSelectedEmployee(employee)
    setIsResignModalOpen(true)
  }

  const handleModalClose = () => {
    setIsTransferModalOpen(false)
    setIsResignModalOpen(false)  
    setSelectedEmployee(null)
    setRefresh(prev => prev + 1) // 触发刷新
  }

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold">员工列表</h2>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {employees.map((employee) => (
          <div 
            key={employee.id}
            className="p-4 border rounded-lg space-y-3"
          >
            <div>
              <h3 className="font-semibold">{employee.name}</h3>
              <p className="text-sm text-muted-foreground">
                入职日期: {employee.hire_date}
              </p>
            </div>

            <div>
              <p className="text-sm">公司: {employee.company_name || '待分配'}</p>
              <p className="text-sm">职位: {employee.position}</p>
              <p className="text-sm">状态: {employee.status}</p>
            </div>

            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => handleTransfer(employee)}
              >
                调动
              </Button>
              <Button
                variant="outline" 
                size="sm"
                onClick={() => handleResign(employee)}
              >
                离职
              </Button>
            </div>
          </div>
        ))}
      </div>

      {selectedEmployee && (
        <>
          <TransferModal
            isOpen={isTransferModalOpen}
            onClose={handleModalClose}
            employee={selectedEmployee}
          />
          <ResignModal 
            isOpen={isResignModalOpen}
            onClose={handleModalClose}
            employee={selectedEmployee}
          />
        </>
      )}
    </div>
  )
}

