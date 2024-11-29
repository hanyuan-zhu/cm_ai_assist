'use client'

import { useState, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import { UserPlus, UserMinus, UserCog } from 'lucide-react'
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog"
import { toast } from "@/components/ui/use-toast"

export function PendingChangesList({ role }) {
  const [pendingChanges, setPendingChanges] = useState([])
  const [confirmDialogOpen, setConfirmDialogOpen] = useState(false)
  const [rejectDialogOpen, setRejectDialogOpen] = useState(false)
  const [selectedChange, setSelectedChange] = useState(null)

  useEffect(() => {
    const fetchPendingChanges = async () => {
      try {
        const response = await fetch('/api/changes')
        if (!response.ok) {
          throw new Error('Failed to fetch pending changes')
        }
        const data = await response.json()
        setPendingChanges(data.changes)
      } catch (error) {
        console.error('Error fetching pending changes:', error)
      }
    }

    fetchPendingChanges()
  }, [role])

  const handleConfirm = async () => {
    try {
      const response = await fetch(`/api/changes/${selectedChange.id}/confirm`, {
        method: 'PUT',
      })
      if (!response.ok) {
        throw new Error('Failed to confirm change')
      }
      const data = await response.json()
      if (data.success) {
        toast({
          title: "变动已确认",
          description: `${selectedChange.name}的${selectedChange.type}申请已确认。`,
        })
        // Remove the confirmed change from the list
        setPendingChanges(pendingChanges.filter(change => change.id !== selectedChange.id))
      } else {
        throw new Error('Failed to confirm change')
      }
    } catch (error) {
      console.error('Error confirming change:', error)
      toast({
        title: "确认失败",
        description: "发生错误，请稍后重试。",
        variant: "destructive",
      })
    } finally {
      setConfirmDialogOpen(false)
      setSelectedChange(null)
    }
  }

  const handleReject = async () => {
    try {
      const response = await fetch(`/api/changes/${selectedChange.id}/reject`, {
        method: 'PUT',
      })
      if (!response.ok) {
        throw new Error('Failed to reject change')
      }
      const data = await response.json()
      if (data.success) {
        toast({
          title: "变动已拒绝",
          description: `${selectedChange.name}的${selectedChange.type}申请已拒绝。`,
        })
        // Remove the rejected change from the list
        setPendingChanges(pendingChanges.filter(change => change.id !== selectedChange.id))
      } else {
        throw new Error('Failed to reject change')
      }
    } catch (error) {
      console.error('Error rejecting change:', error)
      toast({
        title: "拒绝失败",
        description: "发生错误，请稍后重试。",
        variant: "destructive",
      })
    } finally {
      setRejectDialogOpen(false)
      setSelectedChange(null)
    }
  }

  const getChangeIcon = (type) => {
    switch (type) {
      case '入职': return <UserPlus className="text-emerald-500" />
      case '离职': return <UserMinus className="text-rose-500" />
      case '调岗': return <UserCog className="text-sky-500" />
      default: return null
    }
  }

  const getChangeBgColor = (type) => {
    switch (type) {
      case '入职': return 'bg-emerald-50'
      case '离职': return 'bg-rose-50'
      case '调岗': return 'bg-sky-50'
      default: return ''
    }
  }

  return (
    <div className="space-y-2">
      <div className="max-h-[400px] overflow-y-auto">
        {pendingChanges.map((change) => (
          <div key={change.id} className={`flex justify-between items-center p-2 rounded-lg mb-2 ${getChangeBgColor(change.type)}`}>
            <div className="flex items-center">
              {getChangeIcon(change.type)}
              <div className="ml-2">
                <p className="font-semibold text-sm">{change.name}</p>
                <p className="text-xs">
                  {change.type === '调岗' && `${change.fromCompany} → ${change.toCompany}`}
                  {change.type === '入职' && `加入 ${change.toCompany}`}
                  {change.type === '离职' && `离开 ${change.fromCompany}`}
                </p>
                <p className="text-xs text-gray-500">生效日期: {change.effectiveDate}</p>
              </div>
            </div>
            <div className="space-x-1">
              <Button 
                size="sm" 
                variant="outline" 
                className="text-xs py-1 h-7" 
                onClick={() => {
                  setSelectedChange(change)
                  setConfirmDialogOpen(true)
                }}
              >
                确认
              </Button>
              <Button 
                size="sm" 
                variant="outline" 
                className="text-xs py-1 h-7" 
                onClick={() => {
                  setSelectedChange(change)
                  setRejectDialogOpen(true)
                }}
              >
                拒绝
              </Button>
            </div>
          </div>
        ))}
      </div>

      <AlertDialog open={confirmDialogOpen} onOpenChange={setConfirmDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>确认变动</AlertDialogTitle>
            <AlertDialogDescription>
              您确定要确认 {selectedChange?.name} 的{selectedChange?.type}申请吗？
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>取消</AlertDialogCancel>
            <AlertDialogAction onClick={handleConfirm}>确认</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      <AlertDialog open={rejectDialogOpen} onOpenChange={setRejectDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>拒绝变动</AlertDialogTitle>
            <AlertDialogDescription>
              您确定要拒绝 {selectedChange?.name} 的{selectedChange?.type}申请吗？
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>取消</AlertDialogCancel>
            <AlertDialogAction onClick={handleReject}>拒绝</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  )
}

