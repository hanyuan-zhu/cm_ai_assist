// lib/api.ts

import { User, Employee, PendingChange, LoginResponse, RegisterResponse, ApiResponse, Project, Company } from './types'

const API_BASE = 'http://127.0.0.1:5000/api'

// 辅助函数
const getToken = (): string | null => {
  return localStorage.getItem('token')
}

// 通用的认证请求函数
const fetchWithAuth = async (url: string, options: RequestInit = {}) => {
  const token = getToken()
  if (!token) {
    throw new Error('未登录')
  }

  const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
    ...options.headers
  }

  const response = await fetch(url, {
    ...options,
    headers
  })

  if (response.status === 401) {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    window.location.href = '/login'
    throw new Error('未授权，请重新登录')
  }

  return response
}

export async function login(username: string, password: string): Promise<LoginResponse> {
  const response = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  })
  return response.json()
}
export async function register(username: string, password: string): Promise<ApiResponse<RegisterResponse>> {
  const response = await fetch(`${API_BASE}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  })
  return response.json()
}

export async function logout(token: string): Promise<ApiResponse<null>> {
  const response = await fetch(`${API_BASE}/auth/logout`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
  })
  return response.json()
}

export async function getCurrentUser(token: string): Promise<ApiResponse<User>> {
  const response = await fetch(`${API_BASE}/users/me`, {
    headers: { 'Authorization': `Bearer ${token}` },
  })
  return response.json()
}

export async function getActiveEmployees(): Promise<{ employees: Employee[] }> {
  const response = await fetchWithAuth(`${API_BASE}/active-employees`)
  return response.json()
}

export async function getPendingChanges(): Promise<{ changes: PendingChange[] }> {
  const response = await fetchWithAuth(`${API_BASE}/pending-changes`);
  const data = await response.json();
  return data; // 直接返回 { changes: [...] }
}

export async function addEmployee(name: string, position: string, effectiveDate: string): Promise<ApiResponse<Employee>> {
  const response = await fetchWithAuth(`${API_BASE}/employees`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name,
      position,
      efffective_date: effectiveDate
    })
  })
  return response.json()
}

export async function transferEmployee(
  id: number, 
  newCompany: number,  // 应该是number而不是string
  newProject: number,  // 应该是number而不是string
  effectiveDate: string
): Promise<ApiResponse<null>> {
  const response = await fetchWithAuth(`${API_BASE}/pending-changes/${id}/transfer`, {
    method: 'PUT',
    body: JSON.stringify({ new_company: newCompany, new_project: newProject, effective_date: effectiveDate }),
  })
  return response.json()
}

export async function resignEmployee(id: number, resignDate: string): Promise<ApiResponse<null>> {
  const response = await fetchWithAuth(`${API_BASE}/pending-changes/${id}/resign`, {
    method: 'PUT',
    body: JSON.stringify({ resign_date: resignDate }),
  })
  return response.json()
}

export async function approveChange(id: number): Promise<ApiResponse<null>> {
  const response = await fetchWithAuth(`${API_BASE}/pending-changes/${id}/approve`, {
    method: 'PUT',
  })
  return response.json()
}

export async function rejectChange(id: number): Promise<ApiResponse<null>> {
  const response = await fetchWithAuth(`${API_BASE}/pending-changes/${id}/reject`, {
    method: 'PUT',
  })
  return response.json()
}

export async function getCompanies(): Promise<{ companies: Company[] }> {
  const response = await fetch(`${API_BASE}/companies`, {
    headers: { 'Content-Type': 'application/json' }
  })
  if (!response.ok) {
    throw new Error('获取公司列表失败')
  }
  return response.json()
}

export async function getProjects(companyId: number): Promise<{ projects: Project[] }> {
  const response = await fetchWithAuth(`${API_BASE}/companies/${companyId}/projects`, {
    headers: { 'Content-Type': 'application/json' }
  })
  if (!response.ok) {
    throw new Error('获取项目列表失败')
  }
  return response.json()
}