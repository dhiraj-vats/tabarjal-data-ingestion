# FNS Tabarjal - Application Run Guide

This document explains how to set up and run the FNS Tabarjal FastAPI application on a Windows system.

---

## 1. Recommended Folder Structure

Create one common folder in `C:` drive:

```text
C:\FNS-TABARJAL
```

Suggested sub-folders:

```text
C:\FNS-TABARJAL\webapp
C:\FNS-TABARJAL\data-ingestion
C:\FNS-TABARJAL\forwarder
C:\FNS-TABARJAL\logs
C:\FNS-TABARJAL\backups
```

For data ingestion service:

```text
C:\FNS-TABARJAL\data-ingestion
```

---

## 2. Clone Git Repository

Open CMD and go to the project folder:

```bat
cd C:\FNS-TABARJAL
```

Clone the repository:

```bat
git clone git@github.com:dhiraj-vats/tabarjal-data-ingestion.git data-ingestion
```

Go inside the project:

```bat
cd C:\FNS-TABARJAL\data-ingestion
```

---

## 3. Check Python Version

Recommended Python version: **Python 3.12**

Check Python:

```bat
python --version
```

Or:

```bat
py -3.12 --version
```

Expected output example:

```text
Python 3.12.x
```

---

## 4. Create Virtual Environment

Run this command from the project root folder:

```bat
py -3.12 -m venv .venv
```

If only one Python version is installed, this can also be used:

```bat
python -m venv .venv
```

---

## 5. Activate Virtual Environment

For Windows CMD:

```bat
.venv\Scripts\activate
```

After activation, CMD should look like this:

```text
(.venv) C:\FNS-TABARJAL\data-ingestion>
```

---

## 6. Install Required Packages

Install all dependencies:

```bat
pip install -r requirements.txt
```

If pip needs upgrade:

```bat
python -m pip install --upgrade pip
```

Then again run:

```bat
pip install -r requirements.txt
```

---

## 7. Run FastAPI Application

Run the application using uvicorn:

```bat
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

If running in production/client system, use without reload:

```bat
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 8. Open Application in Browser

Local URL:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

OpenAPI JSON:

```text
http://127.0.0.1:8000/openapi.json
```

---

## 9. If Uvicorn Command Not Found

Use this command instead of direct `uvicorn`:

```bat
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Or install uvicorn manually:

```bat
pip install uvicorn
```

---

## 10. If Requirements Changed

If `requirements.txt` is updated, activate venv and run:

```bat
pip install -r requirements.txt
```

To force reinstall packages:

```bat
pip install --force-reinstall --no-cache-dir -r requirements.txt
```

---

## 11. Check Installed Packages

```bat
pip list
```

Check dependency issues:

```bat
pip check
```

---

## 12. Stop Application

Press:

```text
CTRL + C
```

---

## 13. Deactivate Virtual Environment

```bat
deactivate
```

---

## 14. Fresh Setup Again

If virtual environment is corrupted, remove and recreate:

```bat
deactivate
rmdir /s /q .venv
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 15. Common Important Commands

```bat
cd C:\FNS-TABARJAL\data-ingestion
.venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Notes

- Always activate `.venv` before installing packages or running the application.
- Use Python 3.12 for better compatibility.
- Use `python -m uvicorn` instead of direct `uvicorn` to avoid PATH issues.
- Swagger documentation will be available at `/docs`.
