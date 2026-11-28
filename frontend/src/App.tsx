// Main React UI: prospectus accordions, authentication and admin Users/Logs pages.
import { useEffect, useState, type FormEvent, type ReactNode } from "react"
import {
  createProspectus,
  createUniversity,
  deleteProspectus,
  deleteUniversity,
  getUniversity,
  listUniversities,
  updateProspectus,
  updateUniversity,
  login,
  logout,
  restoreSession,
  listAdminUsers,
  createEditor,
  changeUserRole,
  changeUserStatus,
  deleteAdminUser,
  listActivityLogs,
  type AdminUser,
  type ActivityLog,
  type AuthUser,
  type Prospectus,
  type ProspectusInput,
  type University,
  type UniversityInput,
  type Unit,
  type UnitInput,
} from "./services/api"

type UnitForm = {
  unit_name: string
  background: string
  total_seats: string
  min_ssc_gpa: string
  min_hsc_gpa: string
  combined_gpa: string
  second_time_allowed: string
  second_time_penalty_marks: string
  subject_requirements: string
  total_marks: string
  mcq_marks: string
  written_marks: string
  negative_marking_penalty: string
  pass_mark_total: string
  subject_breakout: string
  general_seats: string
  quota_breakdown: string
  application_start: string
  application_end: string
  admit_card_start: string
  exam_date: string
  application_fee: string
  payment_methods: string
}

type FormValues = {
  name: string
  website_url: string
  session: string
  overview: string
  application_start: string
  application_end: string
  admit_card_download: string
  exam_date: string
  units: UnitForm[]
}

const emptyUnit: UnitForm = {
  unit_name: "",
  background: "",
  total_seats: "",
  min_ssc_gpa: "",
  min_hsc_gpa: "",
  combined_gpa: "",
  second_time_allowed: "",
  second_time_penalty_marks: "",
  subject_requirements: "",
  total_marks: "",
  mcq_marks: "",
  written_marks: "",
  negative_marking_penalty: "",
  pass_mark_total: "",
  subject_breakout: "",
  general_seats: "",
  quota_breakdown: "",
  application_start: "",
  application_end: "",
  admit_card_start: "",
  exam_date: "",
  application_fee: "",
  payment_methods: "",
}

const emptyForm: FormValues = {
  name: "",
  website_url: "",
  session: "",
  overview: "",
  application_start: "",
  application_end: "",
  admit_card_download: "",
  exam_date: "",
  units: [],
}

function toUnitForm(unit: Unit): UnitForm {
  return {
    ...emptyUnit,
    unit_name: unit.unit_name,
    background: unit.background,
    total_seats: unit.total_seats?.toString() ?? "",
    min_ssc_gpa: unit.eligibility_rule?.min_ssc_gpa?.toString() ?? "",
    min_hsc_gpa: unit.eligibility_rule?.min_hsc_gpa?.toString() ?? "",
    combined_gpa: unit.eligibility_rule?.combined_gpa?.toString() ?? "",
    second_time_allowed: unit.eligibility_rule?.second_time_allowed?.toString() ?? "",
    second_time_penalty_marks: unit.eligibility_rule?.second_time_penalty_marks?.toString() ?? "",
    subject_requirements: unit.eligibility_rule?.subject_requirements ?? "",
    total_marks: unit.mark_distribution?.total_marks?.toString() ?? "",
    mcq_marks: unit.mark_distribution?.mcq_marks?.toString() ?? "",
    written_marks: unit.mark_distribution?.written_marks?.toString() ?? "",
    negative_marking_penalty: unit.mark_distribution?.negative_marking_penalty?.toString() ?? "",
    pass_mark_total: unit.mark_distribution?.pass_mark_total?.toString() ?? "",
    subject_breakout: unit.mark_distribution?.subject_breakout ?? "",
    general_seats: unit.seat_info?.general_seats?.toString() ?? "",
    quota_breakdown: unit.seat_info?.quota_breakdown ?? "",
    application_start: unit.important_date?.application_start ?? "",
    application_end: unit.important_date?.application_end ?? "",
    admit_card_start: unit.important_date?.admit_card_start ?? "",
    exam_date: unit.important_date?.exam_date ?? "",
    application_fee: unit.fee_structure?.application_fee?.toString() ?? "",
    payment_methods: unit.fee_structure?.payment_methods ?? "",
  }
}

function toUniversityForm(university: University): FormValues {
  return {
    name: university.name,
    website_url: university.website_url ?? "",
    session: "",
    overview: "",
    application_start: "",
    application_end: "",
    admit_card_download: "",
    exam_date: "",
    units: [],
  }
}

function toProspectusForm(prospectus: Prospectus): FormValues {
  return {
    name: "",
    session: prospectus.session,
    website_url: "",
    overview: prospectus.overview,
    application_start: prospectus.application_start ?? "",
    application_end: prospectus.application_end ?? "",
    admit_card_download: prospectus.admit_card_download ?? "",
    exam_date: prospectus.exam_date ?? "",
    units: prospectus.units.map(toUnitForm),
  }
}

function optionalText(value: string): string | null {
  return value.trim() ? value : null
}

function toUnitInput(form: UnitForm): UnitInput {
  return {
    unit_name: form.unit_name,
    background: form.background,
    total_seats: optionalText(form.total_seats),
    eligibility_rule: {
      min_ssc_gpa: optionalText(form.min_ssc_gpa),
      min_hsc_gpa: optionalText(form.min_hsc_gpa),
      combined_gpa: optionalText(form.combined_gpa),
      second_time_allowed: form.second_time_allowed ? form.second_time_allowed === "true" : null,
      second_time_penalty_marks: optionalText(form.second_time_penalty_marks),
      subject_requirements: form.subject_requirements.trim() || null,
    },
    mark_distribution: {
      total_marks: optionalText(form.total_marks),
      mcq_marks: optionalText(form.mcq_marks),
      written_marks: optionalText(form.written_marks),
      negative_marking_penalty: optionalText(form.negative_marking_penalty),
      pass_mark_total: optionalText(form.pass_mark_total),
      subject_breakout: form.subject_breakout.trim() || null,
    },
    seat_info: {
      general_seats: optionalText(form.general_seats),
      quota_breakdown: form.quota_breakdown.trim() || null,
    },
    important_date: {
      application_start: form.application_start || null,
      application_end: form.application_end || null,
      admit_card_start: form.admit_card_start || null,
      exam_date: form.exam_date || null,
    },
    fee_structure: {
      application_fee: optionalText(form.application_fee),
      payment_methods: form.payment_methods.trim() || null,
    },
  }
}

function toUniversityInput(form: FormValues): UniversityInput {
  return {
    name: form.name,
    website_url: form.website_url.trim() || null,
  }
}

function toProspectusInput(form: FormValues): ProspectusInput {
  return {
    session: form.session,
    overview: form.overview,
    application_start: form.application_start || null,
    application_end: form.application_end || null,
    admit_card_download: form.admit_card_download || null,
    exam_date: form.exam_date || null,
    units: form.units.map(toUnitInput),
  }
}

function Field({
  id,
  label,
  value,
  onChange,
  type = "text",
  placeholder,
  required = false,
  maxLength,
  multiline = false,
  rows = 3,
}: {
  id: string
  label: string
  value: string
  onChange: (value: string) => void
  type?: string
  placeholder?: string
  required?: boolean
  maxLength?: number
  multiline?: boolean
  rows?: number
}) {
  return (
    <div className="field">
      <label htmlFor={id}>{label}</label>
      {multiline ? (
        <textarea
          id={id}
          value={value}
          onChange={(event) => onChange(event.target.value)}
          placeholder={placeholder}
          maxLength={maxLength}
          rows={rows}
          required={required}
        />
      ) : (
        <input
          id={id}
          type={type}
          value={value}
          onChange={(event) => onChange(event.target.value)}
          placeholder={placeholder}
          maxLength={maxLength}
          required={required}
        />
      )}
    </div>
  )
}

function DetailSection({ title, entries }: { title: string; entries: [string, ReactNode][] }) {
  return (
    <section className="unit-detail-section">
      <h4>{title}</h4>
      <dl className="details-list">
        {entries.map(([label, value]) => (
          <div key={label}>
            <dt>{label}</dt>
            <dd>{value ?? "Not provided"}</dd>
          </div>
        ))}
      </dl>
    </section>
  )
}

export default function App() {
  // Top-level state separates prospectus browsing, record editing and admin pages.
  const [universities, setUniversities] = useState<University[]>([])
  const [authUser, setAuthUser] = useState<AuthUser | null>(null)
  const [authLoading, setAuthLoading] = useState(true)
  const [loginEmail, setLoginEmail] = useState("")
  const [loginPassword, setLoginPassword] = useState("")
  const [loginError, setLoginError] = useState("")
  const [selectedUniversity, setSelectedUniversity] = useState<University | null>(null)
  const [selectedProspectus, setSelectedProspectus] = useState<Prospectus | null>(null)
  const [form, setForm] = useState<FormValues>(emptyForm)
  const [editing, setEditing] = useState<"university" | "prospectus" | null>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState("")
  const [page, setPage] = useState<"prospectuses" | "users" | "logs" | "editor">("prospectuses")
  const [adminUsers, setAdminUsers] = useState<AdminUser[]>([])
  const [adminSearch, setAdminSearch] = useState("")
  const [adminRole, setAdminRole] = useState("")
  const [adminStatus, setAdminStatus] = useState("")
  const [adminLoading, setAdminLoading] = useState(false)
  const [editorForm, setEditorForm] = useState({ name: "", email: "", password: "" })
  const [activityLogs, setActivityLogs] = useState<ActivityLog[]>([])
  const [logSearch, setLogSearch] = useState("")
  const [logAction, setLogAction] = useState("")
  const [logIpAddress, setLogIpAddress] = useState("")
  const [logLoading, setLogLoading] = useState(false)

  useEffect(() => {
    // Restore the session before rendering authenticated controls, avoiding guest-content flashes.
    void restoreSession()
      .then(setAuthUser)
      .finally(() => setAuthLoading(false))
    void loadUniversities()
  }, [])

  async function handleLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setLoginError("")
    try {
      const user = await login({ email: loginEmail, password: loginPassword })
      setAuthUser(user)
      setLoginPassword("")
    } catch (err) {
      setLoginEmail("")
      setLoginPassword("")
      setLoginError(err instanceof Error ? err.message : "Could not log in.")
    }
  }

  async function handleLogout() {
    try {
      await logout()
    } finally {
      setAuthUser(null)
      setEditing(null)
      setSelectedProspectus(null)
      setPage("prospectuses")
    }
  }

  async function loadAdminUsers() {
    // Reload the Users table after filters or account actions change server state.
    setAdminLoading(true)
    setError("")
    try {
      const result = await listAdminUsers({
        search: adminSearch,
        role: adminRole,
        status: adminStatus,
      })
      setAdminUsers(result.items)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not load users.")
    } finally {
      setAdminLoading(false)
    }
  }

  async function loadActivityLogs() {
    // Search and filter parameters are sent to the server for the Logs table.
    setLogLoading(true)
    setError("")
    try {
      const result = await listActivityLogs({
        search: logSearch,
        action: logAction,
        ipAddress: logIpAddress,
      })
      setActivityLogs(result.items)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not load logs.")
    } finally {
      setLogLoading(false)
    }
  }

  async function handleCreateEditor(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError("")
    if (editorForm.password.length < 8) {
      setError("Temporary password must be at least 8 characters.")
      return
    }
    try {
      await createEditor(editorForm)
      setEditorForm({ name: "", email: "", password: "" })
      await loadAdminUsers()
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not create editor.")
    }
  }

  async function loadUniversities(preferredId?: number) {
    setLoading(true)
    setError("")
    try {
      const records = await listUniversities()
      setUniversities(records)
      const nextId = preferredId ?? records[0]?.id
      if (nextId === undefined) {
        setSelectedUniversity(null)
        setSelectedProspectus(null)
        return
      }
      const university = await getUniversity(nextId)
      setSelectedUniversity(university)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not load prospectuses.")
    } finally {
      setLoading(false)
    }
  }

  function startNewUniversity() {
    setSelectedUniversity(null)
    setSelectedProspectus(null)
    setForm(emptyForm)
    setEditing("university")
    setError("")
    setPage("editor")
  }

  function startNewProspectus(university: University) {
    setSelectedUniversity(university)
    setSelectedProspectus(null)
    setForm(emptyForm)
    setEditing("prospectus")
    setError("")
    setPage("editor")
  }

  function startEditingUniversity(university: University) {
    setSelectedUniversity(university)
    setSelectedProspectus(null)
    setForm(toUniversityForm(university))
    setEditing("university")
    setError("")
    setPage("editor")
  }

  function startEditingProspectus(university: University, prospectus: Prospectus) {
    setSelectedUniversity(university)
    setSelectedProspectus(prospectus)
    setForm(toProspectusForm(prospectus))
    setEditing("prospectus")
    setError("")
    setPage("editor")
  }

  function cancelEditor() {
    setEditing(null)
    setSelectedProspectus(null)
    setForm(emptyForm)
    setPage("prospectuses")
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setSaving(true)
    setError("")
    try {
      if (editing === "university") {
        const university = selectedUniversity
          ? await updateUniversity(selectedUniversity.id, toUniversityInput(form))
          : await createUniversity(toUniversityInput(form))
        setSelectedUniversity(university)
        setSelectedProspectus(null)
        setEditing(null)
        setPage("prospectuses")
        await loadUniversities(university.id)
      } else if (editing === "prospectus" && selectedUniversity) {
        if (selectedProspectus) {
          await updateProspectus(
            selectedUniversity.id,
            selectedProspectus.id,
            toProspectusInput(form),
          )
        } else {
          await createProspectus(selectedUniversity.id, toProspectusInput(form))
        }
        setEditing(null)
        setSelectedProspectus(null)
        setPage("prospectuses")
        await loadUniversities(selectedUniversity.id)
      } else {
        throw new Error("Select a university before saving a prospectus.")
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not save this prospectus.")
    } finally {
      setSaving(false)
    }
  }

  async function handleDeleteUniversity(university: University) {
    if (!window.confirm(`Delete ${university.name} and all its prospectuses?`)) return
    setError("")
    try {
      await deleteUniversity(university.id)
      if (selectedUniversity?.id === university.id) {
        setSelectedUniversity(null)
        setSelectedProspectus(null)
      }
      await loadUniversities()
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not delete this university.")
    }
  }

  async function handleDeleteProspectus(university: University, prospectus: Prospectus) {
    if (!window.confirm(`Delete the ${prospectus.session} prospectus for ${university.name}?`)) return
    setError("")
    try {
      await deleteProspectus(university.id, prospectus.id)
      await loadUniversities(university.id)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not delete this prospectus.")
    }
  }

  function updateField(field: keyof FormValues, value: string) {
    setForm((current) => ({ ...current, [field]: value }))
  }

  function updateUnit(index: number, field: keyof UnitForm, value: string) {
    setForm((current) => ({
      ...current,
      units: current.units.map((unit, unitIndex) =>
        unitIndex === index ? { ...unit, [field]: value } : unit,
      ),
    }))
  }

  function addUnit() {
    setForm((current) => ({ ...current, units: [...current.units, { ...emptyUnit }] }))
  }

  function removeUnit(index: number) {
    setForm((current) => ({
      ...current,
      units: current.units.filter((_, unitIndex) => unitIndex !== index),
    }))
  }

  const isEditingExisting =
    (editing === "university" && selectedUniversity !== null) ||
    (editing === "prospectus" && selectedProspectus !== null)

  return (
    <main className="page-shell">
      <header className="topbar panel">
        <div>
          <p className="eyebrow">Admission information manager</p>
          <h1>Prospekt</h1>
        </div>
        <div className="topbar-right">
          {authLoading ? (
            <span className="chip">Restoring session...</span>
          ) : authUser ? (
            <>
              {authUser.role === "admin" && (
                <>
                  <button
                    type="button"
                    className={page === "prospectuses" ? "secondary-button" : undefined}
                    onClick={cancelEditor}
                  >
                    Prospectuses
                  </button>
                  <button
                    type="button"
                    className={page === "users" ? "secondary-button" : undefined}
                    onClick={() => {
                      cancelEditor()
                      setPage("users")
                      void loadAdminUsers()
                    }}
                  >
                    Users
                  </button>
                  <button
                    type="button"
                    className={page === "logs" ? "secondary-button" : undefined}
                    onClick={() => {
                      cancelEditor()
                      setPage("logs")
                      void loadActivityLogs()
                    }}
                  >
                    Logs
                  </button>
                </>
              )}
              <span className="chip">{authUser.name} ({authUser.role})</span>
              <button type="button" onClick={() => void handleLogout()}>Log out</button>
            </>
          ) : (
            <form className="auth-inline" onSubmit={(event) => void handleLogin(event)}>
              <input
                aria-label="Email"
                type="email"
                placeholder="Email"
                value={loginEmail}
                onChange={(event) => setLoginEmail(event.target.value)}
                required
              />
              <input
                aria-label="Password"
                type="password"
                placeholder="Password"
                value={loginPassword}
                onChange={(event) => setLoginPassword(event.target.value)}
                required
              />
              <button type="submit">Log in</button>
            </form>
          )}
        </div>
      </header>

      {loginError && <p className="notice error" role="alert">{loginError}</p>}

      {error && <p className="notice error" role="alert">{error}</p>}

      {page === "prospectuses" ? (
      <section className="accordion-layout">
        <div className="accordion-toolbar">
          <div>
            <p className="eyebrow">Admission prospectuses</p>
            <h2>Universities</h2>
          </div>
          {authUser?.role === "admin" && (
            <button type="button" onClick={startNewUniversity}>New university</button>
          )}
        </div>

        {loading ? (
          <p className="panel state-message">Loading universities...</p>
        ) : universities.length === 0 ? (
          <p className="panel state-message">No universities have been added yet.</p>
        ) : (
          <div className="university-accordions">
            {/* University -> prospectus -> unit is intentionally nested to keep information compact. */}
            {universities.map((university, universityIndex) => (
              <details className="university-accordion" key={university.id} open={universityIndex === 0}>
                <summary>
                  <span>
                    <strong>{university.name}</strong>
                    <small>{university.prospectuses.length} prospectus{university.prospectuses.length === 1 ? "" : "es"}</small>
                  </span>
                </summary>

                <div className="university-actions">
                  {authUser && (
                    <div className="button-row">
                      <button type="button" onClick={() => startNewProspectus(university)}>
                        Add prospectus
                      </button>
                      <button type="button" onClick={() => startEditingUniversity(university)}>
                        Edit university
                      </button>
                      <button
                        className="danger-button"
                        type="button"
                        onClick={() => void handleDeleteUniversity(university)}
                      >
                        Delete university
                      </button>
                    </div>
                  )}
                </div>

                {university.prospectuses.length === 0 ? (
                  <p className="empty-message">No prospectuses have been added to this university.</p>
                ) : university.prospectuses.map((prospectus) => (
                  <details className="prospectus-accordion" key={prospectus.id}>
                    <summary>Admission session {prospectus.session}</summary>
                    <div className="prospectus-content">
                      {authUser && (
                        <div className="button-row">
                          <button
                            type="button"
                            onClick={() => startEditingProspectus(university, prospectus)}
                          >
                            Edit prospectus
                          </button>
                          <button
                            className="danger-button"
                            type="button"
                            onClick={() => void handleDeleteProspectus(university, prospectus)}
                          >
                            Delete prospectus
                          </button>
                        </div>
                      )}
                      <DetailSection title="Prospectus information" entries={[
                        ["Official website", university.website_url ? (
                          <a href={university.website_url} target="_blank" rel="noreferrer">
                            {university.website_url}
                          </a>
                        ) : null],
                        ["Overview", prospectus.overview || "Not provided"],
                      ]} />
                      <DetailSection title="Prospectus-wide schedule" entries={[
                        ["Application opens", prospectus.application_start],
                        ["Application closes", prospectus.application_end],
                        ["Admit card download", prospectus.admit_card_download],
                        ["Admission exam", prospectus.exam_date],
                      ]} />

                      <div className="unit-accordions">
                      <h3>Units ({prospectus.units.length})</h3>
                      {prospectus.units.length === 0 ? (
                        <p className="empty-message">No units have been added to this prospectus.</p>
                      ) : prospectus.units.map((unit) => (
                        <details className="unit-accordion" key={unit.id}>
                          <summary>
                            <span>{unit.unit_name}</span>
                            <small>{unit.background}</small>
                          </summary>
                          <div className="unit-content">
                            <DetailSection title="Unit information" entries={[
                              ["Background", unit.background],
                              ["Total seats", unit.total_seats],
                            ]} />
                            <DetailSection title="Eligibility rules" entries={[
                              ["Minimum SSC GPA", unit.eligibility_rule?.min_ssc_gpa],
                              ["Minimum HSC GPA", unit.eligibility_rule?.min_hsc_gpa],
                              ["Combined GPA", unit.eligibility_rule?.combined_gpa],
                              ["Second-time applicants", unit.eligibility_rule?.second_time_allowed === null
                                ? null
                                : unit.eligibility_rule?.second_time_allowed ? "Allowed" : "Not allowed"],
                              ["Second-time penalty marks", unit.eligibility_rule?.second_time_penalty_marks],
                              ["Subject requirements", unit.eligibility_rule?.subject_requirements],
                            ]} />
                            <DetailSection title="Mark distribution" entries={[
                              ["Total marks", unit.mark_distribution?.total_marks],
                              ["MCQ marks", unit.mark_distribution?.mcq_marks],
                              ["Written marks", unit.mark_distribution?.written_marks],
                              ["Negative marking penalty", unit.mark_distribution?.negative_marking_penalty],
                              ["Pass mark", unit.mark_distribution?.pass_mark_total],
                              ["Subject breakdown", unit.mark_distribution?.subject_breakout],
                            ]} />
                            <DetailSection title="Seat information" entries={[
                              ["General seats", unit.seat_info?.general_seats],
                              ["Quota breakdown", unit.seat_info?.quota_breakdown],
                            ]} />
                            <DetailSection title="Important dates" entries={[
                              ["Application opens", unit.important_date?.application_start],
                              ["Application closes", unit.important_date?.application_end],
                              ["Admit card available", unit.important_date?.admit_card_start],
                              ["Admission exam", unit.important_date?.exam_date],
                            ]} />
                            <DetailSection title="Fee structure" entries={[
                              ["Application fee", unit.fee_structure?.application_fee],
                              ["Payment methods", unit.fee_structure?.payment_methods],
                            ]} />
                          </div>
                        </details>
                      ))}
                      </div>
                    </div>
                  </details>
                ))}
              </details>
            ))}
          </div>
        )}
      </section>
      ) : page === "users" ? (
        <section className="panel admin-users-page">
          {/* This page is available only to admins; account actions are also enforced by the API. */}
          <div className="section-heading">
            <div>
              <p className="eyebrow">Account management</p>
              <h2>Admins and editors</h2>
            </div>
          </div>

          <form className="editor-create-form" onSubmit={(event) => void handleCreateEditor(event)}>
            <h3>Create editor account</h3>
            <Field id="editor-name" label="Name" value={editorForm.name} onChange={(value) => setEditorForm((current) => ({ ...current, name: value }))} required />
            <Field id="editor-email" label="Email" type="email" value={editorForm.email} onChange={(value) => setEditorForm((current) => ({ ...current, email: value }))} required />
            <Field id="editor-password" label="Temporary password (at least 8 characters)" type="password" value={editorForm.password} onChange={(value) => setEditorForm((current) => ({ ...current, password: value }))} required />
            <button type="submit">Create editor</button>
          </form>

          <div className="admin-user-filters">
            <Field id="admin-search" label="Search" value={adminSearch} onChange={setAdminSearch} />
            <div className="field">
              <label htmlFor="admin-role">Role</label>
              <select id="admin-role" value={adminRole} onChange={(event) => setAdminRole(event.target.value)}>
                <option value="">All roles</option>
                <option value="admin">Admin</option>
                <option value="editor">Editor</option>
              </select>
            </div>
            <div className="field">
              <label htmlFor="admin-status">Status</label>
              <select id="admin-status" value={adminStatus} onChange={(event) => setAdminStatus(event.target.value)}>
                <option value="">All statuses</option>
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
              </select>
            </div>
            <button type="button" onClick={() => void loadAdminUsers()} disabled={adminLoading}>
              {adminLoading ? "Loading..." : "Apply filters"}
            </button>
          </div>

          <div className="admin-user-table-wrap">
            <table className="admin-user-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Role</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {adminUsers.map((user) => (
                  <tr key={user.id}>
                    <td>{user.name}</td>
                    <td>{user.email}</td>
                    <td>
                      <select
                        aria-label={`Role for ${user.name}`}
                        value={user.role}
                        disabled={user.id === authUser?.id}
                        onChange={(event) => {
                          void changeUserRole(user.id, event.target.value as "editor" | "admin")
                            .then(loadAdminUsers)
                            .catch((err: unknown) => setError(err instanceof Error ? err.message : "Could not change role"))
                        }}
                      >
                        <option value="editor">Editor</option>
                        <option value="admin">Admin</option>
                      </select>
                    </td>
                    <td>
                      <span className={user.is_active ? "status-active" : "status-inactive"}>
                        {user.is_active ? "Active" : "Inactive"}
                      </span>
                    </td>
                    <td>
                      <div className="button-row">
                        <button
                          type="button"
                          className="secondary-button"
                          disabled={user.id === authUser?.id}
                          onClick={() => {
                            void changeUserStatus(user.id, !user.is_active)
                              .then(loadAdminUsers)
                              .catch((err: unknown) => setError(err instanceof Error ? err.message : "Could not change status"))
                          }}
                        >
                          {user.is_active ? "Deactivate" : "Reactivate"}
                        </button>
                        <button
                          type="button"
                          className="danger-button"
                          disabled={user.id === authUser?.id}
                          title={user.id === authUser?.id ? "You cannot delete the account you are currently signed into." : undefined}
                          onClick={() => {
                            if (!window.confirm(`Delete ${user.name}'s account?`)) return
                            void deleteAdminUser(user.id)
                              .then(loadAdminUsers)
                              .catch((err: unknown) => setError(err instanceof Error ? err.message : "Could not delete account"))
                          }}
                        >
                          Delete
                        </button>
                      </div>
                      {user.id === authUser?.id && (
                        <small className="account-self-action-note">Sign in with another admin account to delete this one.</small>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {!adminLoading && adminUsers.length === 0 && (
              <p className="empty-message">No matching accounts found.</p>
            )}
          </div>
        </section>
      ) : page === "logs" ? (
        <section className="panel admin-logs-page">
          {/* Audit entries show account, network, browser and action context for admins. */}
          <div className="section-heading">
            <div>
              <p className="eyebrow">Audit and security</p>
              <h2>Logs</h2>
            </div>
          </div>

          <div className="admin-log-filters">
            <Field id="log-search" label="Search" value={logSearch} onChange={setLogSearch} />
            <div className="field">
              <label htmlFor="log-action">Action</label>
              <select id="log-action" value={logAction} onChange={(event) => setLogAction(event.target.value)}>
                <option value="">All actions</option>
                <option value="login_success">Successful login</option>
                <option value="login_failed">Failed login</option>
                <option value="logout">Logout</option>
                <option value="password_change">Password change</option>
                <option value="account_created">Account created</option>
                <option value="account_deleted">Account deleted</option>
                <option value="account_activated">Account activated</option>
                <option value="account_deactivated">Account deactivated</option>
                <option value="role_promoted">Role promoted</option>
                <option value="role_demoted">Role demoted</option>
                <option value="university_created">University created</option>
                <option value="university_updated">University updated</option>
                <option value="university_deleted">University deleted</option>
                <option value="access_denied">Access denied</option>
              </select>
            </div>
            <Field id="log-ip" label="IP address" value={logIpAddress} onChange={setLogIpAddress} />
            <button type="button" onClick={() => void loadActivityLogs()} disabled={logLoading}>
              {logLoading ? "Loading..." : "Apply filters"}
            </button>
          </div>

          <div className="admin-log-table-wrap">
            <table className="admin-log-table">
              <thead>
                <tr>
                  <th>Time</th>
                  <th>Action</th>
                  <th>Account</th>
                  <th>IP address</th>
                  <th>Browser</th>
                  <th>Details</th>
                </tr>
              </thead>
              <tbody>
                {activityLogs.map((entry) => (
                  <tr key={entry.id}>
                    <td>{new Date(entry.created_at).toLocaleString()}</td>
                    <td><span className="log-action">{entry.action.replaceAll("_", " ")}</span></td>
                    <td>{entry.account_email || "Unknown"}</td>
                    <td>{entry.ip_address || "Unknown"}</td>
                    <td className="user-agent">{entry.user_agent || "Unknown"}</td>
                    <td>{entry.detail || "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            {!logLoading && activityLogs.length === 0 && (
              <p className="empty-message">No matching log entries found.</p>
            )}
          </div>
        </section>
      ) : (
      <section className="main-column">

          {authUser &&
            ((editing === "university" &&
              (selectedUniversity !== null || authUser.role === "admin")) ||
              (editing === "prospectus" && selectedUniversity !== null)) && (
            <section className="panel form-panel">
              <p className="eyebrow">{isEditingExisting ? "Update record" : "Create record"}</p>
              <h2>
                {editing === "university"
                  ? isEditingExisting ? "Edit university" : "New university"
                  : isEditingExisting ? "Edit prospectus" : "New prospectus"}
              </h2>
              <form className="record-form" onSubmit={(event) => void handleSubmit(event)}>
                <fieldset className="form-section">
                  <legend>{editing === "university" ? "University information" : "Prospectus information"}</legend>
                  {editing === "university" ? (
                    <>
                      <Field
                        id="name"
                        label="University name"
                        value={form.name}
                        onChange={(value) => updateField("name", value)}
                        maxLength={150}
                        required
                      />
                      <Field
                        id="website_url"
                        label="Official website URL"
                        value={form.website_url}
                        onChange={(value) => updateField("website_url", value)}
                        type="url"
                      />
                    </>
                  ) : (
                    <>
                      <Field
                        id="session"
                        label="Admission session"
                        value={form.session}
                        onChange={(value) => updateField("session", value)}
                        maxLength={20}
                        placeholder="e.g. 2026-2027"
                        required
                      />
                      <Field
                        id="overview"
                        label="Overview"
                        value={form.overview}
                        onChange={(value) => updateField("overview", value)}
                        maxLength={2000}
                        multiline
                        required
                      />
                    </>
                  )}
                </fieldset>

                {editing === "prospectus" && (
                <fieldset className="form-section">
                  <legend>Prospectus-wide schedule (optional)</legend>
                  <p className="section-help">Each unit can have its own dates below.</p>
                  <Field id="university_application_start" label="Application opens" type="date" value={form.application_start} onChange={(value) => updateField("application_start", value)} />
                  <Field id="university_application_end" label="Application closes" type="date" value={form.application_end} onChange={(value) => updateField("application_end", value)} />
                  <Field id="university_admit_card_download" label="Admit card download" type="date" value={form.admit_card_download} onChange={(value) => updateField("admit_card_download", value)} />
                  <Field id="university_exam_date" label="Admission exam" type="date" value={form.exam_date} onChange={(value) => updateField("exam_date", value)} />
                </fieldset>
                )}

                {editing === "prospectus" && (
                <fieldset className="form-section">
                  <legend>Prospectus units</legend>
                  <p className="section-help">Each unit has its own eligibility rules, marks, seats, dates, and fees.</p>
                  {form.units.length === 0 && <p>No units added yet.</p>}
                  {form.units.map((unit, index) => {
                    const field = (name: keyof UnitForm) =>
                      (value: string) => updateUnit(index, name, value)
                    return (
                      <fieldset className="unit-form-card" key={index}>
                        <legend>Unit {index + 1}</legend>
                        <div className="section-heading">
                          <h3>{unit.unit_name || `Unit ${index + 1}`}</h3>
                          <button type="button" className="danger-button" onClick={() => removeUnit(index)}>
                            Remove unit
                          </button>
                        </div>
                        <Field id={`unit_name_${index}`} label="Unit name" value={unit.unit_name} onChange={field("unit_name")} placeholder="e.g. A Unit" required />
                        <div className="field">
                          <label htmlFor={`background_${index}`}>Background</label>
                          <select
                            id={`background_${index}`}
                            value={unit.background}
                            onChange={(event) => field("background")(event.target.value)}
                            required
                          >
                            <option value="">Select a background</option>
                            <option value="Science">Science</option>
                            <option value="Arts">Arts</option>
                            <option value="Commerce">Commerce</option>
                            <option value="All">All backgrounds</option>
                          </select>
                        </div>
                        <Field id={`total_seats_${index}`} label="Total seats" value={unit.total_seats} onChange={field("total_seats")} />

                        <fieldset className="nested-form-section">
                          <legend>Eligibility rules</legend>
                          <Field id={`min_ssc_gpa_${index}`} label="Minimum SSC GPA" value={unit.min_ssc_gpa} onChange={field("min_ssc_gpa")} />
                          <Field id={`min_hsc_gpa_${index}`} label="Minimum HSC GPA" value={unit.min_hsc_gpa} onChange={field("min_hsc_gpa")} />
                          <Field id={`combined_gpa_${index}`} label="Combined GPA" value={unit.combined_gpa} onChange={field("combined_gpa")} />
                          <div className="field">
                            <label htmlFor={`second_time_allowed_${index}`}>Second-time applicants</label>
                            <select
                              id={`second_time_allowed_${index}`}
                              value={unit.second_time_allowed}
                              onChange={(event) => field("second_time_allowed")(event.target.value)}
                            >
                              <option value="">Not specified</option>
                              <option value="true">Allowed</option>
                              <option value="false">Not allowed</option>
                            </select>
                          </div>
                          <Field id={`second_time_penalty_marks_${index}`} label="Second-time penalty marks" value={unit.second_time_penalty_marks} onChange={field("second_time_penalty_marks")} />
                          <Field id={`subject_requirements_${index}`} label="Subject requirements" value={unit.subject_requirements} onChange={field("subject_requirements")} multiline />
                        </fieldset>

                        <fieldset className="nested-form-section">
                          <legend>Mark distribution</legend>
                          <Field id={`total_marks_${index}`} label="Total marks" value={unit.total_marks} onChange={field("total_marks")} />
                          <Field id={`mcq_marks_${index}`} label="MCQ marks" value={unit.mcq_marks} onChange={field("mcq_marks")} />
                          <Field id={`written_marks_${index}`} label="Written marks" value={unit.written_marks} onChange={field("written_marks")} />
                          <Field id={`negative_marking_penalty_${index}`} label="Negative marking penalty" value={unit.negative_marking_penalty} onChange={field("negative_marking_penalty")} />
                          <Field id={`pass_mark_total_${index}`} label="Pass mark" value={unit.pass_mark_total} onChange={field("pass_mark_total")} />
                          <Field id={`subject_breakout_${index}`} label="Subject mark breakdown" value={unit.subject_breakout} onChange={field("subject_breakout")} placeholder="e.g. English 30 marks, General Knowledge 20 marks" multiline />
                        </fieldset>

                        <fieldset className="nested-form-section">
                          <legend>Seat information</legend>
                          <Field id={`general_seats_${index}`} label="General seats" value={unit.general_seats} onChange={field("general_seats")} />
                          <Field id={`quota_breakdown_${index}`} label="Seat quota breakdown" value={unit.quota_breakdown} onChange={field("quota_breakdown")} placeholder="e.g. Freedom Fighter: 5 seats, Tribal: 3 seats" multiline />
                        </fieldset>

                        <fieldset className="nested-form-section">
                          <legend>Important dates</legend>
                          <Field id={`unit_application_start_${index}`} label="Application opens" type="date" value={unit.application_start} onChange={field("application_start")} />
                          <Field id={`unit_application_end_${index}`} label="Application closes" type="date" value={unit.application_end} onChange={field("application_end")} />
                          <Field id={`unit_admit_card_start_${index}`} label="Admit card available" type="date" value={unit.admit_card_start} onChange={field("admit_card_start")} />
                          <Field id={`unit_exam_date_${index}`} label="Admission exam" type="date" value={unit.exam_date} onChange={field("exam_date")} />
                        </fieldset>

                        <fieldset className="nested-form-section">
                          <legend>Fee structure</legend>
                          <Field id={`application_fee_${index}`} label="Application fee" value={unit.application_fee} onChange={field("application_fee")} />
                          <Field id={`payment_methods_${index}`} label="Payment methods and instructions" value={unit.payment_methods} onChange={field("payment_methods")} multiline />
                        </fieldset>
                      </fieldset>
                    )
                  })}
                  <button type="button" className="secondary-button" onClick={addUnit}>Add unit</button>
                </fieldset>
                )}

                <div className="button-row">
                  <button type="submit" disabled={saving}>
                    {saving
                      ? "Saving..."
                      : isEditingExisting
                        ? "Save changes"
                        : editing === "university" ? "Create university" : "Create prospectus"}
                  </button>
                  {editing !== null && (
                    <button type="button" className="secondary-button" onClick={cancelEditor}>
                      Cancel
                    </button>
                  )}
                  {editing === null && (
                    <button type="button" className="secondary-button" onClick={() => setPage("prospectuses")}>
                      Cancel
                    </button>
                  )}
                </div>
              </form>
            </section>
          )}
        </section>
      )}
    </main>
  )
}
