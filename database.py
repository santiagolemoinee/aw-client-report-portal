import os
import sqlite3
from contextlib import contextmanager

DB_PATH = os.environ.get("RAILWAY_DATABASE_PATH", "data/portal.db")


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if os.path.exists(DB_PATH):
        with get_connection() as conn:
            conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")

    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS clients (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT    NOT NULL,
                type       TEXT    NOT NULL CHECK(type IN ('married', 'individual')),
                status     TEXT    NOT NULL DEFAULT 'active'
                               CHECK(status IN ('active', 'review', 'inactive')),
                created_at TEXT    NOT NULL DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS client_persons (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id  INTEGER NOT NULL REFERENCES clients(id),
                first_name TEXT    NOT NULL,
                last_name  TEXT    NOT NULL,
                dob        TEXT    NOT NULL
                               CHECK(dob GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'),
                ssn_last4  TEXT    NOT NULL
                               CHECK(LENGTH(ssn_last4) = 4
                                     AND ssn_last4 GLOB '[0-9][0-9][0-9][0-9]'),
                role       TEXT    NOT NULL CHECK(role IN ('client_1', 'client_2'))
            );

            CREATE TABLE IF NOT EXISTS client_accounts (
                id                   INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id            INTEGER NOT NULL REFERENCES clients(id),
                account_type         TEXT    NOT NULL
                                         CHECK(account_type IN (
                                             'IRA', 'Roth IRA', '401K', 'Pension',
                                             'Brokerage', 'Checking', 'Savings',
                                             'Joint', 'FICA'
                                         )),
                category             TEXT    NOT NULL
                                         CHECK(category IN (
                                             'retirement', 'non_retirement', 'pinnacle'
                                         )),
                owner                TEXT    NOT NULL
                                         CHECK(owner IN ('client_1', 'client_2', 'joint')),
                institution          TEXT    NOT NULL,
                account_number_last4 TEXT
                                         CHECK(account_number_last4 IS NULL
                                               OR LENGTH(account_number_last4) = 4),
                label                TEXT    NOT NULL DEFAULT '',
                sacs_role            TEXT
                                         CHECK(sacs_role IS NULL OR sacs_role IN (
                                             'inflow', 'outflow', 'private_reserve',
                                             'fica_account', 'investment_account'
                                         )),
                display_order        INTEGER NOT NULL DEFAULT 0,
                is_investment        INTEGER NOT NULL DEFAULT 0
                                         CHECK(is_investment IN (0, 1))
            );

            CREATE TABLE IF NOT EXISTS client_trust (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id           INTEGER NOT NULL REFERENCES clients(id),
                name                TEXT    NOT NULL,
                property_address    TEXT    NOT NULL,
                last_zestimate      REAL    NOT NULL CHECK(last_zestimate >= 0),
                last_zestimate_date TEXT    NOT NULL
            );

            CREATE TABLE IF NOT EXISTS client_liabilities (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id     INTEGER NOT NULL REFERENCES clients(id),
                type          TEXT    NOT NULL,
                interest_rate REAL    NOT NULL CHECK(interest_rate >= 0),
                display_order INTEGER NOT NULL DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS client_static_financials (
                id                       INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id                INTEGER NOT NULL UNIQUE REFERENCES clients(id),
                monthly_salary_client_1  REAL    NOT NULL CHECK(monthly_salary_client_1 >= 0),
                monthly_salary_client_2  REAL    NOT NULL DEFAULT 0
                                             CHECK(monthly_salary_client_2 >= 0),
                monthly_expense_budget   REAL    NOT NULL CHECK(monthly_expense_budget >= 0),
                deductible_auto          REAL    NOT NULL DEFAULT 0
                                             CHECK(deductible_auto >= 0),
                deductible_home          REAL    NOT NULL DEFAULT 0
                                             CHECK(deductible_home >= 0),
                deductible_health        REAL    NOT NULL DEFAULT 0
                                             CHECK(deductible_health >= 0)
            );

            CREATE TABLE IF NOT EXISTS quarterly_snapshots (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id    INTEGER NOT NULL REFERENCES clients(id),
                quarter      TEXT    NOT NULL
                                 CHECK(quarter GLOB 'Q[1-4] [0-9][0-9][0-9][0-9]'),
                status       TEXT    NOT NULL DEFAULT 'draft'
                                 CHECK(status IN ('draft', 'complete', 'archived')),
                generated_at TEXT    NOT NULL DEFAULT (datetime('now')),
                generated_by TEXT    NOT NULL DEFAULT 'system'
            );

            CREATE TABLE IF NOT EXISTS account_balances (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                snapshot_id  INTEGER NOT NULL REFERENCES quarterly_snapshots(id),
                account_id   INTEGER NOT NULL REFERENCES client_accounts(id),
                balance      REAL    NOT NULL CHECK(balance >= 0),
                cash_balance REAL,
                is_stale     INTEGER NOT NULL DEFAULT 0 CHECK(is_stale IN (0, 1))
            );

            CREATE TABLE IF NOT EXISTS liability_balances (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                snapshot_id  INTEGER NOT NULL REFERENCES quarterly_snapshots(id),
                liability_id INTEGER NOT NULL REFERENCES client_liabilities(id),
                balance      REAL    NOT NULL CHECK(balance >= 0)
            );

            -- FK indexes
            CREATE INDEX IF NOT EXISTS idx_client_persons_client
                ON client_persons(client_id);
            CREATE INDEX IF NOT EXISTS idx_client_accounts_client
                ON client_accounts(client_id);
            CREATE INDEX IF NOT EXISTS idx_client_trust_client
                ON client_trust(client_id);
            CREATE INDEX IF NOT EXISTS idx_client_liabilities_client
                ON client_liabilities(client_id);
            CREATE INDEX IF NOT EXISTS idx_snapshots_client
                ON quarterly_snapshots(client_id);
            CREATE INDEX IF NOT EXISTS idx_account_balances_snapshot
                ON account_balances(snapshot_id);
            CREATE INDEX IF NOT EXISTS idx_account_balances_account
                ON account_balances(account_id);
            CREATE INDEX IF NOT EXISTS idx_liability_balances_snapshot
                ON liability_balances(snapshot_id);
            CREATE INDEX IF NOT EXISTS idx_liability_balances_liability
                ON liability_balances(liability_id);

            -- Query pattern indexes
            CREATE INDEX IF NOT EXISTS idx_snapshots_client_quarter
                ON quarterly_snapshots(client_id, quarter);
            CREATE INDEX IF NOT EXISTS idx_accounts_client_category
                ON client_accounts(client_id, category);
        """)
