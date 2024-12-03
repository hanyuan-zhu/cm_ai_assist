'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from "@/components/ui/button"
import { LogOut } from 'lucide-react'
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
import { logout } from '@/lib/api' // 导入 logout 函数

export function LogoutButton() {
  const [showConfirmDialog, setShowConfirmDialog] = useState(false)
  const router = useRouter()

  const handleLogout = async () => {
    const token = localStorage.getItem('token')
    if (!token) {
      toast({
        title: "登出失败",
        description: "未找到认证信息，请重新登录。",
        variant: "destructive",
      })
      return
    }

    try {
      const res = await logout(token)
      if (res.success) {
        localStorage.removeItem('token')
        toast({
          title: "登出成功",
          description: "您已成功退出登录。",
        })
        router.push('/login')
      } else {
        throw new Error(res.message || "未知错误")
      }
    } catch (error) {
      if (error instanceof Error) {
        toast({
          title: "登出失败",
          description: error.message || "发生错误，请稍后重试。",
          variant: "destructive",
        })
      }
    }
  }

  return (
    <>
      <Button 
        variant="outline" 
        onClick={() => setShowConfirmDialog(true)}
        className="flex items-center gap-2"
      >
        <LogOut size={16} />
        登出
      </Button>

      <AlertDialog open={showConfirmDialog} onOpenChange={setShowConfirmDialog}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>确认登出</AlertDialogTitle>
            <AlertDialogDescription>
              您确定要退出登录吗？
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>取消</AlertDialogCancel>
            <AlertDialogAction onClick={handleLogout}>确认登出</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  )
}

