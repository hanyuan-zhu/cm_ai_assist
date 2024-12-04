// lib/types.ts

export interface User {
  id: number
  username: string
  role: string  
}

// 员工接口需要匹配后端返回
export interface Employee {
  id: number
  name: string
  position: string
  efffective_date: string
  status: string
  company_id: number | null
  company_name: string | null
  project_id: number | null
  project_name: string | null
  creator_id: number
}

// 变动申请接口需要匹配后端返回
export interface PendingChange {
  id: number
  type: string
  employee_id: number
  employee_name: string
  from_company_id: number | null
  from_company_name: string | null
  to_company_id: number | null
  to_company_name: string | null
  from_project_id: number | null
  from_project_name: string | null
  to_project_id: number | null
  to_project_name: string | null
  effective_date: string
  status: string
  creator_id: number
}

// 公司接口
export interface Company {
  id: number
  name: string
}

// 项目接口
export interface Project {
  id: number
  name: string
  company_id: number
}

export interface LoginResponse {
  token: string
  user: {
    id: number
    username: string
  }
}

export interface RegisterResponse {
  message: string
}

// API 响应格式修正
export interface ApiSuccessResponse<T> {
  success: true
  data: T
  message?: string
}

export interface ApiErrorResponse {
  success: false
  message: string
}

export type ApiResponse<T> = ApiSuccessResponse<T> | ApiErrorResponse