'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

export default function RegisterPage() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [role, setRole] = useState('')
  const [company, setCompany] = useState('')
  const [project, setProject] = useState('')
  const router = useRouter()

  const [companies, setCompanies] = useState([])
  const [projects, setProjects] = useState([])

  useEffect(() => {
    // TODO: Fetch companies and projects from API
    setCompanies(['公司A', '公司B', '公司C'])
    setProjects(['项目X', '项目Y', '项目Z'])
  }, [])

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault()
    // TODO: Implement actual registration logic here
    console.log('Registering with', { username, password, role, company, project })
    router.push('/login')
  }

  const isFormValid = username.trim() !== '' && 
                      password.trim() !== '' && 
                      confirmPassword === password &&
                      role !== '' &&
                      (role === '总公司管理员' || company !== '') &&
                      (role !== '项目负责人' || project !== '')

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <Card className="w-[400px]">
        <CardHeader>
          <CardTitle>注册</CardTitle>
          <CardDescription>创建您的新账号</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleRegister} className="space-y-4">
            <Input
              placeholder="账号"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <Input
              type="password"
              placeholder="密码"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <Input
              type="password"
              placeholder="确认密码"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
            />
            <Select onValueChange={setRole}>
              <SelectTrigger>
                <SelectValue placeholder="选择角色" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="总公司管理员">总公司管理员</SelectItem>
                <SelectItem value="公司管理员">公司管理员</SelectItem>
                <SelectItem value="项目负责人">项目负责人</SelectItem>
              </SelectContent>
            </Select>
            {(role === '公司管理员' || role === '项目负责人') && (
              <Select onValueChange={setCompany}>
                <SelectTrigger>
                  <SelectValue placeholder="选择公司" />
                </SelectTrigger>
                <SelectContent>
                  {companies.map((company) => (
                    <SelectItem key={company} value={company}>{company}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            )}
            {role === '项目负责人' && (
              <Select onValueChange={setProject}>
                <SelectTrigger>
                  <SelectValue placeholder="选择项目" />
                </SelectTrigger>
                <SelectContent>
                  {projects.map((project) => (
                    <SelectItem key={project} value={project}>{project}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            )}
            <Button 
              type="submit" 
              className="w-full" 
              disabled={!isFormValid}
            >
              注册
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

