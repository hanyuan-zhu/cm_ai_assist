'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { toast } from "@/components/ui/use-toast"

export default function RegisterPage() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const router = useRouter()

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault()
    if (password !== confirmPassword) {
      toast({
        title: "密码不匹配",
        description: "请确保两次输入的密码相同。",
        variant: "destructive",
      })
      return
    }
    try {
      // TODO: Implement actual registration logic here
      console.log('Registering with', { username, password })
      
      // Simulating an API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      toast({
        title: "注册成功",
        description: "您的账号已成功创建。",
      })
      router.push('/login')
    } catch (error) {
      toast({
        title: "注册失败",
        description: "发生错误，请稍后重试。",
        variant: "destructive",
      })
    }
  }

  const isFormValid = username.trim() !== '' && 
                      password.trim() !== '' && 
                      confirmPassword === password

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <Card className="w-[350px]">
        <CardHeader>
          <CardTitle>注册</CardTitle>
          <CardDescription>创建您的新账号</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleRegister} className="space-y-4">
            <div className="space-y-2">
              <Input
                id="username"
                placeholder="账号"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
            <div className="space-y-2">
              <Input
                id="password"
                type="password"
                placeholder="密码"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <div className="space-y-2">
              <Input
                id="confirmPassword"
                type="password"
                placeholder="确认密码"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
              />
            </div>
            <Button 
              type="submit" 
              className="w-full" 
              disabled={!isFormValid}
            >
              注册
            </Button>
          </form>
        </CardContent>
        <CardFooter className="flex justify-center">
          <p className="text-sm text-gray-600">
            已有账号？ 
            <Link href="/login" className="text-blue-600 hover:underline ml-1">
              立即登录
            </Link>
          </p>
        </CardFooter>
      </Card>
    </div>
  )
}

