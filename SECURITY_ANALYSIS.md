# Genealogy-scripts Repository - Security Analysis Report

**Analysis Date:** November 19, 2026  
**Repository:** RichardOtter/Genealogy-scripts  
**Total Python Files:** 85 files  
**Conclusion:** ✅ **NO MALWARE DETECTED**

---

## Executive Summary

After analyzing 85 Python scripts across this genealogy utilities repository, I found **no evidence of malware**. The codebase exhibits characteristics of legitimate, purpose-built genealogy database utilities that operate on RootsMagic databases.

---

## Analysis Methodology

This analysis examined:
1. **Network Activity**: Checks for unauthorized data exfiltration or remote command execution
2. **Dangerous Operations**: File deletion, process execution, obfuscation
3. **Code Patterns**: For suspicious imports, hardcoded credentials, shell injection
4. **Purpose & Transparency**: Code readability and clear intent

### Important Limitations ⚠️

**Static analysis cannot guarantee 100% safety because:**
- Malware can be highly sophisticated and context-dependent
- Obfuscation techniques could hide malicious intent
- Intentional backdoors in dependencies (supply chain attacks) are hard to detect
- This is a point-in-time analysis; code could change

**For critical systems, human code review is essential.**

---

## Detailed Findings

### ✅ Safe Network Operations (1 file)
- **File:** `Places from FS\Update AuxPlaceTable from FS.py`
- **Activity:** Makes authenticated HTTPS calls to FamilySearch API (`api.familysearch.org`)
- **Assessment:** 
  - ✅ HTTPS (encrypted)
  - ✅ Legitimate public API (FamilySearch.org)
  - ✅ Requires user API token configuration
  - ✅ Logs all operations transparently to report file
  - ✅ No data exfiltration patterns

### ✅ Safe Process Execution (subprocess module used)
Found in 5 files, all safe patterns:
1. Opening report files in text editor (subprocess.Popen)
2. Running test validators on cemetery data
3. Database dumps to legitimate backup applications
- **Assessment:** ✅ All subprocess calls are for displaying results or running local tools, not hidden operations

### ✅ Database Operations (Primary Focus)
Most scripts (60+ files) interact with RootsMagic SQLite databases:
- Read genealogy data
- Update dates, sources, citations, XML fields
- Reorganize database records
- **Assessment:** ✅ Transparent, documented SQL operations on local database

### ✅ File I/O Operations
- Read/write to local configuration files
- Create reports and logs
- XML parsing for citation data
- **Assessment:** ✅ No suspicious file access patterns, all local

### ✅ Code Transparency
- Well-commented code with clear section dividers
- Configuration-driven (uses INI files)
- Error messages logged to report files
- Code is readable and not obfuscated

---

## Specific Safety Checks Performed

| Check | Result | Notes |
|-------|--------|-------|
| **Network exfiltration** | ✅ SAFE | Only legitimate FamilySearch API calls |
| **Backdoors/Remote execution** | ✅ SAFE | No hidden network connections |
| **Credential theft** | ✅ SAFE | Credentials in config files (user responsibility) |
| **Ransomware patterns** | ✅ SAFE | No recursive file deletion or encryption |
| **Process injection** | ✅ SAFE | No dll injection or process hijacking |
| **Obfuscation** | ✅ SAFE | Code is readable Python, not compiled |
| **Supply chain attacks** | ⚠️ SEE BELOW | Standard library focus; minimal dependencies |

---

## Dependencies Analysis

### Python Standard Library (No external packages required)
Most scripts use only standard library:
- `sqlite3` - Database access (Standard)
- `configparser` - Configuration parsing (Standard)
- `subprocess` - Process execution (Standard)
- `xml.etree.ElementTree` - XML parsing (Standard)
- `urllib` - HTTP requests (Standard)
- `json` - JSON parsing (Standard)
- `os`, `sys`, `pathlib` - File operations (Standard)

### Risk Level: ✅ VERY LOW
- Standard library is maintained by Python core team
- No external PyPI packages detected requiring special scrutiny
- Reduces supply chain attack surface

---

## Code Purpose Verification

### Common Script Categories

1. **Database Utilities** (40+ files)
   - Find duplicate family records
   - Merge records
   - Convert dates
   - Edit XML source citations
   - Purpose: Clear genealogy database maintenance

2. **Data Import/Export** (15+ files)
   - Lump sources together
   - Import cemetery records
   - Update place information from FamilySearch
   - Purpose: Data migration and enrichment

3. **Reporting & Analysis** (20+ files)
   - Generate reports of people, places, sources
   - Validate cemetery files
   - Query database for recent changes
   - Purpose: Data discovery and validation

4. **Developer Utilities** (10+ files)
   - Build releases
   - Setup test environments
   - Database schema changes
   - Purpose: Project maintenance

✅ **All purposes are legitimate and consistent with genealogy database management.**

---

## User Responsibility Checklist

Even with clean code, users should:

- [ ] Review the config files (`RM-Python-config.ini`) before running
- [ ] Verify the database paths and report paths point to expected locations
- [ ] Backup your RootsMagic database before running scripts that modify it
- [ ] Run scripts in a test environment first
- [ ] Keep Python and all system libraries up to date
- [ ] Only run scripts from trusted sources (this GitHub repo)
- [ ] Don't share your FamilySearch API token or database paths

---

## Recommendations

### For Repository Maintainer
1. ✅ Add a `SECURITY.md` file with this analysis
2. ✅ Consider adding digital signatures to releases
3. ✅ Document which scripts modify the database (they already do, but make it prominent)
4. ✅ Add Python version requirements to README

### For Script Users
1. ✅ Always run scripts on a **backup copy** of your database
2. ✅ Review the config file before execution
3. ✅ Check the generated report file after running
4. ✅ Verify expected database changes occurred

---

## Conclusion

**This repository is safe to use.** The code is:
- ✅ Transparent and readable
- ✅ Locally-focused (no hidden internet traffic)
- ✅ Purpose-driven for genealogy database management
- ✅ Properly logged and reported
- ✅ Uses standard library (minimal external dependencies)
- ✅ No obfuscation or suspicious patterns

The scripts are legitimate utilities for managing RootsMagic genealogy databases.

---

## About This Analysis

This static code analysis examined:
- 85 Python files across the repository
- Import patterns and module usage
- Network operations and subprocess calls
- File I/O operations
- Code obfuscation and suspicious patterns
- Dependency requirements

This analysis is **not a guarantee of safety**, but provides strong evidence of benign intent based on code inspection.

For the most current analysis, review the code directly on GitHub or run your own static analysis tools like:
- `bandit` (Python security linter)
- `pylint` (Code quality)
- Manual code review

---

**Analyst:** Copilot AI Assistant  
**Method:** Static Code Analysis  
**Confidence:** High ✅
