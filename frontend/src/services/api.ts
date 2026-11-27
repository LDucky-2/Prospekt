export type EligibilityRule = {
  min_ssc_gpa: string | null
  min_hsc_gpa: string | null
  combined_gpa: string | null
  second_time_allowed: boolean | null
  second_time_penalty_marks: string | null
  subject_requirements: string | null
}

export type MarkDistribution = {
  total_marks: string | null
  mcq_marks: string | null
  written_marks: string | null
  negative_marking_penalty: string | null
  pass_mark_total: string | null
  subject_breakout: string | null
}

export type SeatInfo = {
  general_seats: string | null
  quota_breakdown: string | null
}

export type ImportantDate = {
  application_start: string | null
  application_end: string | null
  admit_card_start: string | null
  exam_date: string | null
}

export type FeeStructure = {
  application_fee: string | null
  payment_methods: string | null
}

export type Unit = {
  id: number
  unit_name: string
  background: string
  total_seats: string | null
  eligibility_rule: EligibilityRule | null
  mark_distribution: MarkDistribution | null
  seat_info: SeatInfo | null
  important_date: ImportantDate | null
  fee_structure: FeeStructure | null
}

export type UnitInput = Omit<Unit, "id">

export type Prospectus = {
  id: number
  university_id: number
  session: string
  overview: string
  application_start: string | null
  application_end: string | null
  admit_card_download: string | null
  exam_date: string | null
  units: Unit[]
  created_at: string
  updated_at: string
}

export type ProspectusInput = Omit<Prospectus, "id" | "university_id" | "created_at" | "updated_at" | "units"> & {
  units: UnitInput[]
}

export type University = {
  id: number
  name: string
  website_url: string | null
  prospectuses: Prospectus[]
  created_at: string
  updated_at: string
}

export type UniversityInput = Pick<University, "name" | "website_url">

export type AuthUser = {
  id: string
  email: string
  name: string
  role: "editor" | "admin"
  is_active: boolean
  last_login_at: string | null
  created_at: string
}

export type AdminUser = AuthUser

export type AdminUserPage = {
  items: AdminUser[]
  total: number
  offset: number
  limit: number
}

export type CreateEditorInput = {
  name: string
  email: string
  password: string
}

export type ActivityLog = {
  id: string
  action: string
  account_id: string | null
  account_email: string | null
  target_id: string | null
  detail: string | null
  ip_address: string | null
  user_agent: string | null
  created_at: string
}

export type ActivityLogPage = {
  items: ActivityLog[]
  total: number
  offset: number
  limit: number
}

export type LoginInput = {
  email: string
  password: string
}

const TOKEN_KEY = "prospekt_access_token"
const EXPIRY_KEY = "prospekt_access_expires"
let accessToken = sessionStorage.getItem(TOKEN_KEY)
let accessExpiresAt = Number(sessionStorage.getItem(EXPIRY_KEY) || "0")
let refreshInProgress: Promise<boolean> | null = null

function storeAccessToken(token: string, expiresIn: number) {
  // Store access-token expiry separately so stale tokens are never used after reload.
  accessToken = token
  accessExpiresAt = Date.now() + expiresIn * 1000
  sessionStorage.setItem(TOKEN_KEY, token)
  sessionStorage.setItem(EXPIRY_KEY, String(accessExpiresAt))
}

function clearAccessToken() {
  accessToken = null
  accessExpiresAt = 0
  sessionStorage.removeItem(TOKEN_KEY)
  sessionStorage.removeItem(EXPIRY_KEY)
}

async function refreshAccessToken(): Promise<boolean> {
  // Share one refresh request when several API calls detect a 401 at the same time.
  if (refreshInProgress) return refreshInProgress
  refreshInProgress = (async () => {
    try {
      const response = await fetch("/api/v1/auth/refresh", {
        method: "POST",
        credentials: "include",
      })
      if (!response.ok) return false
      const token = await response.json() as { access_token: string; expires_in: number }
      storeAccessToken(token.access_token, token.expires_in)
      return true
    } catch {
      return false
    } finally {
      refreshInProgress = null
    }
  })()
  return refreshInProgress
}

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  // Every API call adds the bearer token, refreshes once on 401, and keeps errors consistent.
  const send = () => fetch(url, {
    ...options,
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(options?.headers || {}),
      ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
    },
  })
  let response = await send()

  // A 401 refreshes once, then the request is retried with the new access token.
  if (response.status === 401 && !url.startsWith("/api/v1/auth")) {
    const refreshed = await refreshAccessToken()
    if (!refreshed) {
      clearAccessToken()
    } else {
      response = await send()
    }
  }
  if (!response.ok) {
    let message = `Request failed: ${response.status}`
    try {
      const body: { detail?: string } = await response.json()
      if (body.detail) message = body.detail
    } catch {
      // Use the HTTP status when the server does not return JSON.
    }
    throw new Error(message)
  }
  if (response.status === 204) return undefined as T
  return response.json() as Promise<T>
}

async function remove(url: string): Promise<void> {
  await request<void>(url, { method: "DELETE" })
}

export function listUniversities(): Promise<University[]> {
  return request("/api/v1/universities")
}

export function getUniversity(id: number): Promise<University> {
  return request(`/api/v1/universities/${id}`)
}

export function createUniversity(data: UniversityInput): Promise<University> {
  return request("/api/v1/universities", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
}

export function updateUniversity(id: number, data: UniversityInput): Promise<University> {
  return request(`/api/v1/universities/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
}

export function deleteUniversity(id: number): Promise<void> {
  return remove(`/api/v1/universities/${id}`)
}

export function createProspectus(universityId: number, data: ProspectusInput): Promise<Prospectus> {
  return request(`/api/v1/universities/${universityId}/prospectuses`, {
    method: "POST",
    body: JSON.stringify(data),
  })
}

export function updateProspectus(
  universityId: number,
  prospectusId: number,
  data: ProspectusInput,
): Promise<Prospectus> {
  return request(`/api/v1/universities/${universityId}/prospectuses/${prospectusId}`, {
    method: "PUT",
    body: JSON.stringify(data),
  })
}

export function deleteProspectus(universityId: number, prospectusId: number): Promise<void> {
  return remove(`/api/v1/universities/${universityId}/prospectuses/${prospectusId}`)
}

export async function login(data: LoginInput): Promise<AuthUser> {
  const response = await fetch("/api/v1/auth/login", {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
  if (!response.ok) {
    const body = await response.json().catch(() => null) as { detail?: string } | null
    throw new Error(body?.detail || `Login failed (${response.status})`)
  }
  const token = await response.json() as { access_token: string; expires_in: number }
  storeAccessToken(token.access_token, token.expires_in)
  return getCurrentUser()
}

export function getCurrentUser(): Promise<AuthUser> {
  return request<AuthUser>("/api/v1/auth/me")
}

export async function logout(): Promise<void> {
  await request<void>("/api/v1/auth/logout", { method: "POST" })
  clearAccessToken()
}

export async function restoreSession(): Promise<AuthUser | null> {
  if (accessToken && accessExpiresAt > Date.now()) {
    try {
      return await getCurrentUser()
    } catch {
      clearAccessToken()
    }
  }
  if (!(await refreshAccessToken())) return null
  try {
    return await getCurrentUser()
  } catch {
    clearAccessToken()
    return null
  }
}

export function listAdminUsers(params: {
  search?: string
  role?: string
  status?: string
  offset?: number
  limit?: number
}): Promise<AdminUserPage> {
  const query = new URLSearchParams()
  if (params.search) query.set("search", params.search)
  if (params.role) query.set("role", params.role)
  if (params.status) query.set("status", params.status)
  query.set("offset", String(params.offset ?? 0))
  query.set("limit", String(params.limit ?? 20))
  return request<AdminUserPage>(`/api/v1/admin/users?${query.toString()}`)
}

export function createEditor(data: CreateEditorInput): Promise<AdminUser> {
  return request<AdminUser>("/api/v1/admin/users", {
    method: "POST",
    body: JSON.stringify(data),
  })
}

export function changeUserRole(id: string, role: "editor" | "admin"): Promise<AdminUser> {
  return request<AdminUser>(`/api/v1/admin/users/${id}/role`, {
    method: "PATCH",
    body: JSON.stringify({ role }),
  })
}

export function changeUserStatus(id: string, isActive: boolean): Promise<AdminUser> {
  return request<AdminUser>(`/api/v1/admin/users/${id}/status`, {
    method: "PATCH",
    body: JSON.stringify({ is_active: isActive }),
  })
}

export function deleteAdminUser(id: string): Promise<void> {
  return remove(`/api/v1/admin/users/${id}`)
}

export function listActivityLogs(params: {
  search?: string
  action?: string
  ipAddress?: string
  offset?: number
  limit?: number
}): Promise<ActivityLogPage> {
  const query = new URLSearchParams()
  if (params.search) query.set("search", params.search)
  if (params.action) query.set("action", params.action)
  if (params.ipAddress) query.set("ip_address", params.ipAddress)
  query.set("offset", String(params.offset ?? 0))
  query.set("limit", String(params.limit ?? 20))
  return request<ActivityLogPage>(`/api/v1/admin/logs?${query.toString()}`)
}
// Frontend API client: authentication, university CRUD, account management and logs.
