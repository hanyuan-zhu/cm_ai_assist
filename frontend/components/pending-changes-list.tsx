'use client'

import { useState, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import { UserPlus, UserMinus, UserCog } from 'lucide-react'
import {
  AlertDialog,
  AlertDialogContent,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogDescription,
  AlertDialogFooter,
} from "@/components/ui/alert-dialog"
import { toast } from "@/components/ui/use-toast"
import { getPendingChanges, approveChange, rejectChange } from '@/lib/api'
import { PendingChange } from '@/lib/types'

export function PendingChangesList({ role }: { role: string }) {
  const [pendingChanges, setPendingChanges] = useState<PendingChange[]>([])
  const [confirmDialogOpen, setConfirmDialogOpen] = useState(false)
  const [rejectDialogOpen, setRejectDialogOpen] = useState(false)
  const [selectedChange, setSelectedChange] = useState<PendingChange | null>(null)
  const [refresh, setRefresh] = useState(0)

  useEffect(() => {
    console.log('Component mounted, role:', role);
    
    const fetchPendingChanges = async () => {
      try {
        console.log('Fetching pending changes...');
        const response = await getPendingChanges();
        console.log('Raw API response:', response);
        
        // 直接检查 response.changes 是否存在
        if (response.changes) {
          console.log('Setting pending changes:', response.changes);
          setPendingChanges(response.changes);
        } else {
          console.error('API返回数据格式错误:', response);
        }
      } catch (error) {
        console.error('获取待处理变更失败:', error);
        toast({
          title: "获取数据失败",
          description: "请稍后重试",
          variant: "destructive",
        });
      }
    };

    fetchPendingChanges();
    
    return () => {
      console.log('Component will unmount');
    };
  }, [role, refresh]);

  const handleConfirm = async () => {
    if (!selectedChange) return
    try {
      const res = await approveChange(selectedChange.id)
      if (res.success) {
        toast({
          title: "变动已确认",
          description: `${selectedChange.employee_name}的${selectedChange.type}申请已确认。`,
        })
        setRefresh(prev => prev + 1)
      } else {
        throw new Error(res.message)
      }
    } catch (error) {
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
    if (!selectedChange) return
    try {
      const res = await rejectChange(selectedChange.id)
      if (res.success) {
        toast({
          title: "变动已拒绝",
          description: `${selectedChange.employee_name}的${selectedChange.type}申请已拒绝。`,
        })
        setPendingChanges(pendingChanges.filter(change => change.id !== selectedChange.id))
      } else {
        throw new Error(res.message)
      }
    } catch (error) {
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

  const getChangeIcon = (type: string) => {
    switch (type) {
      case '入职': return <UserPlus className="text-emerald-500" />
      case '离职': return <UserMinus className="text-rose-500" />
      case '调岗': return <UserCog className="text-sky-500" />
      default: return null
    }
  }

  const getChangeBgColor = (type: string) => {
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
        {pendingChanges.length === 0 ? (
          <div className="p-4 text-center text-gray-500">暂无待处理变更</div>
        ) : (
          pendingChanges.map((change) => (
            <div key={change.id} className={`flex justify-between items-center p-2 border-b ${getChangeBgColor(change.type)}`}>
              <div className="flex items-center">
                {getChangeIcon(change.type)}
                <span className="ml-2">
                  {change.employee_name} - {change.type}
                  {change.type === '调岗' && (
                    <span className="text-sm text-gray-500">
                      ({change.to_company_name} - {change.to_project_name})
                    </span>
                  )}
                </span>
              </div>
              <div>
                <Button size="sm" onClick={() => { setSelectedChange(change); setConfirmDialogOpen(true); }}>确认</Button>
                <Button size="sm" variant="destructive" onClick={() => { setSelectedChange(change); setRejectDialogOpen(true); }} className="ml-2">拒绝</Button>
              </div>
            </div>
          ))
        )}
      </div>

      {/* 确认对话框 */}
      <AlertDialog open={confirmDialogOpen} onOpenChange={setConfirmDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>确认变动</AlertDialogTitle>
            <AlertDialogDescription>
              你确定要确认此变动申请吗？
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <Button onClick={handleConfirm}>确认</Button>
            <Button variant="destructive" onClick={() => setConfirmDialogOpen(false)}>取消</Button>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      {/* 拒绝对话框 */}
      <AlertDialog open={rejectDialogOpen} onOpenChange={setRejectDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>拒绝变动</AlertDialogTitle>
            <AlertDialogDescription>
              你确定要拒绝此变动申请吗？
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <Button onClick={handleReject}>拒绝</Button>
            <Button variant="destructive" onClick={() => setRejectDialogOpen(false)}>取消</Button>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  )
}

