'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { toast } from "@/components/ui/use-toast"
import { login } from '@/lib/api'

export default function LoginPage() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const router = useRouter()

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const res = await login(username, password)
      console.log('Login response:', res)
      
      if (res.token) { // 直接检查 res.token 而不是 res.success
        // token 和 user 直接从 res 中获取
        const { token, user } = res
        
        // 保存 token
        localStorage.setItem('token', token)
        
        // 保存用户信息
        localStorage.setItem('user', JSON.stringify(user))

        toast({
          title: "登录成功",
          description: `欢迎，${user.username}！`,
        })

        // 路由跳转
        router.push('/dashboard')
      } else {
        throw new Error('登录失败：未收到token')
      }
    } catch (error) {
      console.error('Login error:', error)
      toast({
        title: "登录失败",
        description: error instanceof Error ? error.message : "账号或密码错误。",
        variant: "destructive",
      })
    }
  }

  const isFormValid = username.trim() !== '' && password.trim() !== ''

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <Card className="w-[350px]">
        <CardHeader>
          <CardTitle>登录</CardTitle>
          <CardDescription>请输入您的账号和密码</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleLogin} className="space-y-4">
            <div className="space-y-2">
              <Input
                id="username"
                placeholder="账号"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Input
                id="password"
                type="password"
                placeholder="密码"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <Button 
              type="submit" 
              className="w-full" 
              disabled={!isFormValid}
            >
              登录
            </Button>
          </form>
        </CardContent>
        <CardFooter className="flex justify-center">
          <p className="text-sm text-gray-600">
            还没有账号？ 
            <Link href="/register" className="text-blue-600 hover:underline ml-1">
              立即注册
            </Link>
          </p>
        </CardFooter>
      </Card>
    </div>
  )
}

