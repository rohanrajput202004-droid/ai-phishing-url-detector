# 🛡️ AI-Powered Phishing & Malicious URL Scanner

A modern cybersecurity analysis application built with **Streamlit** and **Google Gemini AI**. It enables users to scan suspicious emails, SMS messages, and URLs in real time to detect phishing attacks, social engineering tricks, credential harvesting, and malicious redirects.

---

## 🌟 Key Features

1. **Dual Scanning Support**:
   - Paste full email bodies (including sender headers, subject line, links).
   - Paste raw or defanged URLs (e.g. `http://...`, `hxxp://...`).
   - Paste SMS / WhatsApp smishing messages.

2. **AI Threat Intelligence (Powered by Gemini)**:
   - **Risk Classification**: Color-coded badges for **Safe (🟢)**, **Suspicious (🟡)**, and **Dangerous (🔴)**.
   - **Threat Severity Index**: 0 to 100 severity meter.
   - **Phishing Indicators**: Granular detection tags (Domain Spoofing, Urgency/Fear Tactics, Credential Harvesters, Generic Greetings, etc.).
   - **Actionable Defense Recommendations**: Step-by-step guidance on what to do immediately.
   - **Technical Telemetry**: Extracted URLs, trigger keywords, attack vector classification, and targeted brand detection.

3. **Built-in Quick Test Samples**:
   - Preloaded realistic attack scenarios (Netflix suspension scam, PayPal credential harvesting URL, Bank KYC SMS alert, and legitimate Google Drive share).

4. **Offline / Demo Mode**:
   - Allows instant testing without entering an API key.

---

## 🚀 Quick Start Guide

### 1. Setup Virtual Environment & Install Dependencies
Open PowerShell or your terminal in this project directory:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 2. Configure Gemini API Key (Optional)
You can configure your API key in two ways:
- **Option A (Environment Variable)**: Create a `.env` file from `.env.example`:
  ```env
  GEMINI_API_KEY=your_gemini_api_key_here
  ```
- **Option B (Direct in App)**: Enter it directly in the app sidebar input.

*(You can get a free Gemini API Key from [Google AI Studio](https://aistudio.google.com/app/apikey)).*

### 3. Run the Streamlit Application
```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

The application will launch automatically in your browser at `http://localhost:8501`.
