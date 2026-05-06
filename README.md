# AW Client Report Portal

Internal portal for **Windbrook Solutions** (EF financial planning firm, Atlanta) to generate quarterly **SACS** (Simple Automated Cashflow System) and **TCC** (Total Client Chart) PDF reports for high-net-worth clients.

> Built as a demo for the Sagan AI Automation Engineer test. Reduces manual report preparation from a full day to under one hour.

## Live demo

_Coming soon — Railway deployment in progress._

## What it does

- Stores static client profiles (one-time setup): names, accounts, salary, expense budget, deductibles
- Captures quarterly balance updates via a structured form (no manual math)
- Generates pixel-perfect SACS PDF reports matching the existing template
- Live SVG preview of the SACS as you type

## Tech stack (per PRD)

| Layer | Tool |
|-------|------|
| Hosting | Railway |
| Frontend | HTML + CSS + Vanilla JS (no frameworks) |
| Backend | Python + Flask |
| Database | SQLite (Railway volume) |
| PDF | ReportLab |
| AI | None (deterministic arithmetic only) |

## How to run locally

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000

## Project structure

```
.
├── app.py             # Flask entry point
├── database.py        # SQLite helpers
├── seed.py            # Sample client (Smith Family) seeder
├── pdf/
│   └── sacs.py        # ReportLab SACS generator
├── static/            # CSS, JS, assets
├── templates/         # Jinja2 HTML templates
├── requirements.txt
├── Procfile           # Railway deployment
└── runtime.txt        # Python version
```

## Roadmap

See [`roadmap.md`](roadmap.md) for the full 6-phase plan with Definition of Ready / Definition of Done per phase.

## What's deferred (V2+)

- TCC PDF generation (variable bubble layout)
- Multi-client setup wizard
- Reports history / Profile editing / Activity log tabs
- RightCapital / Schwab / Pinnacle / Zillow API integrations
- Canva export
- Client-facing expense worksheet

## Business rules (non-negotiable)

1. Liabilities are **NOT** subtracted from net worth
2. Trust does **NOT** enter Non-Retirement Total (it does enter Grand Total)
3. PDF layout is **fixed** — absolute coordinates, nothing shifts
4. Floor is always $1,000 in each bank account
5. Retirement accounts only: IRA, Roth IRA, 401K, Pension
6. No Google products (compliance constraint)

## License

Demo / evaluation purposes only.
