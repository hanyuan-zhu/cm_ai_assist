'use client'

import { useState, useEffect } from 'react'
import { Button } from "@/components/ui/button"

export function PendingChangesList({ role }) {
  const [pendingChanges, setPendingChanges] = useState([])

  useEffect(() => {
    // TODO: Fetch pending changes from API based on role
    setPendingChanges([
      { id: 1, type: '调岗', name: '张三', fromCompany: '公司A', toCompany: '公司B', fromProject: '项目X', toProject: '项目Y', effectiveDate: '2023-06-01' },
      { id: 2, type: '入职', name: '李四', toCompany: '公司C', toProject: '项目Z', effectiveDate: '2023-06-15' },
      { id: 3, type: '离职', name: '王五', fromCompany: '公司B', fromProject: '项目Y', effectiveDate: '2023-06-30' },
    ])
  }, [role])

  const getChangeColor = (type) => {
    switch (type) {
      case '入职': return 'text-green-600'
      case '离职': return 'text-red-600'
      case '调岗': return 'text-blue-600'
      default: return ''
    }
  }

  return (
    <div className="space-y-4">
      <div className="max-h-64 overflow-y-auto">
        {pendingChanges.map((change) => (
          <div key={change.id} className={`flex justify-between items-center p-2 border-b ${getChangeColor(change.type)}`}>
            <div>
              <p className="font-semibold">{change.name}</p>
              <p className="text-sm">
                {change.type === '调岗' && `${change.fromCompany} → ${change.toCompany}`}
                {change.type === '入职' && `加入 ${change.toCompany}`}
                {change.type === '离职' && `离开 ${change.fromCompany}`}
              </p>
              <p className="text-sm">生效日期: {change.effectiveDate}</p>
            </div>
            <Button size="sm">确认</Button>
          </div>
        ))}
      </div>
    </div>
  )
}

