# Missing MCP Servers - Research Results **Date**: 2025-10-06

**Research Status**:  All servers located

---

##  Summary All 6 "missing" MCP servers have been located with correct package names and installation methods. | Server | Status | Correct Package/Repo |

|--------|--------|---------------------|
| MCP Code Checker |  Found | `mcp_server_code_checker_python` (GitHub) |
| Python LFT MCP |  Found | `python-lft-mcp` (PyPI) |
| MCP Analyzer |  Found | `mcp-server-analyzer` (PyPI/uvx) |
| NumPy MCP |  Found | `numpy-mcp` (GitHub) |
| Pandas MCP |  Found | `pandas-mcp-server` (GitHub) |
| Sphinx-MCP |  Found | `sphinx-mcp` (PyPI, likely already installed) |

---

## 1⃣ MCP Code Checker (Python) ### Overview

MCP server providing code quality checks (pylint and pytest) with smart LLM-friendly prompts for analysis and fixes. ### Correct Installation **Option A: From GitHub (Recommended)**
```bash
# Clone repository
git clone https://github.com/mcpflow/mcp_server_code_checker_python.git
cd mcp_server_code_checker_python # Install with pip
pip install -e . # Or install directly
pip install git+https://github.com/mcpflow/mcp_server_code_checker_python.git
``` **Option B: Alternative Repository**

```bash
git clone https://github.com/MarcusJellinghaus/mcp-code-checker.git
cd mcp-code-checker
pip install -e .
``` ### Running

```bash
python -m src.main --project-dir D:\Projects\main
``` ### Features

-  Run pylint checks for code quality
-  Execute pytest to identify failing tests
-  Generate smart prompts for LLMs
-  Explain issues and suggest fixes ### Requirements
- Python 3.10+
- Python MCP SDK 1.2.0+ ### Configuration
```json
{ "code-checker": { "type": "stdio", "command": "python", "args": ["-m", "src.main", "--project-dir", "D:\\Projects\\main"], "env": {}, "description": "Code quality checks with pylint and pytest" }
}
```

---

## 2⃣ Python LFT MCP (Lint, Format, Test) ### Overview

Modern, modular Python development tools package exposing linting, formatting, and testing features via MCP. ### Correct Installation **From PyPI:**
```bash
# Basic installation
pip install python-lft-mcp # With all optional tool dependencies (recommended)
pip install python-lft-mcp[tools]
``` ### Features

-  Auto-detection of 70+ Python config files
-  Integrated tools: ruff, black, pytest, mypy, pylint
-  Unified MCP interface
-  Tox for standardized workflows ### Supported Tools
- **Linting**: ruff, pylint
- **Formatting**: black, ruff
- **Testing**: pytest
- **Type Checking**: mypy
- **Coverage**: coverage reporting ### Configuration
```json
{ "python-lft": { "type": "stdio", "command": "python", "args": ["-m", "python_lft_mcp"], "env": {}, "description": "Python lint, format, and test tools" }
}
```

---

## 3⃣ MCP Server Analyzer (RUFF + Vulture) ### Overview

Python code analysis using RUFF for linting and VULTURE for dead code detection. ### Correct Installation **Option A: uvx (Recommended)**
```bash
uvx install mcp-server-analyzer
``` **Option B: pip**

```bash
pip install mcp-server-analyzer
``` **Option C: From Source**

```bash
git clone https://github.com/anselmoo/mcp-server-analyzer.git
cd mcp-server-analyzer
uv sync --dev
uv run mcp-server-analyzer
``` **Option D: Docker**

```bash
docker run ghcr.io/anselmoo/mcp-server-analyzer:latest
``` ### Features

-  **RUFF Analysis**: Python linting with auto-fixes
-  **Dead Code Detection**: Find unused imports, functions, variables with VULTURE ### Package Info
- **PyPI**: mcp-server-analyzer v0.1.1
- **GitHub**: https://github.com/anselmoo/mcp-server-analyzer ### Configuration
```json
{ "analyzer": { "type": "stdio", "command": "uvx", "args": ["mcp-server-analyzer"], "env": {}, "description": "RUFF linting and VULTURE dead code detection" }
}
```

---

## 4⃣ NumPy MCP Server ### Overview

Model Context Protocol server for numerical computations with NumPy. ### Correct Installation **From GitHub:**
```bash
# Clone repository
git clone https://github.com/colesmcintosh/numpy-mcp.git
cd numpy-mcp # Install with UV
uv venv
source .venv/bin/activate # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt # Or install in Claude Desktop
mcp install server.py --name "NumPy Calculator"
``` ### Features

-  Basic arithmetic operations
-  Linear algebra (matrix multiplication, eigendecomposition)
-  Statistical analysis (mean, median, std dev)
-  Polynomial fitting ### Testing with Dependencies
```bash
uv run mcp dev server.py --with pandas --with numpy
``` ### Configuration

```json
{ "numpy-mcp": { "type": "stdio", "command": "python", "args": ["D:\\Projects\\main\\.mcp_servers\\numpy-mcp\\server.py"], "env": {}, "description": "NumPy numerical computations and linear algebra" }
}
```

---

## 5⃣ Pandas MCP Server ### Overview

Multiple implementations available for pandas data analysis via MCP. ### Correct Installation **Option A: marlonluo2018 implementation (Recommended)**
```bash
git clone https://github.com/marlonluo2018/pandas-mcp-server.git
cd pandas-mcp-server
pip install -r requirements.txt
``` **Option B: alistairwalsh implementation**

```bash
# Available via PulseMCP
# Installation details from repository
``` ### Features

-  Execute pandas code through standardized workflow
-  Data manipulation and analysis
-  Statistical analysis
-  Data visualization with matplotlib
-  Support for CSV and Parquet files ### Use Cases
- Automated data exploration
- Dynamic RAG pipelines
- Real-time sentiment analysis
- Data-driven project analysis ### Configuration
```json
{ "pandas-mcp": { "type": "stdio", "command": "python", "args": ["D:\\Projects\\main\\.mcp_servers\\pandas-mcp-server\\server.py"], "env": {}, "description": "Pandas data analysis and visualization" }
}
```

---

## 6⃣ Sphinx-MCP Extension ### Overview

Sphinx extension for documenting MCP tools, prompts, resources and resource templates. ### Correct Installation **Option A: From PyPI (if available)**
```bash
pip install sphinx-mcp
``` **Option B: From GitHub (Development)**

```bash
git clone https://github.com/sphinx-contrib/mcp.git
cd mcp
uv sync --all-groups
``` ### Status

- ⏳ Early stage project (no tests yet)
-  Documentation: sphinx-mcp.pdf (pre-compiled)
-  Development setup with uv and pre-commit ### Features
- Document MCP tools
- Document prompts
- Document resources and resource templates
- Sphinx integration for documentation generation ### Requirements
- uv for dependency management
- pre-commit for Git hooks ### Verification
```bash
# Check if already installed
pip list | grep sphinx-mcp
python -c "import sphinx_mcp; print(sphinx_mcp.__version__)"
```

---

##  Installation Priority ### High Priority (Production Ready)

1. **mcp-server-analyzer** - RUFF + Vulture, ready to use
2. **python-lft-mcp** - Available on PyPI, tooling ### Medium Priority (Active Development)
3. **mcp-code-checker** - Stable GitHub repos, good for code quality
4. **numpy-mcp** - Useful for numerical analysis in PSO/optimization ### Lower Priority (Specialized Use Cases)
5. **pandas-mcp** - Good for data analysis but overlaps with SQLite
6. **sphinx-mcp** - Documentation only, early stage

---

##  Recommended Installation Order 1. **mcp-server-analyzer** (uvx) - Easiest install, immediate value

2. **python-lft-mcp** (PyPI) - One command install, broad utility
3. **mcp-code-checker** (GitHub) - Clone and pip install
4. **numpy-mcp** (GitHub) - For PSO numerical analysis
5. **pandas-mcp** (GitHub) - If needed for advanced data analysis
6. **sphinx-mcp** (verify existing) - Already attempted, check status

---

##  Local Server Directory Structure Create a dedicated directory for locally-installed MCP servers: ```

D:\Projects\main\.mcp_servers\
 mcp-code-checker\
 numpy-mcp\
 pandas-mcp-server\
``` This keeps GitHub-cloned servers organized and separate from npm global packages.

---

##  Next Steps 1. Install high-priority servers (analyzer, python-lft)
2. Clone and setup GitHub-based servers (code-checker, numpy-mcp, pandas-mcp)
3. Verify sphinx-mcp installation status
4. Update .mcp.json with all new server configurations
5. Test each server with MCP Inspector
6. Create testing workflow

---

**Last Updated**: 2025-10-06
**Research By**: Claude Code
