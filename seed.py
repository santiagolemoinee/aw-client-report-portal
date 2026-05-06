"""Smith Family seed data — Phase 1. Idempotent: safe to run multiple times."""
from database import get_connection, init_db


def seed_smith_family():
    with get_connection() as conn:
        existing = conn.execute(
            "SELECT id FROM clients WHERE name = ?", ("Smith Family",)
        ).fetchone()
        if existing:
            return existing["id"]

        # --- Client ---
        cur = conn.execute(
            "INSERT INTO clients (name, type, status) VALUES (?, ?, ?)",
            ("Smith Family", "married", "active"),
        )
        cid = cur.lastrowid

        # --- Persons ---
        conn.execute(
            "INSERT INTO client_persons "
            "(client_id, first_name, last_name, dob, ssn_last4, role) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (cid, "Andrew", "Smith", "1974-03-12", "4521", "client_1"),
        )
        conn.execute(
            "INSERT INTO client_persons "
            "(client_id, first_name, last_name, dob, ssn_last4, role) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (cid, "Sarah", "Smith", "1977-09-08", "7892", "client_2"),
        )

        # --- Retirement accounts ---
        retirement = [
            ("Roth IRA", "client_1", "Schwab",   "1234", "Andrew – Roth IRA", None, 1, 1),
            ("IRA",      "client_1", "Schwab",   "5678", "Andrew – IRA",      None, 1, 2),
            ("Roth IRA", "client_2", "Schwab",   "9012", "Sarah – Roth IRA",  None, 1, 3),
            ("IRA",      "client_2", "Schwab",   "3456", "Sarah – IRA",       None, 1, 4),
            ("401K",     "client_2", "Fidelity", "7890", "Sarah – 401K",      None, 1, 5),
        ]
        acct_ids = {}
        for acct_type, owner, institution, acct4, label, sacs_role, is_inv, disp in retirement:
            cur = conn.execute(
                "INSERT INTO client_accounts "
                "(client_id, account_type, category, owner, institution, "
                " account_number_last4, label, sacs_role, display_order, is_investment) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (cid, acct_type, "retirement", owner, institution,
                 acct4, label, sacs_role, disp, is_inv),
            )
            acct_ids[label] = cur.lastrowid

        # --- Non-retirement accounts ---
        non_ret = [
            ("Checking",  "joint", "Wells Fargo", "2341", "WF Main Checking", None,                 0, 1),
            ("Savings",   "joint", "Wells Fargo", "5612", "WF Savings",       None,                 0, 2),
            ("Brokerage", "joint", "Schwab",      "8923", "Schwab JT TEN",    "investment_account", 1, 3),
            ("FICA",      "joint", "StoneCastle", "4521", "StoneCastle FICA", "fica_account",       0, 4),
        ]
        for acct_type, owner, institution, acct4, label, sacs_role, is_inv, disp in non_ret:
            cur = conn.execute(
                "INSERT INTO client_accounts "
                "(client_id, account_type, category, owner, institution, "
                " account_number_last4, label, sacs_role, display_order, is_investment) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (cid, acct_type, "non_retirement", owner, institution,
                 acct4, label, sacs_role, disp, is_inv),
            )
            acct_ids[label] = cur.lastrowid

        # --- Pinnacle accounts (SACS flow accounts) ---
        pinnacle = [
            ("Checking", "joint", "Pinnacle Bank", "1001", "Pinnacle Inflow",          "inflow",          0, 1),
            ("Checking", "joint", "Pinnacle Bank", "1002", "Pinnacle Outflow",         "outflow",         0, 2),
            ("FICA",     "joint", "Pinnacle Bank", "1003", "Pinnacle Private Reserve", "private_reserve", 0, 3),
        ]
        for acct_type, owner, institution, acct4, label, sacs_role, is_inv, disp in pinnacle:
            cur = conn.execute(
                "INSERT INTO client_accounts "
                "(client_id, account_type, category, owner, institution, "
                " account_number_last4, label, sacs_role, display_order, is_investment) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (cid, acct_type, "pinnacle", owner, institution,
                 acct4, label, sacs_role, disp, is_inv),
            )
            acct_ids[label] = cur.lastrowid

        # --- Trust ---
        conn.execute(
            "INSERT INTO client_trust "
            "(client_id, name, property_address, last_zestimate, last_zestimate_date) "
            "VALUES (?, ?, ?, ?, ?)",
            (cid, "Smith Family Trust",
             "2847 Peachtree Rd NE, Atlanta GA 30305",
             785000.00, "2026-03-31"),
        )

        # --- Liabilities ---
        liabilities_data = [
            ("Primary Mortgage",       6.25, 234218.24, 1),
            ("Secondary Mortgage",     5.50, 107587.31, 2),
            ("Mercedes Loan",          4.20,  11552.00, 3),
            ("GMC Sierra Loan",        3.90,  25992.00, 4),
            ("Cadillac Escalade Loan", 4.70,  31627.52, 5),
            ("PNC Loan",               7.10,  14028.00, 6),
            ("Health Loan",            0.00,   1447.00, 7),
        ]
        liab_ids = {}
        for liab_type, rate, balance, disp in liabilities_data:
            cur = conn.execute(
                "INSERT INTO client_liabilities "
                "(client_id, type, interest_rate, display_order) VALUES (?, ?, ?, ?)",
                (cid, liab_type, rate, disp),
            )
            liab_ids[liab_type] = (cur.lastrowid, balance)

        # --- Static financials (Andrew $8k + Sarah $7k = $15k total inflow) ---
        conn.execute(
            "INSERT INTO client_static_financials "
            "(client_id, monthly_salary_client_1, monthly_salary_client_2, "
            " monthly_expense_budget, deductible_auto, deductible_home, deductible_health) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (cid, 8000.00, 7000.00, 12000.00, 1000.00, 2000.00, 1000.00),
        )

        # --- Q1 2026 snapshot (complete) ---
        cur = conn.execute(
            "INSERT INTO quarterly_snapshots (client_id, quarter, status, generated_by) "
            "VALUES (?, ?, ?, ?)",
            (cid, "Q1 2026", "complete", "seed"),
        )
        snap_id = cur.lastrowid

        account_balances = {
            "Andrew – Roth IRA":        45000.00,
            "Andrew – IRA":            125000.00,
            "Sarah – Roth IRA":         38000.00,
            "Sarah – IRA":              87000.00,
            "Sarah – 401K":            215000.00,
            "WF Main Checking":             25000.00,
            "WF Savings":                   18000.00,
            "Schwab JT TEN":               285000.00,
            "StoneCastle FICA":             78500.00,
            "Pinnacle Inflow":              16240.00,
            "Pinnacle Outflow":              1850.00,
            "Pinnacle Private Reserve":      4200.00,
        }
        for label, bal in account_balances.items():
            conn.execute(
                "INSERT INTO account_balances "
                "(snapshot_id, account_id, balance, is_stale) VALUES (?, ?, ?, ?)",
                (snap_id, acct_ids[label], round(bal, 2), 0),
            )

        for liab_type, (lid, bal) in liab_ids.items():
            conn.execute(
                "INSERT INTO liability_balances (snapshot_id, liability_id, balance) "
                "VALUES (?, ?, ?)",
                (snap_id, lid, round(bal, 2)),
            )

        return cid


if __name__ == "__main__":
    init_db()
    cid = seed_smith_family()
    print(f"Smith Family seeded — client_id={cid}")
