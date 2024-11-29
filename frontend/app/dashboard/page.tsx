'use client'

import { useState, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { EmployeeList } from '@/components/employee-list'
import { AddEmployeeModal } from '@/components/add-employee-modal'
import { PendingChangesList } from '@/components/pending-changes-list'
import { LogoutButton } from '@/components/logout-button'

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
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold">欢迎，{user.name}！</h1>
          <p className="text-gray-600">{user.role}</p>
        </div>
        <div className="flex items-center gap-4">
          <Button onClick={() => setIsAddEmployeeModalOpen(true)}>
            添加新员工
          </Button>
          <LogoutButton />
        </div>
      </div>
      
      <div className="space-y-6">
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

      <AddEmployeeModal 
        isOpen={isAddEmployeeModalOpen} 
        onClose={() => setIsAddEmployeeModalOpen(false)} 
      />
    </div>
  )
}

