import json
import os
import re
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file if available
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Phishing & Malicious URL Scanner",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Cyber Security Aesthetic CSS
st.markdown(
    """
    <style>
    /* Global Styling */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* App Header Banner */
    .hero-banner {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.9) 100%);
        border: 1px solid rgba(59, 130, 246, 0.25);
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .hero-banner::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(59, 130, 246, 0.08) 0%, transparent 60%);
        pointer-events: none;
    }

    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #60a5fa, #38bdf8, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        font-weight: 400;
        margin: 0;
    }

    /* Risk Cards */
    .risk-card {
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    
    .risk-safe {
        background: linear-gradient(135deg, rgba(6, 78, 59, 0.35) 0%, rgba(6, 95, 70, 0.2) 100%);
        border: 1.5px solid #10b981;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.15);
    }

    .risk-suspicious {
        background: linear-gradient(135deg, rgba(120, 53, 15, 0.35) 0%, rgba(146, 64, 14, 0.2) 100%);
        border: 1.5px solid #f59e0b;
        box-shadow: 0 0 25px rgba(245, 158, 11, 0.15);
    }

    .risk-dangerous {
        background: linear-gradient(135deg, rgba(127, 29, 29, 0.45) 0%, rgba(153, 27, 27, 0.25) 100%);
        border: 1.5px solid #ef4444;
        box-shadow: 0 0 30px rgba(239, 68, 68, 0.25);
    }

    .risk-badge {
        display: inline-block;
        font-weight: 800;
        font-size: 0.95rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        padding: 6px 14px;
        border-radius: 9999px;
        margin-bottom: 12px;
    }

    .badge-safe {
        background-color: rgba(16, 185, 129, 0.2);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }

    .badge-suspicious {
        background-color: rgba(245, 158, 11, 0.2);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.4);
    }

    .badge-dangerous {
        background-color: rgba(239, 68, 68, 0.25);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.5);
    }

    /* Threat Indicator Card */
    .indicator-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(71, 85, 105, 0.4);
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 10px;
    }

    .severity-pill {
        display: inline-block;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 6px;
        text-transform: uppercase;
    }
    .sev-high { background: #ef4444; color: white; }
    .sev-med { background: #f59e0b; color: black; }
    .sev-low { background: #3b82f6; color: white; }

    /* Action Item Card */
    .action-card {
        background: rgba(15, 23, 42, 0.6);
        border-left: 4px solid #38bdf8;
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 8px;
        color: #e2e8f0;
    }
    
    /* Quick Samples Toolbar */
    .sample-pill {
        background-color: #1e293b;
        color: #cbd5e1;
        border: 1px solid #334155;
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 0.85rem;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------- Pre-loaded Samples for Quick Testing -----------------
SAMPLES = {
    "🚨 Netflix Phishing Email (Urgent Scam)": """From: support@netflix-account-security-update.com
Subject: URGENT: Your Netflix Subscription Has Been Suspended!
Date: Today

Dear Customer,

We were unable to process your monthly payment for your Netflix subscription. As a result, your streaming access has been temporarily suspended.

If you do not update your billing credentials and credit card information within the next 24 hours, your account and viewing profiles will be permanently deleted.

Click the secure link below to verify your payment immediately:
http://netflix-billing-portal.security-update-9482.xyz/login.php?user=verify

Thank you,
Netflix Support Team
    """,
    "🎣 Malicious PayPal URL": """hxxp://paypal-account-security-alert.verification-portal99.tk/cgi-bin/webscr?cmd=_login-run&dispatch=5885d80a13c0db1f&locale=en_US""",
    "📱 Urgent Bank SMS / Smishing": """[ALERT]: SBI / HDFC Bank: Your bank account will be blocked today due to pending KYC verification. Click here immediately to update PAN card: https://bit.ly/3kYc9-bank-update-kyc or call +91-9876543210.""",
    "✅ Legitimate Google Drive Email": """From: Google Drive <drive-shares-noreply@google.com>
Subject: Project Proposal 2026.pdf has been shared with you
Date: Today

Alice (alice.dev@company.org) has invited you to view the following document:

Project Proposal 2026.pdf

Open in Google Drive:
https://drive.google.com/file/d/1A2b3C4d5E6f7G8h9I0jKlMnOpQrSt/view?usp=sharing

Google LLC, 1600 Amphitheatre Parkway, Mountain View, CA 94043, USA
    """,
}

# ----------------- Mock Results for Demo Mode -----------------
def get_mock_analysis(content: str):
    """Provides instant high-fidelity security analysis without requiring an API key."""
    content_lower = content.lower()

    if "netflix-billing" in content_lower or "subscription has been suspended" in content_lower:
        return {
            "risk_level": "Dangerous",
            "threat_score": 96,
            "verdict_title": "Active Credential Harvesting Phishing Attack",
            "summary": "This is a classic credential harvesting email impersonating Netflix. It employs false urgency ('within 24 hours') and directs the recipient to a deceptive typo-squatted domain.",
            "phishing_indicators": [
                {
                    "category": "Domain Spoofing",
                    "severity": "High",
                    "description": "Sender domain 'netflix-account-security-update.com' is not official Netflix. Target URL uses suspicious TLD (.xyz) on an unverified domain.",
                },
                {
                    "category": "Urgency & Fear Tactics",
                    "severity": "High",
                    "description": "Threatens permanent deletion of account and profiles within 24 hours to cause panic and bypass critical thinking.",
                },
                {
                    "category": "Credential Harvesting",
                    "severity": "High",
                    "description": "Prompts user to re-enter billing credentials and credit card details on an unverified third-party link.",
                },
                {
                    "category": "Generic Greeting",
                    "severity": "Low",
                    "description": "Uses 'Dear Customer' instead of the account holder's registered name.",
                },
            ],
            "recommended_actions": [
                "DO NOT click the link or provide any payment details.",
                "Mark the email as Phishing / Spam in your mail client.",
                "If you entered credentials, change your real Netflix password immediately and freeze your card.",
                "Verify your account status by navigating directly to netflix.com in a new browser tab.",
            ],
            "technical_details": {
                "detected_urls": ["http://netflix-billing-portal.security-update-9482.xyz/login.php?user=verify"],
                "suspicious_keywords": ["suspended", "permanently deleted", "24 hours", "update payment", "urgent"],
                "impersonated_brand": "Netflix",
                "attack_vector": "Email Phishing (Credential Harvester)",
            },
        }
    elif "paypal" in content_lower or ".tk" in content_lower:
        return {
            "risk_level": "Dangerous",
            "threat_score": 98,
            "verdict_title": "Deceptive URL / PayPal Impersonation",
            "summary": "This URL mimics PayPal's legitimate login endpoint using subdomains and high-risk free TLDs (.tk) to steal user credentials and financial tokens.",
            "phishing_indicators": [
                {
                    "category": "Domain Spoofing",
                    "severity": "High",
                    "description": "Uses a deceptive free TLD (.tk) with 'paypal-account-security-alert' as a subdomain to fake legitimacy.",
                },
                {
                    "category": "Credential Harvesting",
                    "severity": "High",
                    "description": "Path mimics PayPal's internal CGI script ('/cgi-bin/webscr?cmd=_login-run') designed to capture login passwords.",
                },
                {
                    "category": "Suspicious URL/Redirect",
                    "severity": "Medium",
                    "description": "Defanged protocol notation and unusual host naming convention typical of bulletproof hosting.",
                },
            ],
            "recommended_actions": [
                "Do NOT open this URL under any circumstances.",
                "Report the URL to Google Safe Browsing and phish@paypal.com.",
                "Ensure your browser and DNS security filters (like Cloudflare 1.1.1.2) are active.",
            ],
            "technical_details": {
                "detected_urls": ["hxxp://paypal-account-security-alert.verification-portal99.tk/..."],
                "suspicious_keywords": ["verification", "security-alert", "webscr", "login-run"],
                "impersonated_brand": "PayPal",
                "attack_vector": "Malicious Website / Phishing URL",
            },
        }
    elif "google.com" in content_lower and "noreply@google.com" in content_lower:
        return {
            "risk_level": "Safe",
            "threat_score": 5,
            "verdict_title": "Legitimate Notification",
            "summary": "The email and link originate from verified Google infrastructure. Standard shared document notification with authentic headers and official HTTPS domains.",
            "phishing_indicators": [
                {
                    "category": "Sender Verification",
                    "severity": "Low",
                    "description": "Sender address 'drive-shares-noreply@google.com' matches legitimate Google Drive sharing service.",
                },
                {
                    "category": "Domain Authenticity",
                    "severity": "Low",
                    "description": "Target URL points to official 'drive.google.com' over secure TLS/HTTPS.",
                },
            ],
            "recommended_actions": [
                "Safe to view if you recognize the collaborator (Alice).",
                "Confirm that you were expecting this document before downloading or executing macros.",
            ],
            "technical_details": {
                "detected_urls": ["https://drive.google.com/file/d/1A2b3C4d5E6f7G8h9I0jKlMnOpQrSt/view?usp=sharing"],
                "suspicious_keywords": [],
                "impersonated_brand": "None (Authentic Google Drive)",
                "attack_vector": "Legitimate Communication",
            },
        }
    else:
        # Heuristic assessment for general inputs
        is_suspicious = any(k in content_lower for k in ["kyc", "pan", "bit.ly", "blocked", "urgent", "lottery", "winner", "prize", "otp"])
        risk = "Suspicious" if is_suspicious else "Safe"
        score = 68 if is_suspicious else 18
        return {
            "risk_level": risk,
            "threat_score": score,
            "verdict_title": f"{risk} Content Detected",
            "summary": "Simulated security evaluation. Identified potential social engineering cues and non-standard URL structures." if is_suspicious else "No obvious phishing or malicious characteristics identified in this sample.",
            "phishing_indicators": [
                {
                    "category": "Urgency & Tone" if is_suspicious else "Normal Content",
                    "severity": "Medium" if is_suspicious else "Low",
                    "description": "Text contains urgency keywords or short links commonly associated with spam/phishing." if is_suspicious else "Standard neutral tone without coercive triggers.",
                }
            ],
            "recommended_actions": [
                "Verify the sender's identity through an independent channel." if is_suspicious else "Standard vigilance is recommended.",
                "Never share OTP, passwords, or personal ID numbers." if is_suspicious else "Proceed as normal.",
            ],
            "technical_details": {
                "detected_urls": re.findall(r'https?://[^\s]+', content),
                "suspicious_keywords": [w for w in ["kyc", "blocked", "urgent", "verify", "link", "pan"] if w in content_lower],
                "impersonated_brand": "Unknown / Unspecified",
                "attack_vector": "Message / SMS" if len(content) < 250 else "General Text",
            },
        }


# ----------------- Gemini API Scanner -----------------
def analyze_with_gemini(api_key: str, model_name: str, content: str):
    """Calls Gemini API with structured prompt to analyze phishing/malicious content."""
    prompt = f"""
You are an elite Cybersecurity Threat Analyst specializing in phishing detection, malicious URL analysis, and social engineering countermeasures.

Perform a thorough security inspection of the following content (Email, SMS message, or URL):
\"\"\"
{content}
\"\"\"

Carefully evaluate:
1. SENDER & DOMAIN: Check for lookalike domains, typo-squatting, free/suspicious TLDs, mismatched display names vs email headers.
2. PSYCHOLOGICAL TRIGGERS: Urgent deadlines, threats of account suspension/arrest, excessive reward promises, artificial scarcity.
3. CREDENTIAL HARVESTING & LINKS: Requests for passwords, OTPs, credit cards, SSN/PAN, or links masked as legitimate services.
4. LANGUAGE & FORMAT: Odd grammatical constructs, generic greetings ("Dear Customer"), mismatched formatting.

Return your analysis strictly as a valid JSON object with the following schema:
{{
  "risk_level": "Safe" | "Suspicious" | "Dangerous",
  "threat_score": <integer from 0 to 100>,
  "verdict_title": "<Short punchy title, e.g. 'Active Credential Harvesting Phishing Email'>",
  "summary": "<2-3 sentence executive summary explaining the assessment clearly>",
  "phishing_indicators": [
    {{
      "category": "<Domain Spoofing | Urgency & Fear Tactics | Suspicious URL/Redirect | Credential Harvesting | Impersonation | Spelling & Grammar | Generic Greeting | Unusual Attachment>",
      "severity": "<High | Medium | Low>",
      "description": "<Specific detail observed in the content>"
    }}
  ],
  "recommended_actions": [
    "<Immediate action step 1>",
    "<Security precaution step 2>",
    "<Reporting or remediation step 3>"
  ],
  "technical_details": {{
    "detected_urls": ["<url1>", "<url2>"],
    "suspicious_keywords": ["<keyword1>", "<keyword2>"],
    "impersonated_brand": "<Brand name or 'None'>",
    "attack_vector": "<Email Phishing | Smishing (SMS) | Malicious Website/URL | Legitimate Communication>"
  }}
}}

Output ONLY the raw JSON string without any markdown code fences or conversational text.
"""

    # First attempt: modern google-genai SDK
    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.1,
            ),
        )
        text = response.text.strip()
        # Clean potential markdown fences if present
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        return json.loads(text)
    except Exception as e_new:
        # Fallback attempt: google-generativeai SDK
        try:
            import google.generativeai as legacy_genai

            legacy_genai.configure(api_key=api_key)
            model = legacy_genai.GenerativeModel(
                model_name=model_name,
                generation_config={"response_mime_type": "application/json", "temperature": 0.1},
            )
            response = model.generate_content(prompt)
            text = response.text.strip()
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```$", "", text)
            return json.loads(text)
        except Exception as e_legacy:
            raise RuntimeError(f"Gemini API call failed: {e_new} | Legacy fallback: {e_legacy}")


# ----------------- UI Layout & Controls -----------------

# Session State Initialization
if "scan_history" not in st.session_state:
    st.session_state.scan_history = []
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "current_result" not in st.session_state:
    st.session_state.current_result = None

# Sidebar Configuration
with st.sidebar:
    st.markdown("### ⚙️ Scanner Configuration")

    # API Key Input
    saved_key = os.getenv("GEMINI_API_KEY", "")
    api_key = st.text_input(
        "Gemini API Key",
        value=saved_key,
        type="password",
        help="Enter your Google Gemini API key. Get one free at aistudio.google.com",
    )

    demo_mode = False
    if not api_key:
        st.warning("⚠️ No API Key found. You can enter one above or enable Demo Mode below.")
        demo_mode = st.toggle("🧪 Demo Mode (Simulated AI Scan)", value=True)
    else:
        st.success("🟢 API Key Loaded")
        demo_mode = st.toggle("🧪 Force Demo Mode", value=False)

    st.markdown("---")

    # Model Selection
    model_name = st.selectbox(
        "Gemini Model",
        options=["gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
        index=0,
        help="Gemini 2.5 Flash is recommended for ultra-fast, intelligent threat detection.",
    )

    st.markdown("---")
    st.markdown("### 📚 Quick Test Samples")
    st.caption("Click any scenario to populate the scanner:")

    for title, sample_text in SAMPLES.items():
        if st.button(title, use_container_width=True):
            st.session_state.input_text = sample_text
            st.session_state.current_result = None
            st.rerun()

    st.markdown("---")
    if st.session_state.scan_history:
        st.markdown("### 🕒 Recent Scans")
        for item in reversed(st.session_state.scan_history[-5:]):
            st.caption(f"**{item['risk']}** ({item['score']}/100) - {item['time']}")
            st.text(item['preview'][:60] + "...")
        if st.button("Clear History", use_container_width=True):
            st.session_state.scan_history = []
            st.rerun()

    st.markdown("---")
    st.markdown(
        """
        <div style='font-size: 0.8rem; color: #64748b;'>
        <b>Phishing Red Flags Checklist:</b><br/>
        • Urgency or fear-inducing warnings<br/>
        • Mismatched URLs or odd domains<br/>
        • Requests for passwords or payment<br/>
        • Generic or impersonal greetings<br/>
        • Unsolicited attachments
        </div>
        """,
        unsafe_allow_html=True,
    )

# Hero Header
st.markdown(
    """
    <div class="hero-banner">
        <div class="hero-title">🛡️ AI Phishing & Malicious URL Scanner</div>
        <p class="hero-subtitle">
            Paste suspicious emails, SMS messages, or website URLs to perform real-time threat intelligence and vulnerability analysis powered by Google Gemini.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Main Input Section
col_left, col_right = st.columns([3, 1])
with col_left:
    st.markdown("#### 📥 Input Email Text or URL to Scan")
with col_right:
    if st.button("🧹 Clear Box", use_container_width=True):
        st.session_state.input_text = ""
        st.session_state.current_result = None
        st.rerun()

user_input = st.text_area(
    label="Email Body, SMS, or URL",
    value=st.session_state.input_text,
    placeholder="Paste email content, phishing SMS, or suspicious URL here...\nExample: URGENT: Your account has been suspended! Verify your details at http://...",
    height=180,
    label_visibility="collapsed",
)
st.session_state.input_text = user_input

# Scan Button
scan_col1, scan_col2, scan_col3 = st.columns([1, 2, 1])
with scan_col2:
    scan_clicked = st.button("🔍 Scan for Phishing & Malicious Threats", type="primary", use_container_width=True)

if scan_clicked:
    if not user_input.strip():
        st.error("⚠️ Please enter some email text, message, or a URL to scan.")
    else:
        with st.spinner("🕵️ Scanning content with Gemini AI Security Model..."):
            try:
                if demo_mode:
                    result = get_mock_analysis(user_input)
                else:
                    if not api_key:
                        st.error("❌ Gemini API Key is missing. Enter your key in the sidebar or toggle Demo Mode.")
                        st.stop()
                    result = analyze_with_gemini(api_key, model_name, user_input)

                st.session_state.current_result = result

                # Add to scan history
                from datetime import datetime
                st.session_state.scan_history.append({
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "risk": result.get("risk_level", "Unknown"),
                    "score": result.get("threat_score", 0),
                    "preview": user_input.replace("\n", " ")[:60],
                })
            except Exception as ex:
                st.error(f"❌ Analysis failed: {str(ex)}")
                st.info("💡 Tip: You can toggle 'Demo Mode' in the sidebar to test without an API key.")

# ----------------- Display Results -----------------
if st.session_state.current_result:
    res = st.session_state.current_result
    risk_level = res.get("risk_level", "Suspicious")
    threat_score = int(res.get("threat_score", 50))
    verdict_title = res.get("verdict_title", f"{risk_level} Content Detected")
    summary = res.get("summary", "No summary provided.")
    indicators = res.get("phishing_indicators", [])
    actions = res.get("recommended_actions", [])
    tech_details = res.get("technical_details", {})

    # Determine badge and styling
    risk_clean = risk_level.strip().capitalize()
    if risk_clean == "Safe":
        card_class = "risk-safe"
        badge_class = "badge-safe"
        badge_icon = "✅"
        gauge_color = "#10b981"
    elif risk_clean == "Dangerous":
        card_class = "risk-dangerous"
        badge_class = "badge-dangerous"
        badge_icon = "🚨"
        gauge_color = "#ef4444"
    else:
        card_class = "risk-suspicious"
        badge_class = "badge-suspicious"
        badge_icon = "⚠️"
        gauge_color = "#f59e0b"

    st.markdown("---")
    st.markdown("### 📊 Security Threat Assessment")

    # Primary Verdict Banner
    st.markdown(
        f"""
        <div class="risk-card {card_class}">
            <div class="risk-badge {badge_class}">{badge_icon} RISK LEVEL: {risk_clean.upper()}</div>
            <h2 style="margin: 0 0 10px 0; font-size: 1.6rem; font-weight: 700; color: #f8fafc;">
                {verdict_title}
            </h2>
            <p style="font-size: 1.05rem; line-height: 1.6; color: #e2e8f0; margin: 0;">
                {summary}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Metrics Row
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.metric("Threat Score", f"{threat_score}/100", delta=f"{'High Risk' if threat_score > 65 else 'Moderate' if threat_score > 20 else 'Low Risk'}", delta_color="inverse")
    with m_col2:
        st.metric("Risk Classification", risk_clean)
    with m_col3:
        st.metric("Indicators Found", len(indicators))
    with m_col4:
        impersonated = tech_details.get("impersonated_brand", "None")
        st.metric("Target / Brand", impersonated if impersonated else "None")

    # Threat Score Progress Bar
    st.markdown(f"**Threat Severity Index:** {threat_score}%")
    st.progress(threat_score / 100.0)

    st.write("")

    # Detailed Analysis Tabs
    tab_indicators, tab_actions, tab_technical = st.tabs([
        "🚩 Phishing Indicators Detected",
        "🛡️ Recommended Security Actions",
        "🔍 Technical Breakdown & Evidence",
    ])

    # Tab 1: Phishing Indicators
    with tab_indicators:
        if indicators:
            st.markdown(f"#### Identified {len(indicators)} Key Red Flag(s):")
            for ind in indicators:
                cat = ind.get("category", "General")
                sev = ind.get("severity", "Medium").capitalize()
                desc = ind.get("description", "")
                sev_cls = "sev-high" if sev == "High" else "sev-med" if sev == "Medium" else "sev-low"

                st.markdown(
                    f"""
                    <div class="indicator-card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                            <span style="font-weight: 700; font-size: 1rem; color: #f1f5f9;">📌 {cat}</span>
                            <span class="severity-pill {sev_cls}">{sev} Severity</span>
                        </div>
                        <div style="color: #94a3b8; font-size: 0.95rem; line-height: 1.5;">{desc}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.success("✅ No malicious or suspicious indicators detected in this content.")

    # Tab 2: Recommended Actions
    with tab_actions:
        st.markdown("#### Recommended Next Steps:")
        if actions:
            for i, act in enumerate(actions, 1):
                st.markdown(
                    f"""
                    <div class="action-card">
                        <b style="color: #38bdf8;">Step {i}:</b> {act}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No specific mitigation actions required. Maintain standard security awareness.")

    # Tab 3: Technical Breakdown
    with tab_technical:
        st.markdown("#### Extracted Technical Artifacts:")
        tech_col1, tech_col2 = st.columns(2)

        with tech_col1:
            st.markdown("**Detected URLs / Links:**")
            detected_urls = tech_details.get("detected_urls", [])
            if detected_urls:
                for url in detected_urls:
                    st.code(url, language="text")
            else:
                st.write("None extracted from text.")

            st.markdown("**Attack Vector:**")
            st.info(tech_details.get("attack_vector", "Unknown"))

        with tech_col2:
            st.markdown("**Trigger Keywords:**")
            keywords = tech_details.get("suspicious_keywords", [])
            if keywords:
                st.write(", ".join([f"`{k}`" for k in keywords]))
            else:
                st.write("No high-risk keywords flagged.")

            st.markdown("**Targeted Brand / Entity:**")
            st.write(f"**{tech_details.get('impersonated_brand', 'None')}**")

        with st.expander("🛠️ View Raw JSON Security Telemetry"):
            st.json(res)
