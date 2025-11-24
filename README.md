## 🚀 Setup Instructions (Using uv)

This project uses **uv** for dependency management and virtual environments.  
No `requirements.txt` is needed — all dependencies are defined in `pyproject.toml`.

---

### 1. Install uv

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify installation:
```bash
uv --version
```

---

### 2. Clone the Repository

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

---

### 3. Install All Dependencies

```bash
uv sync
```

`uv sync` will:
- Create a `.venv/` virtual environment  
- Install all project dependencies  
- Install workspace members (e.g., `simple_agent`, `advanced_agent`)  
- Use `pyproject.toml` + `uv.lock` for reproducible builds  

---

### 4. Activate the Virtual Environment

**macOS / Linux:**
```bash
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

---

### 5. Run the Project

Examples:

```bash
python simple_agent/main.py
```

Or if using FastAPI:

```bash
uvicorn simple_agent.main:app --reload
```

---

### Notes

- No `requirements.txt` is required — uv manages all dependencies.
- Workspace members defined in `pyproject.toml` are installed automatically.
- To upgrade dependencies later:
```bash
uv sync --upgrade
```
