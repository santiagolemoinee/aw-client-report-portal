# Roadmap — AW Client Report Portal

**Project**: Sagan test demo for Windbrook Solutions (EF financial planning firm, Atlanta)
**Time cap**: 2 hours of actual work
**Deadline**: 48 hours from Ritchelle's email
**Deliverables**: live app on Railway + 2-min Loom + GitHub repo

**PRD Confidence Score (official)**:
- Scope Definition: 5/5 — "Exceptionally clear"
- Technical Feasibility: 5/5 — "Zero technical risk"
- Customer Impact: 4/5 — ~24 person-days/year saved across 6 clients
- **Overall: 4/5**

**Real value (per PRD)**: NOT primarily time savings (small, only 6 clients quarterly). The bigger impact is:
1. Eliminating manual math errors
2. Enabling scale — firm can take more clients without hiring more staff

---

## Phase Gate Protocol — STRICT

**Rule**: A phase CANNOT advance to the next until its Definition of Done (DoD) is fully verified through the iteration cycle.

**Gate verification checklist (must pass before next phase):**
1. [ ] All DoD checkboxes ticked
2. [ ] `code-reviewer` agent passed (no critical issues)
3. [ ] `debugger` agent passed (no known bugs)
4. [ ] `error-handling` skill passed (errors gracefully handled)
5. [ ] `security-auditor` agent passed (no vulnerabilities — financial data)
6. [ ] `qa-expert` agent passed (PRD acceptance criteria met)
7. [ ] Manual smoke test passed (the feature actually works)

**If ANY check fails → ITERATE in current phase. Do NOT advance.**

This is non-negotiable. Even if a phase runs over budget, do not skip the gate verification — it's better to ship 4 perfect phases than 6 broken ones.

---

## Iteration Cycle Philosophy

Every phase follows the **continuous iteration cycle**:

```
CODE (frontend / backend / db agents)
  ↓ after every code block:
  1. code-reviewer    → quality & patterns
  2. debugger         → potential bugs
  3. error-handling   → error handling
  4. security-auditor → financial data
  5. qa-expert        → meets PRD
  ↓ if anything fails → ITERATE
```

---

## Critical Reference Documents

- **PRD AI Engineer Test.pdf** — official 14-page spec
- **subtitles.txt** — 45-min video transcript with all rules
- **Data Point List doc** (29:14 in video) — created by Rebecca + Maryann specifically for the build, maps every PDF field to its data source
- **SACS-Example.pdf** — template the SACS PDF must replicate
- **tcc_sample_client Green.pdf** — template the TCC PDF must replicate (sample green; real Windbrook colors are blue)
- **Stitch designs** in `designs/*.png` — UI references

---

## Domain Glossary

| Term | Meaning |
|------|---------|
| **SACS** | Simple Automated Cash Flow — one-page visual diagram of how money flows through bank accounts each month |
| **TCC** | Total Client Chart — one-page net worth overview by account type |
| **Inflow** | Take-home pay (after-tax). Changes only yearly |
| **Outflow** | Agreed monthly expense budget transferred from inflow. Rounded up for buffer ("mental state of abundance") |
| **Private Reserve** | High-yield savings where excess (Inflow − Outflow) accumulates. Target = 6 × monthly expenses + all insurance deductibles |
| **FICA Account** | The Private Reserve, in SACS Page 2 (light blue circle). Often a StoneCastle FICA |
| **Investment Account** | Schwab Brokerage, in SACS Page 2 (navy circle). "Remainder" of liquid wealth |
| **Trust** | Usually funded by primary residence. Value = Zillow Zestimate, updated quarterly |
| **Pinnacle Bank** | Where all clients have personal banking. Balances via secure email 2 days before meeting |
| **RightCapital** | Financial planning aggregator. API unreliable — Maryann: "don't trust RightCapital that much" |
| **PreciseFP** | Onboarding questionnaire tool — closest thing to a CRM |
| **Floor** | $1,000 minimum balance per bank account. Never changes |
| **Quarterly meeting** | ~6 clients × 4 quarters = ~24 reports/year |

---

## Data Format Standards

- **Currency**: USD `$XX,XXX.XX` (US formatting)
- **Dates**: `MMM DD, YYYY` for display; `MM/DD/YY` compact PDF
- **Account numbers**: Last 4 only: `••••4521`
- **SSN**: Last 4 only: `•••-••-1234`
- **Asterisk (*)**: Red asterisk = "we do not have up to date information"
- **Money font**: Plus Jakarta Sans Bold, tabular nums

---

## Non-negotiable Business Rules (apply across ALL phases)

1. **Liabilities NOT subtracted from net worth** — separate informational box only
2. **Trust NOT in Non-Retirement Total** — but DOES enter Grand Total
3. **PDF layout FIXED** — absolute coordinates, nothing shifts
4. **Floor always $1,000** — never changes
5. **Retirement accounts ONLY**: IRA, Roth IRA, 401K, Pension
6. **No Google products** — compliance constraint
7. **No AI in V1** — pure deterministic arithmetic
8. **Inflow is after-tax** — not gross
9. **Outflow rounded up** — for buffer / abundance mindset
10. **Trust = Zillow Zestimate** — accept the imprecision
11. **Schwab access only Rebecca/Andrew** — compliance, never share login
12. **All math automated** — no manual cross-referencing

---

## PHASE 0 — Setup & Initial Deploy (15 min)

### Goal
Empty app running on Railway with public domain. **If this doesn't work, nothing else does.**

### User Stories
- **US0.1**: As an engineer, I need a clean GitHub repo with clear structure so Sagan can review it
- **US0.2**: As an evaluator (Ritchelle), I need to open a Railway link and see the app working without delays

### Definition of Ready (DoR)
- [ ] Final stack decision: Python + Flask + ReportLab + SQLite + Railway
- [ ] Railway account with active $5 trial
- [ ] GitHub account ready
- [ ] Local Python 3.11+ installed (or accept deploying blind via Railway)

### Definition of Done (DoD)
- [ ] GitHub repo with structure: `app.py`, `requirements.txt`, `Procfile`, `static/`, `templates/`, `pdf/`, `database.py`, `seed.py`
- [ ] Flask app responds at root URL
- [ ] Railway auto-deploys → public URL accessible
- [ ] Env vars configured: `RAILWAY_DATABASE_PATH`, optionally `CANVA_API_KEY`
- [ ] `.gitignore` excludes `.env`, `*.db`, `__pycache__`, `venv/`
- [ ] README with: what it is, how to run locally, Railway link
- [ ] No `debug=True` in production

### Phase 0 Gate Checklist
- [ ] App URL responds 200 OK
- [ ] `code-reviewer` reviewed scaffolding — no anti-patterns
- [ ] `security-auditor` confirmed no secrets in repo
- [ ] Manual: opened Railway URL → loaded successfully

### Agents & Skills
- `eng-devops` — Railway config
- `eng-backend` — Flask scaffolding
- `code-reviewer` — final review
- `security-auditor` — secrets audit

### Risks
- Railway fails → fallback Render with sleep enabled (documented)

---

## PHASE 1 — Data Model & Sample Clients (15 min)

### Goal
SQLite database with full schema, seeded with Smith Family ready for end-to-end demo.

### User Stories
- **US1.1**: As Maryann, the portal is pre-loaded with Smith Family for the demo
- **US1.2**: Schema respects business rules (trust separate, liabilities separate, retirement-only)
- **US1.3**: Static data (salary, expense budget) and dynamic data (quarterly balances) modeled separately

### Definition of Ready (DoR)
- [ ] Phase 0 completed AND gate verified
- [ ] Schema spec designed
- [ ] Smith Family sample data identified from TCC sample PDF
- [ ] Static/dynamic distinction clear

### Definition of Done (DoD)

**Schema tables**:
- [ ] `clients` — name, type (married/individual), created_at
- [ ] `client_persons` — first_name, last_name, dob, ssn_last4, role
- [ ] `client_accounts` — type, category (retirement/non_retirement/pinnacle), owner, institution, account_number_last4, is_investment
- [ ] `client_trust` — name, property_address, last_zestimate, last_zestimate_date
- [ ] `client_liabilities` — type, interest_rate, current_balance
- [ ] `client_static_financials` — monthly_salary, monthly_expense_budget, deductible_auto, deductible_home, deductible_health
- [ ] `quarterly_snapshots` — client_id, quarter, generated_at, generated_by
- [ ] `account_balances` — snapshot_id, account_id, balance, cash_balance, is_stale
- [ ] `liability_balances` — snapshot_id, liability_id, balance

**Seed data (Smith Family)**:
- [ ] 2 spouses: Andrew Smith (52, DOB 1974-03-12, SSN ••••4521), Sarah Smith (48, DOB 1977-09-08, SSN ••••7892)
- [ ] Retirement: Roth IRA + IRA per spouse, 1 401K Sarah
- [ ] Non-retirement: Wells Fargo Checking + Savings (joint), Schwab JT TEN, StoneCastle FICA
- [ ] Pinnacle: Inflow, Outflow, Private Reserve
- [ ] Trust: Smith Family Trust, "2847 Peachtree Rd NE, Atlanta GA 30305", $785,000
- [ ] Liabilities: P Mortg 6.25% $234,218.24 / S Mortg 5.50% $107,587.31 / Mercedes 4.20% $11,552 / GMC Sierra 3.90% $25,992 / Escalade 4.70% $31,627.52 / PNC 7.10% $14,028 / Health 0% $1,447
- [ ] Static financials: salary $15,000, expense_budget $12,000, deductibles $1,000/$2,000/$1,000

**Data integrity**:
- [ ] DB persistent volume on Railway
- [ ] All queries parametrized (no SQL injection)
- [ ] WAL mode enabled
- [ ] Indexes on foreign keys
- [ ] Query test: SELECT * FROM clients returns Smith Family

### Phase 1 Gate Checklist
- [ ] All seed data loads successfully
- [ ] `database-administrator` reviewed schema — supports all 12 business rules
- [ ] `sql-pro` reviewed queries — parametrized, indexed
- [ ] `security-auditor` confirmed: SSN never logged, balances never logged
- [ ] `qa-expert` confirmed: schema supports all 4 user stories

### Agents & Skills
- `database-administrator` — schema design
- `sql-pro` — optimized queries
- `eng-backend` — Flask integration
- `code-reviewer` + `security-auditor` — SQL injection + sensitive data
- `qa-expert` — PRD compliance

---

## PHASE 2 — Layout + Clients List (15 min)

### Goal
Reusable layout (navy sidebar + top bar) and the Clients List page.

### User Stories
- **US2.1**: As Maryann, I open the portal and see my client list with status pills
- **US2.2**: Clicking a client takes me to their detail page
- **US2.3**: Layout immediately conveys "premium wealth management"

### Definition of Ready (DoR)
- [ ] Phase 1 completed AND gate verified
- [ ] Stitch designs as reference
- [ ] Design system: navy #0F2A47, Plus Jakarta Sans + Inter, Round-8

### Definition of Done (DoD)
- [ ] `templates/base.html` with reusable sidebar (240px navy) + top bar
  - Sidebar nav: Dashboard, Clients (active), Reports, Settings
  - Bottom: avatar Maryann R. with role label
- [ ] `templates/clients_list.html` with cards/table
  - Each row: name, type, AUM, last report date, status pill, "Generate Report" button
  - Status pill colors: green (Up to date), amber (Due soon), red (Overdue), blue (New)
- [ ] `static/style.css` with design system tokens (CSS variables)
- [ ] Route `/` → `/clients`
- [ ] Route `/clients` lists clients from DB (Smith Family + 2-3 hardcoded extras)
- [ ] Click on client → `/clients/<id>`
- [ ] Search input + filter dropdown (visual only OK)
- [ ] Basic responsiveness at 1280px

### Phase 2 Gate Checklist
- [ ] All routes return 200
- [ ] No console errors
- [ ] `code-reviewer` — semantic HTML, organized CSS
- [ ] `debugger` — no broken links
- [ ] `qa-expert` — visually matches Stitch design

### Agents & Skills
- `frontend-developer` + `eng-frontend`
- `design-uiux` — fidelity
- `code-reviewer`

---

## PHASE 3 — Client Detail + Live SACS Preview (30 min) ⭐

### Goal
The **HERO** screen. Form with balances + live SVG SACS preview that updates as you type.

### User Stories
- **US3.1**: As Maryann, I see static client data pre-loaded
- **US3.2**: Each input field shows last quarter's value as reference
- **US3.3**: I can click "use last value" if a field hasn't changed
- **US3.4**: I can manually override any field
- **US3.5**: I see the SACS updating live as I type
- **US3.6**: As Rebecca, calculations happen automatically — no manual math
- **US3.7**: Form prevents generating report with missing data

### Definition of Ready (DoR)
- [ ] Phase 2 completed AND gate verified
- [ ] Stitch design reference (`designs/02b-client-detail-with-tabs.png`)
- [ ] 4 tabs decided: Overview active, others stub

### Definition of Done (DoD)

**Page layout**:
- [ ] Route `/clients/<id>`
- [ ] Client info card pre-loaded (both spouses + financials)
- [ ] Tabs row: Overview (active 2px navy underline), Reports History, Profile, Activity Log
- [ ] Top-right: "Edit Profile" + "Generate Q2 2026 Report PDF →" (primary navy)

**Form (left, 40%)**:
- [ ] Inflow Andrew/Sarah read-only (from profile)
- [ ] Outflow input + last-quarter reference + "Use Last Value" button
- [ ] Auto-calc indicator: "Excess to Reserve: $X,XXX/mo" (live)
- [ ] Private Reserve / FICA balance input + last-value + delta pill
- [ ] Investment Account (Schwab) input + last-value + delta pill
- [ ] Insurance deductibles: Auto / Home / Health (3 inputs) + computed total
- [ ] Calculated Reserve Target shown
- [ ] Validation: button disabled if any required field empty
- [ ] Validation: error if non-numeric

**Live SACS Preview (right, 60%)**:
- [ ] Header "Live SACS Preview" + green pulsing "Live" indicator
- [ ] Page 1 SVG: green Inflow circle, red Outflow circle, blue Private Reserve circle, arrows with labels, "$1,000 Floor", "MONTHLY CASHFLOW"
- [ ] Page 2 SVG below: light blue FICA Account + navy Investment Account + bidirectional arrow
- [ ] All numbers update on input change (debounced ~150ms)

**Live calculations (JS)**:
- [ ] `excess = (inflow_andrew + inflow_sarah) − outflow`
- [ ] `target = (6 × outflow) + auto + home + health`
- [ ] Updates SVG amounts AND auto-calc indicators in real time

### Phase 3 Gate Checklist
- [ ] Live preview updates within 200ms of typing
- [ ] All calculations match PRD formulas exactly
- [ ] `code-reviewer` — JS modular, no inline handlers
- [ ] `debugger` — edge cases work (empty, NaN, negative, large)
- [ ] `error-handling` — graceful fallback if JS fails
- [ ] `security-auditor` — XSS prevention: inputs escaped before SVG render
- [ ] `qa-expert` — meets PRD US2 acceptance criteria

### Agents & Skills
- `frontend-developer` + `eng-frontend` + `design-uiux`
- `fullstack-developer` — fetch endpoint
- `code-reviewer` + `debugger` + `security-auditor`

---

## PHASE 4 — SACS PDF Generator (30 min) ⭐⭐

### Goal
The **wow factor**. Click "Generate PDF" → download pixel-perfect 2-page SACS.

### User Stories
- **US4.1**: As Maryann, I click and download a pixel-perfect SACS
- **US4.2**: As Andrew, the PDF respects the original template exactly
- **US4.3**: As Rebecca, all arithmetic is correct (Excess, Target, Floor)
- **US4.4**: PDF has client name + date in header automatically
- **US4.5**: Real client reports use Windbrook blue branding

### Definition of Ready (DoR)
- [ ] Phase 3 completed AND gate verified
- [ ] ReportLab installed
- [ ] SACS visual spec clear
- [ ] Sample SACS-Example.pdf reviewed
- [ ] Absolute coordinates planned

### Definition of Done (DoD)

**Architecture**:
- [ ] `pdf/sacs.py` with `generate_sacs(client, snapshot) -> bytes`
- [ ] Helpers: `_draw_circle()`, `_draw_arrow()`
- [ ] Endpoint `/clients/<id>/generate-sacs` returns PDF download

**Page 1**:
- [ ] Title centered, Plus Jakarta Sans 18pt Bold
- [ ] Subtitle "Smith Family — Q2 2026"
- [ ] Top-left: "$8,000 - Andrew / $7,000 - Sarah" green
- [ ] Top-right: "X = Monthly Expenses"
- [ ] Solid green INFLOW circle, white inset rectangle "$15,000", "$1,000 Floor" below
- [ ] Solid red OUTFLOW circle "$12,000", "$1,000 Floor" below
- [ ] Red arrow Inflow → Outflow with "X = $12,000/month* — Automated transfer on the 28th"
- [ ] Solid blue PRIVATE RESERVE circle below
- [ ] Blue L-shaped arrow Inflow → Private Reserve "$3,000/mo*"
- [ ] Bottom: "MONTHLY CASHFLOW"

**Page 2**:
- [ ] Title centered
- [ ] Vertical dashed dividing line
- [ ] Light blue (#7DB3D9) FICA ACCOUNT circle "$75,000" + caption "6X Monthly Expenses + Deductibles"
- [ ] Navy (#0F2A47) INVESTMENT ACCOUNT circle "$15,000+" + caption "Remainder"
- [ ] Bidirectional arrow between them

**Layout integrity**:
- [ ] All ABSOLUTE coordinates
- [ ] Numbers in white inset rectangles
- [ ] Manual test: $15k/$12k → excess $3k, layout intact
- [ ] Edge: Inflow $50k, Outflow $10k → layout doesn't break
- [ ] Edge: very small numbers → still readable

**File handling**:
- [ ] Filename: `SACS_<client>_<quarter>.pdf` (sanitized)
- [ ] No PII in URL/headers
- [ ] PDF size <200KB

### Phase 4 Gate Checklist
- [ ] PDF downloads on click
- [ ] Page 1 + Page 2 visually correct
- [ ] All circles SOLID (not outlined)
- [ ] Arrows render with labels
- [ ] Numbers correct
- [ ] `code-reviewer` — render/data layer separated
- [ ] `debugger` — empty/negative/large numbers handled
- [ ] `error-handling` — clean 500 if ReportLab fails
- [ ] `security-auditor` — sanitized filename, no path traversal
- [ ] `qa-expert` — matches SACS-Example.pdf

### Agents & Skills
- `fullstack-developer` + `eng-backend` + `eng-senior`
- `code-reviewer` + `debugger` + `qa-expert`
- `security-auditor` — sanitization

---

## PHASE 5 — Polish, E2E Testing, Final Deploy (15 min)

### Goal
Smoke test full flow, deploy to Railway, write final README.

### User Stories
- **US5.1**: As Ritchelle, the Railway link works without errors
- **US5.2**: README clearly shows what was done and what's deferred
- **US5.3**: Full flow navigable: dashboard → client → generate → PDF

### Definition of Ready (DoR)
- [ ] Phases 0-4 completed AND gates verified
- [ ] List of bugs/improvements identified

### Definition of Done (DoD)

**E2E smoke test from Railway URL**:
- [ ] Open `/clients` → Smith Family visible
- [ ] Click client → detail page with preview loads
- [ ] All 4 tabs visible (Overview active)
- [ ] Change Outflow input → preview Excess updates live
- [ ] Change Private Reserve → Page 2 preview updates
- [ ] Click "Generate PDF" → SACS downloads
- [ ] Open PDF → both pages visually correct
- [ ] No console errors
- [ ] No 500s in Railway logs

**README content**:
- [ ] Title + one-line description
- [ ] What it is and for whom (EF / Windbrook Solutions)
- [ ] Tech stack
- [ ] How to run locally
- [ ] Live Railway link
- [ ] Screenshots from `designs/`
- [ ] What's implemented section
- [ ] What's next (V1 full) section
- [ ] What's deferred to V2+ section
- [ ] Design decisions section
- [ ] Architecture diagram

**Production hardening**:
- [ ] No `debug=True` in prod
- [ ] Correct `.gitignore`
- [ ] No PII in logs
- [ ] Final push → Railway deploys clean

### Phase 5 Gate Checklist
- [ ] Full E2E smoke test passes
- [ ] No console errors
- [ ] No backend errors in logs
- [ ] `qa-expert` — full PRD acceptance check
- [ ] `debugger` — final pass
- [ ] `security-auditor` — final audit
- [ ] `code-reviewer` — final review
- [ ] README is professional and complete

### Agents & Skills
- `qa-expert` — E2E
- `debugger` — last pass
- `security-auditor` — final audit
- `eng-tech-writer` — README
- `code-reviewer` — final

---

## PHASE 6 — Loom Recording (post-demo)

### Script (max 2 minutes)
- **0:00-0:20** — "Hi, I'm Santiago. I built the AW Client Report Portal for EF — a wealth management firm in Atlanta. Their team currently spends a full day on each quarterly client report. This portal cuts that to under an hour."
- **0:20-0:50** — Show dashboard → Smith Family → click → detail with pre-filled static data + tabs
- **0:50-1:20** — Change Outflow input → live SVG SACS preview updating → click "Generate PDF" → PDF downloads
- **1:20-1:50** — Open PDF → SACS Page 1 (Inflow → Outflow → Private Reserve) and Page 2 (FICA + Investment) → "I prioritized SACS because it's the visual wow. TCC, multi-client, Canva export are on the roadmap."
- **1:50-2:00** — Show clean GitHub repo with README

### DoD
- [ ] Loom max 2 minutes (under, not over)
- [ ] Clear audio
- [ ] Showed: dashboard, detail, live preview, generated PDF (open), repo
- [ ] Mentioned implemented vs next
- [ ] Uploaded and link copied to email reply

---

## Phase Summary (timing)

| Phase | Time | Cumulative | Wow factor |
|-------|------|------------|------------|
| 0 — Setup & Deploy | 15 min | 0:15 | Foundation |
| 1 — DB & Seed | 15 min | 0:30 | — |
| 2 — Layout & Clients List | 15 min | 0:45 | Premium sidebar |
| 3 — Client Detail + Live Preview | 30 min | 1:15 | ⭐ Live updating |
| 4 — SACS PDF Generator | 30 min | 1:45 | ⭐⭐ PDF download |
| 5 — Polish & E2E | 15 min | 2:00 | Everything works |
| **TOTAL** | **2:00** | | |

---

## PRD Acceptance Criteria mapped to roadmap

### US1 (Profile Management) → Phase 1 (partial — Smith Family hardcoded)
- ✅ Names, DOB, age, SSN last 4, spouse — sample data
- ✅ Account structure — DB schema
- ✅ Static financials — sample data
- ✅ Single & married support — schema supports both
- ⚠️ Edit details — NOT in demo, mention in README

### US2a (Quarterly Data Entry) → Phase 3
- ✅ One-click "Generate Report"
- ✅ Form with pre-loaded fields
- ✅ Static data prefilled
- ✅ Last quarter reference per field
- ✅ "Use last value" button
- ✅ Manual override
- ✅ Validation: cannot generate with missing data

### US2b (Automated Calculations) → Phase 3
- ✅ SACS: Excess = Inflow − Outflow
- ✅ SACS: Target = (6 × expenses) + Σ deductibles
- ⚠️ TCC totals — schema ready, NOT calculated in demo
- ✅ Real-time updates

### US3a (SACS PDF) → Phase 4
- ✅ Layout matches: green Inflow, red Outflow, blue Private Reserve, arrows
- ✅ Client name + date in header
- ✅ Page 1: cashflow diagram
- ✅ Page 2: FICA + Investment Account
- ✅ Numbers correctly placed
- ✅ Format fixed
- ✅ Branding colors

### US3b (TCC PDF) → NOT in demo, mention in README

### US4 (Export Options) → Phase 4 (partial)
- ✅ Download as PDF (SACS only)
- ⚠️ Export to Canva — NOT in demo (PRD itself nice-to-have)
- ⚠️ Report history — schema ready, NOT in demo

---

## Discussed But Not Confirmed (NOT in demo)

- **Canva export** — Rebecca said "ideally we don't want to use Canva either" (13:48)
- **Dropbox auto-save** — Maryann asked (41:23), Zaki didn't commit
- **Monthly email** — Rebecca: "we only do quarterly" (16:15)

---

## Out of Scope (Future V2+)

- RightCapital API auto-pull — "don't trust RightCapital that much" (49:06)
- Schwab API auto-pull — compliance (48:14)
- Pinnacle Bank email automation
- Zillow API
- Plaid integration
- Client-facing expense worksheet (42:14)
- Onboarding automation agent (43:36)
- Multi-client setup wizard
- TCC PDF generation (next priority after SACS)
- Reports history / Profile editing / Activity log tabs (UI deferred)
- Auth/login

---

## Global Risk Register

| Risk | Phase | Mitigation |
|------|-------|------------|
| Railway deploy fails | 0 | Render as documented backup |
| ReportLab circles not solid | 4 | `setFillColor` + `circle(fill=1, stroke=0)` |
| Time slipping on CSS | 2 | 80/20 rule, CSS variables, don't perfect |
| Live preview ≠ PDF | 3-4 | Same numeric formatting helpers |
| SQL injection | 1 | Always parametrized queries |
| Sensitive data in logs | All | Never log balances or SSN |
| Console errors during demo | 5 | Smoke test before Loom |
| Live JS preview breaks | 3 | Validate inputs, show placeholder |
| ReportLab arrows hard | 4 | Simple line fallback |
| 2hr cap exceeded | All | Drop nice-to-haves before skipping gate |

---

## Stack and assigned agents

| Layer | Stack | Primary agents |
|-------|-------|----------------|
| Hosting | Railway | `eng-devops` |
| Frontend | HTML + CSS + Vanilla JS | `frontend-developer` + `eng-frontend` |
| Backend | Python + Flask | `fullstack-developer` + `eng-backend` |
| DB | SQLite + Railway Volume | `database-administrator` + `sql-pro` |
| PDF | ReportLab | `fullstack-developer` + `eng-backend` + `eng-senior` |
| Quality (always) | — | `code-reviewer` + `debugger` + `qa-expert` |
| Security (always) | — | `security-auditor` |
| Documentation | — | `eng-tech-writer` |

---

## How this roadmap is enforced

1. **Each phase ends with a gate.** No skipping.
2. **The iteration cycle (5 agents) runs at the end of each phase.** Not optional.
3. **If a phase runs over budget, drop nice-to-haves — never skip the gate.**
4. **Memory files** (`memory/project_*.md`) are the source of truth for business rules.
5. **CLAUDE.md** at the project root is loaded on every session.
6. **`feedback_agents_skills_auto.md`** specifies which agents trigger automatically.
