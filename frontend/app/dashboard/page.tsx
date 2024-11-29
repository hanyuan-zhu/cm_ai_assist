'use client'

import { useState, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { EmployeeList } from '@/components/employee-list'
import { AddEmployeeModal } from '@/components/add-employee-modal'
import { PendingChangesList } from '@/components/pending-changes-list'

export default function DashboardPage() {
  const [user, setUser] = useState(null)
  const [isAddEmployeeModalOpen, setIsAddEmployeeModalOpen] = useState(false)

  useEffect(() => {
    // TODO: Fetch user data from API
    setUser({ name: '张三', role: '总公司管理员' })
  }, [])

  if (!user) return <div>Loading...</div>

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">欢迎，{user.name}！</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card>
          <CardHeader>
            <CardTitle>在岗人员名单</CardTitle>
          </CardHeader>
          <CardContent>
            <EmployeeList />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>待确认变动名单</CardTitle>
          </CardHeader>
          <CardContent>
            <PendingChangesList role={user.role} />
          </CardContent>
        </Card>
      </div>

      <Button onClick={() => setIsAddEmployeeModalOpen(true)} className="mt-4">
        添加新员工
      </Button>

      <AddEmployeeModal 
        isOpen={isAddEmployeeModalOpen} 
        onClose={() => setIsAddEmployeeModalOpen(false)} 
      />
    </div>
  )
}

