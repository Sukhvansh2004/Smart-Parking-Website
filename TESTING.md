# 🧪 Testing Guide

This document explains how to run and extend the pytest suite for the Smart Parking Website backend.

---

## 🚀 Prerequisites

pip install pytest module for carrying out the testing
---

## 🗂️ Project Layout

```
backend/
├── auth.py             # Google OAuth & JWT logic
├── create_admin.py     # CLI script to seed admin user
├── database.py         # SQLAlchemy models & engine
├── main.py             # FastAPI app & endpoints
├── secret.py           # Loads env vars (DATABASE_URL, SECRET_KEY…)
└── tests/
    ├── conftest.py     # pytest fixtures & env/db setup
    ├── test_auth.py
    ├── test_create_admin.py
    ├── test_database.py
    ├── test_main.py
    └── test_secret.py
```

---

## 🔧 Environment Overrides

All tests are isolated in their own temporary SQLite database. The `tests/conftest.py` fixture:

1. Uses `tmp_path_factory` to create a `test.db` file.  
2. Monkey‑patches `DATABASE_URL`, `SECRET_KEY`, `GOOGLE_CLIENT_ID`, and `GOOGLE_CLIENT_SECRET`.  
3. Reloads modules (`database`, `main`, `secret`, `create_admin`, `auth`) to pick up the test env.  
4. Runs `Base.metadata.create_all()` before tests and drops tables after.

You don’t need to manually set any env vars—pytest does it for you, however do source the set_env.sh file before running the tests

---

## ▶️ Running the Tests

From within `/backend`, simply run:

```bash
pytest tests/ -v
```

- `-v` (verbose) shows each test name and pass/fail status.
- All tests should complete in under a few seconds.

### Filtering Tests

- **Single file**  
  ```bash
  pytest tests/test_auth.py -v
  ```

- **Pattern**  
  ```bash
  pytest -k "auth or secret" -v
  ```

- **With coverage**  
  ```bash
  pytest --cov=./ --cov-report=term-missing
  ```

---

## 📋 Test Breakdown

### 1. `test_auth.py`
- **Google OAuth**  
  - Stubs `id_token.verify_oauth2_token` for valid/invalid cases.
- **Password hashing**  
  - Checks `get_password_hash()` ↔ `verify_password()`.
- **JWT**  
  - `create_access_token()` → `decode_access_token()`.

### 2. `test_secret.py`
- Verifies `secret.py` picks up all four env vars.

### 3. `test_database.py`
- `init_db()` runs without error.
- CRUD on `ParkingSlot` & `Admin` models via a fresh session.

### 4. `test_create_admin.py`
- `create_admin()` CLI logic:
  - New admin creation outputs a success message.
  - Duplicate admin prints an “already exists” warning.
  - Uses the `db` fixture’s session under the hood.

### 5. `test_main.py`
- **Public endpoints**  
  - `/parking_status`, `/book/{slot}`, `/release/{slot}`, `/user?token=…`  
- **Admin endpoints**  
  - `/admin/login`, `/admin/add_slot/{slot}`, `/admin/delete_slot/{slot}`, `/admin/verify`  
  - Validates HTTP codes, payloads, and token-based auth.

---

## ➕ Adding New Tests

1. **Write a new file** under `tests/`, e.g. `test_my_feature.py`.  
2. Import any fixtures (`client`, `db`, or auto‑use `env_and_db`).  
3. Follow naming convention: functions beginning with `test_`.  
4. Run only your file to iterate quickly:
   ```bash
   pytest tests/test_my_feature.py -q
   ```

---

## 🐞 Troubleshooting

- **`ModuleNotFoundError: No module named 'auth'`**  
  Ensure you ran `pytest` from the `backend/` directory so `sys.path` sees your modules.

- **DB errors (UndefinedTable, Relation does not exist)**  
  Confirm `conftest.py` is reloading `create_admin.py` & `database.py` *after* patching `DATABASE_URL`.

- **Slow tests**  
  Bcrypt hashing is somewhat slow by design; you can lower the cost factor in `auth.py` during development if needed.

---
