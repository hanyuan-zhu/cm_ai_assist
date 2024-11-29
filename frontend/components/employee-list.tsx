'use client'

import { useState, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import { TransferModal } from './transfer-modal'
import { ResignModal } from './resign-modal'

export function EmployeeList() {
  const [employees, setEmployees] = useState([])
  const [isTransferModalOpen, setIsTransferModalOpen] = useState(false)
  const [isResignModalOpen, setIsResignModalOpen] = useState(false)
  const [selectedEmployee, setSelectedEmployee] = useState(null)

  useEffect(() => {
    // TODO: Fetch employees from API
    setEmployees([
      { id: 1, name: '李四', position: '开发工程师', company: '公司A', project: '项目X', status: '在岗' },
      { id: 2, name: '王五', position: '产品经理', company: '公司B', project: '项目Y', status: '在岗' },
      // ... more employees
    ])
  }, [])

  const handleTransfer = (employee) => {
    setSelectedEmployee(employee)
    setIsTransferModalOpen(true)
  }

  const handleResign = (employee) => {
    setSelectedEmployee(employee)
    setIsResignModalOpen(true)
  }

  return (
    <div className="space-y-4">
      <div className="max-h-64 overflow-y-auto">
        {employees.map((employee) => (
          <div key={employee.id} className="flex justify-between items-center p-2 border-b">
            <div>
              <p className="font-semibold">{employee.name}</p>
              <p className="text-sm text-gray-500">{employee.position} | {employee.company} | {employee.project}</p>
            </div>
            <div>
              <Button size="sm" onClick={() => handleTransfer(employee)}>调岗</Button>
              <Button size="sm" variant="destructive" onClick={() => handleResign(employee)} className="ml-2">离职</Button>
            </div>
          </div>
        ))}
      </div>

      <TransferModal 
        isOpen={isTransferModalOpen} 
        onClose={() => setIsTransferModalOpen(false)}
        employee={selectedEmployee}
      />

      <ResignModal
        isOpen={isResignModalOpen}
        onClose={() => setIsResignModalOpen(false)}
        employee={selectedEmployee}
      />
    </div>
  )
}

