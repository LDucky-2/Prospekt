export type EligibilityRule = {
  min_ssc_gpa: number | null
  min_hsc_gpa: number | null
  combined_gpa: number | null
  second_time_allowed: boolean | null
  second_time_penalty_marks: number | null
  subject_requirements: string | null
}

export type MarkDistribution = {
  total_marks: number | null
  mcq_marks: number | null
  written_marks: number | null
  negative_marking_penalty: number | null
  pass_mark_total: number | null
  subject_breakout: string | null
}

export type SeatInfo = {
  general_seats: number | null
  quota_breakdown: string | null
}

export type ImportantDate = {
  application_start: string | null
  application_end: string | null
  admit_card_start: string | null
  exam_date: string | null
}

export type FeeStructure = {
  application_fee: number | null
  payment_methods: string | null
}

export type Unit = {
  id: number
  unit_name: string
  background: string
  total_seats: number | null
  eligibility_rule: EligibilityRule | null
  mark_distribution: MarkDistribution | null
  seat_info: SeatInfo | null
  important_date: ImportantDate | null
  fee_structure: FeeStructure | null
}

export type UnitInput = Omit<Unit, "id">

export type University = {
  id: number
  name: string
  session: string
  website_url: string | null
  overview: string
  application_start: string | null
  application_end: string | null
  admit_card_download: string | null
  exam_date: string | null
  units: Unit[]
  created_at: string
  updated_at: string
}

export type UniversityInput = Omit<University, "id" | "created_at" | "updated_at" | "units"> & {
  units: UnitInput[]
}

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(url, options)
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
  return response.json() as Promise<T>
}

async function remove(url: string): Promise<void> {
  const response = await fetch(url, { method: "DELETE" })
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
