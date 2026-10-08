# WebSecAI 🛡️

### AI-Powered Web Security Assistant

> Turn security evidence into clear, actionable security insights.

WebSecAI is an open-source, AI-powered web security assistant that performs non-destructive security configuration checks on an authorized website and uses the open-weight **Gemma 3:4b** model to explain the findings in simple, actionable language.

Built for **Hacktoberfest Hack Day 2026**.

---

## 🚀 Overview

Web security findings are often difficult to understand, especially for beginners and developers who are not security specialists.

WebSecAI combines automated security checks with AI-generated explanations.

A user provides an authorized website URL, and WebSecAI:

1. Retrieves the website response.
2. Analyzes security-related HTTP headers.
3. Checks cookie security attributes.
4. Checks selected CORS configuration.
5. Sends the detected evidence to Gemma.
6. Generates an explanation containing the issue, impact, and recommended fix.
7. Displays the results through a simple web interface.

WebSecAI focuses on **evidence-based defensive analysis** and does not perform destructive exploitation.

---

## ✨ Features

### 🔍 Security Header Analysis

WebSecAI checks for the presence of important security headers, including:

- Content-Security-Policy
- Strict-Transport-Security
- X-Content-Type-Options
- X-Frame-Options
- Referrer-Policy
- Permissions-Policy

Detected missing headers are assigned a severity and accompanied by a recommendation.

### 🍪 Cookie Security Analysis

WebSecAI checks `Set-Cookie` headers for:

- Secure
- HttpOnly
- SameSite

The tool reports missing cookie security attributes and provides recommendations.

### 🌐 CORS Analysis

WebSecAI checks selected CORS configuration and identifies potentially broad configurations such as:

- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Origin: null`

### 🤖 Gemma AI Analysis

Detected security findings are provided as evidence to the local **Gemma 3:4b** model through Ollama.

Gemma generates:

- Issue
- Impact
- Fix

The AI is instructed to use only the supplied security evidence and avoid inventing vulnerabilities.

### 💻 Web Interface

The project includes a simple frontend that allows users to:

- Enter an authorized target URL
- Start a security scan
- View security findings
- View severity levels
- Read recommendations
- View Gemma AI analysis

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │     Web Browser     │
                    │   WebSecAI Frontend │
                    └──────────┬──────────┘
                               │
                               │ POST /scan
                               ▼
                    ┌─────────────────────┐
                    │    FastAPI Backend  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Security Scanner  │
                    ├─────────────────────┤
                    │ Security Headers     │
                    │ Cookies              │
                    │ CORS                 │
                    └──────────┬──────────┘
                               │
                               │ Security Evidence
                               ▼
                    ┌─────────────────────┐
                    │     Gemma 3:4b      │
                    │   via Local Ollama  │
                    └──────────┬──────────┘
                               │
                               │ AI Explanation
                               ▼
                    ┌─────────────────────┐
                    │    WebSecAI UI      │
                    │ Findings + AI Fixes │
                    └─────────────────────┘
```

---

## 🛠️ Technology Stack

### Backend

- Python
- FastAPI
- Pydantic
- HTTPX

### Security Analysis

- Security HTTP headers
- Cookie security attributes
- CORS configuration

### AI

- Gemma 3:4b
- Ollama
- Local AI inference

### Frontend

- HTML
- CSS
- JavaScript

### API Documentation

FastAPI provides interactive API documentation through Swagger UI.

---

## 📁 Project Structure

```text
websecai/
│
├── backend/
│   ├── ai/
│   │   └── gemma.py
│   │
│   ├── scanner/
│   │   ├── cookies.py
│   │   ├── cors.py
│   │   ├── security_headers.py
│   │   └── scanner.py
│   │
│   └── main.py
│
├── frontend/
│   ├── app.js
│   ├── index.html
│   └── style.css
│
├── LICENSE
├── README.md
└── requirements.txt
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/SachinAditya/websecai.git
cd websecai
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

#### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install Python dependencies

```bash
pip install -r requirements.txt
```

---

## 🤖 Gemma and Ollama Setup

WebSecAI uses the open-weight **Gemma 3:4b** model locally through Ollama.

Make sure Ollama is installed and running on your system.

Pull the required model:

```bash
ollama pull gemma3:4b
```

Verify that the model is available:

```bash
ollama list
```

The application expects the local Ollama API at:

```text
http://127.0.0.1:11434
```

WebSecAI sends security findings to the local Gemma model for explanation.

---

## ▶️ Running the Backend

From the project root, activate your virtual environment and run:

```bash
uvicorn backend.main:app --reload
```

The FastAPI backend will be available at:

```text
http://127.0.0.1:8000
```

### Health Check

Open:

```text
http://127.0.0.1:8000/health
```

A healthy API returns:

```json
{
    "status": "healthy"
}
```

### Swagger API Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI can be used to test the available API endpoints.

---

## 🌐 Running the Frontend

Open a **second terminal** from the project root.

Run:

```bash
python -m http.server 5500 --directory frontend
```

The frontend will be available at:

```text
http://127.0.0.1:5500
```

Open the address in your browser.

You should see the WebSecAI interface.

---

## 🔎 Using WebSecAI

1. Start Ollama and make sure `gemma3:4b` is available.
2. Start the FastAPI backend.
3. Start the frontend server.
4. Open the WebSecAI frontend.
5. Enter an authorized target URL.
6. Click **Scan Website**.
7. WebSecAI retrieves the target response.
8. The scanner analyzes the available security evidence.
9. The findings are sent to Gemma.
10. The frontend displays the security findings and AI-generated analysis.

### Example

For testing, you can use:

```text
https://example.com
```

Only use targets that you own or have explicit permission to test.

---

## 📊 Example Finding

A missing security header may be displayed as:

```text
Content-Security-Policy

Severity: Medium

Helps control which resources browsers are allowed to load.

Recommendation:
Consider configuring the Content-Security-Policy header.
```

Gemma then provides an explanation based on the detected evidence:

```text
Issue
Impact
Fix
```

---

## 🔐 Security and Authorized Use

WebSecAI is designed for **authorized defensive security analysis only**.

Only scan:

- Websites you own
- Applications you are authorized to test
- Systems where you have explicit permission

Do **not** use WebSecAI for:

- Unauthorized scanning
- Exploitation
- Credential attacks
- Brute-force attacks
- Destructive testing
- Attacks against systems without permission

The current WebSecAI MVP focuses on **non-destructive security configuration analysis**.

The user is responsible for ensuring that every target scanned with WebSecAI is authorized for testing.

---

## 🎯 Project Goals

WebSecAI aims to make web security analysis easier to understand by combining:

```text
Security Evidence
       +
Automated Analysis
       +
Open-Weight AI
       ↓
Clear Security Guidance
```

Instead of simply reporting a technical security finding, WebSecAI helps answer:

```text
What is wrong?
      ↓
Why does it matter?
      ↓
How can it be improved?
```

---

## 🧪 Current MVP

The current MVP includes:

- ✅ FastAPI backend
- ✅ URL validation
- ✅ Security header analysis
- ✅ Cookie security analysis
- ✅ CORS analysis
- ✅ Gemma 3:4b integration
- ✅ Local Ollama inference
- ✅ AI-generated security explanations
- ✅ Web frontend
- ✅ Frontend-to-backend integration
- ✅ Interactive Swagger API documentation
- ✅ CORS support for local frontend development

---

## 🔮 Future Improvements

Potential future improvements include:

- Security scoring
- Finding prioritization
- Additional HTTP security checks
- More advanced cookie analysis
- More detailed CORS analysis
- Exportable security reports
- Improved AI explanations
- Additional open-weight model support
- Improved frontend visualization
- Additional security configuration checks
- More detailed evidence collection

---

## 🏆 Hack Day

WebSecAI was developed for:

**Hacktoberfest Hack Day 2026**

### Track

**Best Open-Source AI Project**

The project uses the open-weight **Gemma 3:4b** model locally through Ollama to transform technical web security evidence into understandable security guidance.

---


## ⭐ Contributing

Contributions, suggestions, bug reports, and improvements are welcome.

If you find WebSecAI useful, consider giving the repository a ⭐ on GitHub.
