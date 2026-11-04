import { useEffect, useState, type FormEvent, type ReactNode } from "react"
import {
  createUniversity,
  deleteUniversity,
  getUniversity,
  listUniversities,
  updateUniversity,
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
  session: string
  website_url: string
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
  session: "",
  website_url: "",
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

function toFormValues(university: University): FormValues {
  return {
    name: university.name,
    session: university.session,
    website_url: university.website_url ?? "",
    overview: university.overview,
    application_start: university.application_start ?? "",
    application_end: university.application_end ?? "",
    admit_card_download: university.admit_card_download ?? "",
    exam_date: university.exam_date ?? "",
    units: university.units.map(toUnitForm),
  }
}

function optionalNumber(value: string): number | null {
  if (!value.trim()) return null
  const parsed = Number(value)
  if (!Number.isFinite(parsed)) throw new Error("Enter a valid number in all numeric fields.")
  return parsed
}

function optionalInteger(value: string): number | null {
  const parsed = optionalNumber(value)
  if (parsed !== null && !Number.isInteger(parsed)) {
    throw new Error("Seat and mark counts must be whole numbers.")
  }
  return parsed
}

function toUnitInput(form: UnitForm): UnitInput {
  return {
    unit_name: form.unit_name,
    background: form.background,
    total_seats: optionalInteger(form.total_seats),
    eligibility_rule: {
      min_ssc_gpa: optionalNumber(form.min_ssc_gpa),
      min_hsc_gpa: optionalNumber(form.min_hsc_gpa),
      combined_gpa: optionalNumber(form.combined_gpa),
      second_time_allowed: form.second_time_allowed ? form.second_time_allowed === "true" : null,
      second_time_penalty_marks: optionalNumber(form.second_time_penalty_marks),
      subject_requirements: form.subject_requirements.trim() || null,
    },
    mark_distribution: {
      total_marks: optionalInteger(form.total_marks),
      mcq_marks: optionalInteger(form.mcq_marks),
      written_marks: optionalInteger(form.written_marks),
      negative_marking_penalty: optionalNumber(form.negative_marking_penalty),
      pass_mark_total: optionalNumber(form.pass_mark_total),
      subject_breakout: form.subject_breakout.trim() || null,
    },
    seat_info: {
      general_seats: optionalInteger(form.general_seats),
      quota_breakdown: form.quota_breakdown.trim() || null,
    },
    important_date: {
      application_start: form.application_start || null,
      application_end: form.application_end || null,
      admit_card_start: form.admit_card_start || null,
      exam_date: form.exam_date || null,
    },
    fee_structure: {
      application_fee: optionalNumber(form.application_fee),
      payment_methods: form.payment_methods.trim() || null,
    },
  }
}

function toUniversityInput(form: FormValues): UniversityInput {
  return {
    name: form.name,
    session: form.session,
    website_url: form.website_url.trim() || null,
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
  const [universities, setUniversities] = useState<University[]>([])
  const [selectedUniversity, setSelectedUniversity] = useState<University | null>(null)
  const [form, setForm] = useState<FormValues>(emptyForm)
  const [editing, setEditing] = useState(false)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState("")

  useEffect(() => {
    void loadUniversities()
  }, [])

  async function loadUniversities(preferredId?: number) {
    setLoading(true)
    setError("")
    try {
      const records = await listUniversities()
      setUniversities(records)
      const nextId = preferredId ?? records[0]?.id
      if (nextId === undefined) {
        setSelectedUniversity(null)
        return
      }
      const university = await getUniversity(nextId)
      setSelectedUniversity(university)
      if (!editing) setForm(toFormValues(university))
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not load prospectuses.")
    } finally {
      setLoading(false)
    }
  }

  async function selectUniversity(id: number) {
    setError("")
    setEditing(false)
    try {
      const university = await getUniversity(id)
      setSelectedUniversity(university)
      setForm(toFormValues(university))
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not load this prospectus.")
    }
  }

  function startNew() {
    setSelectedUniversity(null)
    setForm(emptyForm)
    setEditing(false)
    setError("")
  }

  function startEditing() {
    if (!selectedUniversity) return
    setForm(toFormValues(selectedUniversity))
    setEditing(true)
    setError("")
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setSaving(true)
    setError("")
    try {
      const input = toUniversityInput(form)
      const university =
        editing && selectedUniversity
          ? await updateUniversity(selectedUniversity.id, input)
          : await createUniversity(input)
      setSelectedUniversity(university)
      setForm(toFormValues(university))
      setEditing(false)
      await loadUniversities(university.id)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not save this prospectus.")
    } finally {
      setSaving(false)
    }
  }

  async function handleDelete() {
    if (!selectedUniversity) return
    if (!window.confirm(`Delete the ${selectedUniversity.name} prospectus?`)) return

    setError("")
    try {
      await deleteUniversity(selectedUniversity.id)
      setSelectedUniversity(null)
      setForm(emptyForm)
      setEditing(false)
      await loadUniversities()
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not delete this prospectus.")
    }
  }

  function updateField(field: keyof Omit<FormValues, "units">, value: string) {
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

  const isEditingExisting = editing && selectedUniversity !== null

  return (
    <main className="page-shell">
      <header className="topbar panel">
        <div>
          <p className="eyebrow">Admission information manager</p>
          <h1>Prospekt</h1>
        </div>
        <span className="chip">Prospectus records</span>
      </header>

      {error && <p className="notice error" role="alert">{error}</p>}

      <section className="content-grid">
        <aside className="panel sidebar">
          <div className="section-heading">
            <h2>Prospectuses</h2>
            <button type="button" onClick={startNew}>New record</button>
          </div>
          {loading ? (
            <p>Loading records...</p>
          ) : universities.length === 0 ? (
            <p>No prospectuses have been added yet.</p>
          ) : (
            <ul className="record-list">
              {universities.map((university) => (
                <li key={university.id}>
                  <button
                    type="button"
                    className={
                      university.id === selectedUniversity?.id
                        ? "record-button active"
                        : "record-button"
                    }
                    onClick={() => void selectUniversity(university.id)}
                  >
                    <strong>{university.name}</strong>
                    <span>Session {university.session}</span>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </aside>

        <section className="main-column">
          {selectedUniversity && !editing && (
            <article className="panel detail-card">
              <div className="section-heading">
                <div>
                  <p className="eyebrow">Prospectus details</p>
                  <h2>{selectedUniversity.name}</h2>
                </div>
                <div className="button-row">
                  <button type="button" onClick={startEditing}>Edit</button>
                  <button className="danger-button" type="button" onClick={() => void handleDelete()}>
                    Delete
                  </button>
                </div>
              </div>
              <DetailSection title="University information" entries={[
                ["Admission session", selectedUniversity.session],
                ["Official website", selectedUniversity.website_url ? (
                  <a href={selectedUniversity.website_url} target="_blank" rel="noreferrer">
                    {selectedUniversity.website_url}
                  </a>
                ) : null],
                ["Overview", selectedUniversity.overview || "Not provided"],
              ]} />
              <DetailSection title="University-wide schedule" entries={[
                ["Application opens", selectedUniversity.application_start],
                ["Application closes", selectedUniversity.application_end],
                ["Admit card download", selectedUniversity.admit_card_download],
                ["Admission exam", selectedUniversity.exam_date],
              ]} />
              <section className="units-display">
                <div className="section-heading">
                  <h3>Units ({selectedUniversity.units.length})</h3>
                </div>
                {selectedUniversity.units.length === 0 ? (
                  <p>No units have been added to this university.</p>
                ) : selectedUniversity.units.map((unit) => (
                  <article className="unit-card" key={unit.id}>
                    <h3>{unit.unit_name}</h3>
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
                  </article>
                ))}
              </section>
            </article>
          )}

          {(!selectedUniversity || editing) && (
            <section className="panel form-panel">
              <p className="eyebrow">{isEditingExisting ? "Update record" : "Create record"}</p>
              <h2>{isEditingExisting ? "Edit prospectus" : "New prospectus"}</h2>
              <form className="record-form" onSubmit={(event) => void handleSubmit(event)}>
                <fieldset className="form-section">
                  <legend>University information</legend>
                  <Field
                    id="name"
                    label="University name"
                    value={form.name}
                    onChange={(value) => updateField("name", value)}
                    maxLength={150}
                    required
                  />
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
                    id="website_url"
                    label="Official website URL"
                    value={form.website_url}
                    onChange={(value) => updateField("website_url", value)}
                    type="url"
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
                </fieldset>

                <fieldset className="form-section">
                  <legend>University-wide schedule (optional)</legend>
                  <p className="section-help">Use these dates only when they apply to the university as a whole. Each unit can have its own dates below.</p>
                  <Field id="university_application_start" label="Application opens" type="date" value={form.application_start} onChange={(value) => updateField("application_start", value)} />
                  <Field id="university_application_end" label="Application closes" type="date" value={form.application_end} onChange={(value) => updateField("application_end", value)} />
                  <Field id="university_admit_card_download" label="Admit card download" type="date" value={form.admit_card_download} onChange={(value) => updateField("admit_card_download", value)} />
                  <Field id="university_exam_date" label="Admission exam" type="date" value={form.exam_date} onChange={(value) => updateField("exam_date", value)} />
                </fieldset>

                <fieldset className="form-section">
                  <legend>University units</legend>
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
                        <Field id={`total_seats_${index}`} label="Total seats" type="number" value={unit.total_seats} onChange={field("total_seats")} />

                        <fieldset className="nested-form-section">
                          <legend>Eligibility rules</legend>
                          <Field id={`min_ssc_gpa_${index}`} label="Minimum SSC GPA" type="number" value={unit.min_ssc_gpa} onChange={field("min_ssc_gpa")} />
                          <Field id={`min_hsc_gpa_${index}`} label="Minimum HSC GPA" type="number" value={unit.min_hsc_gpa} onChange={field("min_hsc_gpa")} />
                          <Field id={`combined_gpa_${index}`} label="Combined GPA" type="number" value={unit.combined_gpa} onChange={field("combined_gpa")} />
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
                          <Field id={`second_time_penalty_marks_${index}`} label="Second-time penalty marks" type="number" value={unit.second_time_penalty_marks} onChange={field("second_time_penalty_marks")} />
                          <Field id={`subject_requirements_${index}`} label="Subject requirements" value={unit.subject_requirements} onChange={field("subject_requirements")} multiline />
                        </fieldset>

                        <fieldset className="nested-form-section">
                          <legend>Mark distribution</legend>
                          <Field id={`total_marks_${index}`} label="Total marks" type="number" value={unit.total_marks} onChange={field("total_marks")} />
                          <Field id={`mcq_marks_${index}`} label="MCQ marks" type="number" value={unit.mcq_marks} onChange={field("mcq_marks")} />
                          <Field id={`written_marks_${index}`} label="Written marks" type="number" value={unit.written_marks} onChange={field("written_marks")} />
                          <Field id={`negative_marking_penalty_${index}`} label="Negative marking penalty" type="number" value={unit.negative_marking_penalty} onChange={field("negative_marking_penalty")} />
                          <Field id={`pass_mark_total_${index}`} label="Pass mark" type="number" value={unit.pass_mark_total} onChange={field("pass_mark_total")} />
                          <Field id={`subject_breakout_${index}`} label="Subject mark breakdown" value={unit.subject_breakout} onChange={field("subject_breakout")} placeholder="e.g. English 30 marks, General Knowledge 20 marks" multiline />
                        </fieldset>

                        <fieldset className="nested-form-section">
                          <legend>Seat information</legend>
                          <Field id={`general_seats_${index}`} label="General seats" type="number" value={unit.general_seats} onChange={field("general_seats")} />
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
                          <Field id={`application_fee_${index}`} label="Application fee" type="number" value={unit.application_fee} onChange={field("application_fee")} />
                          <Field id={`payment_methods_${index}`} label="Payment methods and instructions" value={unit.payment_methods} onChange={field("payment_methods")} multiline />
                        </fieldset>
                      </fieldset>
                    )
                  })}
                  <button type="button" className="secondary-button" onClick={addUnit}>Add unit</button>
                </fieldset>

                <div className="button-row">
                  <button type="submit" disabled={saving}>
                    {saving ? "Saving..." : isEditingExisting ? "Save changes" : "Create prospectus"}
                  </button>
                  {editing && (
                    <button type="button" className="secondary-button" onClick={() => {
                      setEditing(false)
                      if (selectedUniversity) setForm(toFormValues(selectedUniversity))
                    }}>
                      Cancel
                    </button>
                  )}
                </div>
              </form>
            </section>
          )}
        </section>
      </section>
    </main>
  )
}
