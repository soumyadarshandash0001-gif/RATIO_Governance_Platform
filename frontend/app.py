"""RATIO Governance Certification Platform - Streamlit Frontend."""
import streamlit as st
import requests
import json
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time

# Configure page
st.set_page_config(
    page_title="RATIO Governance Certification Platform",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ===== CONFIG =====
API_BASE_URL = "http://localhost:8000/api/v1"
st.session_state.setdefault("authenticated", False)
st.session_state.setdefault("current_audit", None)

# ===== STYLING =====
st.markdown("""
<style>
    .main-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
    }
    .score-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
    }
    .tier-controlled {
        background-color: #1b5e20;
        color: white;
        padding: 10px 15px;
        border-radius: 5px;
    }
    .tier-production {
        background-color: #0d47a1;
        color: white;
        padding: 10px 15px;
        border-radius: 5px;
    }
    .tier-enterprise {
        background-color: #4a148c;
        color: white;
        padding: 10px 15px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ===== HEADER =====
st.markdown("""
<div class="main-title">
    <h1>🏛️ RATIO Governance Certification Platform</h1>
    <p>Institutional-grade AI governance audit and certification ecosystem</p>
    <p style="font-size: 12px; margin-top: 10px;">
        Built by: <strong>Soumyadarshan Dash</strong>, <strong>Pranita Jagtap</strong>, <strong>Ramdev Chaudhary</strong>
    </p>
</div>
""", unsafe_allow_html=True)

# ===== SIDEBAR NAVIGATION =====
with st.sidebar:
    st.logo("🏛️")
    st.title("Navigation")
    
    page = st.radio(
        "Select page:",
        [
            "Dashboard",
            "Register Model",
            "Run Audit",
            "View Results",
            "Share Audit",
            "Governance Advisory",
            "Monitoring",
            "Verify Certificate",
        ],
        label_visibility="collapsed",
    )

# ===== PAGE: DASHBOARD =====
if page == "Dashboard":
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Models Registered", 0, delta=None)
    with col2:
        st.metric("Audits Completed", 0, delta=None)
    with col3:
        st.metric("Certifications Issued", 0, delta=None)
    
    st.subheader("Platform Overview")
    st.info("""
    **RATIO** is a production-grade AI governance audit and certification platform that:
    
    - 🔌 **Connects to any AI model** (OpenAI, Anthropic, Google, HuggingFace, Replicate, custom)
    - 🧪 **Runs 40+ deterministic governance tests** across 8 categories
    - 📊 **Measures objective governance metrics** (Security, Reliability, Fairness, etc.)
    - 🏆 **Issues institutional-grade certifications** (Controlled, Production, Enterprise)
    - 🤖 **Provides governance advisory** via Llama 3.2
    - 📈 **Monitors score drift** with auto-revocation
    - 🌍 **Aligns with global AI safety standards** (EU AI Act, NIST, OECD, ISO)
    """)
    
    # Feature matrix
    st.subheader("Core Capabilities")
    features = {
        "Universal Model Connector": "✓ OpenAI, Anthropic, Google, HuggingFace, Replicate, Custom",
        "Governance Test Suite": "✓ 40+ deterministic tests across 8 categories",
        "Rule-Based Evaluation": "✓ Deterministic scoring with Llama 3.2 judge",
        "RATIO Scoring (0-900)": "✓ Weighted across 6 dimensions",
        "Executive Reports": "✓ Structured JSON with compliance metadata",
        "Certification Authority": "✓ Tamper-resistant badges with QR codes",
        "Advisory Chatbot": "✓ Llama 3.2-powered governance guidance",
        "Monitoring & Drift": "✓ Auto-revocation on threshold breach",
    }
    
    for feature, status in features.items():
        st.text(f"{feature}: {status}")


# ===== PAGE: REGISTER MODEL =====
elif page == "Register Model":
    st.subheader("Register AI Model for Audit")
    
    with st.form("model_registration"):
        col1, col2 = st.columns(2)
        
        with col1:
            provider_type = st.selectbox(
                "Model Provider",
                ["openai", "anthropic", "google", "huggingface", "replicate", "custom_http"],
            )
            model_identifier = st.text_input("Model Identifier (e.g., gpt-4, claude-3)")
            display_name = st.text_input("Display Name")
        
        with col2:
            api_key = st.text_input("API Key", type="password")
            endpoint_url = st.text_input("Endpoint URL (if custom)")
            max_tokens = st.number_input("Max Tokens", value=1000, min_value=100)
        
        description = st.text_area("Model Description")
        
        submitted = st.form_submit_button("Register Model")
        
        if submitted:
            try:
                response = requests.post(
                    f"{API_BASE_URL}/models/register",
                    json={
                        "provider_type": provider_type,
                        "model_identifier": model_identifier,
                        "display_name": display_name,
                        "api_key": api_key,
                        "endpoint_url": endpoint_url,
                        "max_tokens": max_tokens,
                        "description": description,
                    },
                )
                result = response.json()
                
                if result.get("success"):
                    st.success(f"✓ Model registered: {result['model_uuid']}")
                    st.info(f"Verification: {result['message']}")
                else:
                    st.error(f"❌ Registration failed: {result['message']}")
            
            except Exception as e:
                st.error(f"Error: {str(e)}")


# ===== PAGE: RUN AUDIT =====
elif page == "Run Audit":
    st.subheader("Execute Governance Audit")
    
    col1, col2 = st.columns(2)
    
    with col1:
        model_uuid = st.text_input("Model UUID")
        model_name = st.text_input("Model Display Name")
    
    with col2:
        st.write("")
        st.write("")
        run_audit = st.button("🚀 Start Audit", use_container_width=True)
    
    if run_audit:
        if not model_uuid or not model_name:
            st.error("Please provide Model UUID and Display Name")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.text("🔄 Executing governance tests...")
                
                response = requests.post(
                    f"{API_BASE_URL}/audits/execute",
                    json={
                        "model_uuid": model_uuid,
                        "model_name": model_name,
                    },
                    timeout=300,
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.current_audit = result
                    
                    progress_bar.progress(100)
                    status_text.text("✓ Audit complete!")
                    
                    # Display results
                    st.success("Audit completed successfully!")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric(
                            "AI TRUST SCORE",
                            f"{result.get('ai_trust_score', 0):.0f}/900",
                            delta=None,
                        )
                    with col2:
                        st.metric("Risk Tier", result.get("risk_tier", "Unknown"))
                    with col3:
                        st.metric("Eligibility", result.get("eligibility_level", "Unknown"))
                    with col4:
                        st.metric("Tests Passed", f"{result.get('tests_passed', 0)}/{result.get('tests_total', 0)}")
                    
                    # Certification status
                    if result.get("certification_issued"):
                        st.success(f"✓ Certification issued: {result['certification_id']}")
                    
                    # Store audit
                    st.session_state.current_audit = result
                    st.info("Audit results saved to session")
                
                else:
                    st.error(f"Audit failed: {response.text}")
            
            except Exception as e:
                st.error(f"Error: {str(e)}")


# ===== PAGE: VIEW RESULTS =====
elif page == "View Results":
    st.subheader("Audit Results & Report")
    
    if st.session_state.current_audit:
        audit_data = st.session_state.current_audit
        
        # Score visualization
        col1, col2 = st.columns([2, 1])
        
        with col1:
            report = audit_data.get("report", {})
            sections = report.get("section_c_dimensions", {})
            dimensions_data = sections.get("dimensions", {})
            
            # Radar chart
            dim_names = list(dimensions_data.keys())
            dim_scores = [dimensions_data[d].get("score", 0) for d in dim_names]
            
            fig = go.Figure(data=go.Scatterpolar(
                r=dim_scores,
                theta=dim_names,
                fill='toself',
                name='Governance Scores',
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                height=400,
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Dimension Scores**")
            for dim_name, dim_data in dimensions_data.items():
                score = dim_data.get("score", 0)
                status = dim_data.get("status", "")
                st.write(f"{dim_name.capitalize()}: {score:.0f}/100 {status}")
        
        # Executive summary
        st.subheader("Executive Summary")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            overview = report.get("section_a_overview", {})
            st.write(f"**Model**: {overview.get('model_name')}")
            st.write(f"**Provider**: {overview.get('provider')}")
            st.write(f"**Tests**: {overview.get('test_count')}")
        with col2:
            score_data = report.get("section_b_score", {})
            st.write(f"**Score**: {score_data.get('ai_trust_score'):.0f}/900")
            st.write(f"**Risk Tier**: {score_data.get('risk_tier')}")
            st.write(f"**Eligible**: {score_data.get('eligibility_level')}")
        with col3:
            risk_data = report.get("section_d_risk", {})
            st.write(f"**Review Required**: {risk_data.get('human_review_required')}")
            if risk_data.get('critical_gaps'):
                st.warning(f"Critical Gaps: {len(risk_data.get('critical_gaps', []))}")
        
        # Recommendations
        st.subheader("Improvement Recommendations")
        roadmap = report.get("section_e_roadmap", {})
        for i, rec in enumerate(roadmap.get("priority_actions", []), 1):
            st.info(f"{i}. {rec}")
        
        # SHAREABLE LINK SECTION
        st.divider()
        st.subheader("📤 Share Audit Results")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("🔗 Generate Shareable Link", use_container_width=True, key="share_btn"):
                try:
                    audit_id = audit_data.get("audit_id", "audit-demo")
                    response = requests.post(
                        f"{API_BASE_URL}/audits/share",
                        params={"audit_id": audit_id},
                    )
                    
                    if response.status_code == 200:
                        share_result = response.json()
                        share_url = share_result.get("public_link", "")
                        shareable_id = share_result.get("shareable_id", "")
                        
                        st.session_state.shareable_link = share_url
                        st.session_state.shareable_id = shareable_id
                        
                        st.success("✓ Shareable link created!")
                    else:
                        st.error("Failed to create shareable link")
                except Exception as e:
                    st.error(f"Error creating link: {str(e)}")
        
        # Display shareable link if exists
        if hasattr(st.session_state, 'shareable_link') and st.session_state.shareable_link:
            st.info("**Share this link with stakeholders to view audit results:**")
            
            share_link = st.session_state.shareable_link
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.code(share_link, language="text")
            
            with col2:
                st.caption("Link expires in 90 days")
            
            with col3:
                if st.button("📋 Copy"):
                    st.write("Link copied! You can share it now.")
            
            # Sharing options
            st.write("**Share on:**")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                mailto_link = f"mailto:?subject=RATIO%20Audit%20Results&body={share_link}"
                st.markdown(f"[📧 Email]({mailto_link})")
            
            with col2:
                twitter_link = f"https://twitter.com/intent/tweet?text=Check%20RATIO%20Audit%20Results%20{share_link}"
                st.markdown(f"[🐦 Twitter]({twitter_link})")
            
            with col3:
                linkedin_link = f"https://www.linkedin.com/sharing/share-offsite/?url={share_link}"
                st.markdown(f"[💼 LinkedIn]({linkedin_link})")
            
            with col4:
                st.markdown(f"[🔗 Copy Link]({share_link})")
        
        # Full report JSON
        with st.expander("View Full JSON Report"):
            st.json(report)
    
    else:
        st.info("Run an audit first to view results")


# ===== PAGE: SHARE AUDIT =====
elif page == "Share Audit":
    st.subheader("📤 Share Audit Results with Stakeholders")
    
    st.write("""
    Generate a shareable link for your audit results that stakeholders can view without authentication.
    Shared audits are public and expire after 90 days.
    """)
    
    if st.session_state.current_audit:
        audit_data = st.session_state.current_audit
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.info(f"""
            **Model:** {audit_data.get('model_name', 'Unknown')}  
            **Score:** {audit_data.get('ai_trust_score', 0):.0f}/900  
            **Status:** {audit_data.get('risk_tier', 'Unknown')}
            """)
        
        with col2:
            st.metric("Certification ID", audit_data.get("certification_id", "N/A"))
        
        st.divider()
        
        # Create shareable link
        if st.button("🔗 Generate Shareable Link", use_container_width=True, key="share_main"):
            try:
                audit_id = audit_data.get("audit_id", "audit-demo")
                response = requests.post(
                    f"{API_BASE_URL}/audits/share",
                    params={"audit_id": audit_id},
                )
                
                if response.status_code == 200:
                    share_result = response.json()
                    share_url = share_result.get("public_link", "")
                    shareable_id = share_result.get("shareable_id", "")
                    
                    st.session_state.shareable_link = share_url
                    st.session_state.shareable_id = shareable_id
                    
                    st.success("✅ Shareable link created successfully!")
                    st.balloons()
                else:
                    st.error("Failed to create shareable link")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        # Display link and sharing options
        if hasattr(st.session_state, 'shareable_link') and st.session_state.shareable_link:
            st.markdown("---")
            st.subheader("✅ Your Shareable Link")
            
            share_link = st.session_state.shareable_link
            
            # Display link
            st.markdown("""
            <div style="background-color: #f0f2f6; padding: 15px; border-radius: 8px; margin: 10px 0;">
                <p style="margin: 0; color: #666;">Share this link with stakeholders:</p>
                <p style="margin: 5px 0; font-family: monospace; font-size: 14px; word-break: break-all;">
                    <strong>""" + share_link + """</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Copy button
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📋 Copy to Clipboard", use_container_width=True):
                    st.success("Link copied! Paste it anywhere to share.")
            
            with col2:
                if st.button("🔄 Generate New Link", use_container_width=True):
                    del st.session_state.shareable_link
                    st.rerun()
            
            with col3:
                if st.button("ℹ️ Link Info", use_container_width=True):
                    st.info("""
                    **Link Details:**
                    - Expires in: 90 days
                    - Public access: Yes
                    - No authentication required
                    - View-only (cannot modify results)
                    """)
            
            st.markdown("---")
            st.subheader("📢 Share On Social Media")
            
            share_text = f"Check out the RATIO AI Governance Audit for {audit_data.get('model_name')} - Score: {audit_data.get('ai_trust_score', 0):.0f}/900"
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                email_link = f"mailto:?subject=RATIO%20Audit%20Results&body={share_text}%20{share_link}"
                st.markdown(f"[📧 **Email**]({email_link})", unsafe_allow_html=True)
            
            with col2:
                twitter_text = f"{share_text}".replace(" ", "%20")
                twitter_link = f"https://twitter.com/intent/tweet?text={twitter_text}%20{share_link}"
                st.markdown(f"[🐦 **Twitter**]({twitter_link})", unsafe_allow_html=True)
            
            with col3:
                linkedin_link = f"https://www.linkedin.com/sharing/share-offsite/?url={share_link}"
                st.markdown(f"[💼 **LinkedIn**]({linkedin_link})", unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"[🔗 **Open Link**]({share_link})", unsafe_allow_html=True)
            
            st.markdown("---")
            st.subheader("📝 Pre-written Messages")
            
            # Email template
            with st.expander("📧 Email Template"):
                email_msg = f"""Subject: RATIO AI Governance Audit Results - {audit_data.get('model_name')}

Hi,

I wanted to share the RATIO AI Governance Audit results for {audit_data.get('model_name')}:

🎯 AI Trust Score: {audit_data.get('ai_trust_score', 0):.0f}/900
📊 Risk Tier: {audit_data.get('risk_tier', 'Unknown')}
✅ Certification: {audit_data.get('certification_id', 'N/A')}

View the full audit results here: {share_link}

RATIO audits AI models against 40+ governance tests across 8 risk categories to ensure enterprise-grade safety and compliance.

Best regards"""
                st.code(email_msg, language="text")
                if st.button("📋 Copy Email Message"):
                    st.success("Email message copied!")
            
            # LinkedIn template
            with st.expander("💼 LinkedIn Post"):
                linkedin_msg = f"""🏛️ We just audited {audit_data.get('model_name')} with RATIO - an AI governance certification platform.

Results:
✅ AI Trust Score: {audit_data.get('ai_trust_score', 0):.0f}/900
📊 Risk Tier: {audit_data.get('risk_tier', 'Unknown')}
🎯 Certified: {audit_data.get('eligibility_level', 'Unknown')}

View detailed audit: {share_link}

#AI #Governance #Safety #Certification #RATIO"""
                st.code(linkedin_msg, language="text")
                if st.button("📋 Copy LinkedIn Post"):
                    st.success("LinkedIn post copied!")
            
            # Tweet template
            with st.expander("🐦 Twitter Post"):
                tweet_msg = f"""✅ {audit_data.get('model_name')} audited with RATIO!

🎯 Score: {audit_data.get('ai_trust_score', 0):.0f}/900
📊 Risk: {audit_data.get('risk_tier', 'Unknown')}

View results: {share_link}

#AI #Governance #Safety"""
                st.code(tweet_msg, language="text")
                if st.button("📋 Copy Tweet"):
                    st.success("Tweet copied!")
    
    else:
        st.warning("⚠️ No audit results to share")
        st.info("👉 Go to 'Run Audit' first to generate audit results, then come back here to share them.")


# ===== PAGE: GOVERNANCE ADVISORY =====
elif page == "Governance Advisory":
    st.subheader("🤖 RATIO Governance Advisory Assistant")
    
    if st.session_state.current_audit:
        st.info(
            f"Advising on: {st.session_state.current_audit.get('model_name')} "
            f"(Score: {st.session_state.current_audit.get('ai_trust_score'):.0f}/900)"
        )
        
        question = st.text_area("Ask about governance or remediation:")
        
        if st.button("Get Advisory", use_container_width=True):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/advisory/ask",
                    json={
                        "audit_id": st.session_state.current_audit.get("audit_id"),
                        "question": question,
                    },
                )
                
                result = response.json()
                st.write("**RATIO Advisory Response:**")
                st.write(result.get("advisory_response", "No response"))
            
            except Exception as e:
                st.error(f"Advisory error: {str(e)}")
    
    else:
        st.info("Run an audit first to use advisory")


# ===== PAGE: MONITORING =====
elif page == "Monitoring":
    st.subheader("Monitoring & Score Drift Detection")
    
    col1, col2 = st.columns(2)
    with col1:
        model_uuid = st.text_input("Model UUID")
    with col2:
        previous_audit_id = st.text_input("Previous Audit ID")
    
    if st.button("Re-Audit & Check Drift", use_container_width=True):
        try:
            response = requests.post(
                f"{API_BASE_URL}/monitoring/re-audit",
                json={
                    "model_uuid": model_uuid,
                    "previous_audit_id": previous_audit_id,
                },
            )
            
            result = response.json()
            
            st.metric("Previous Score", result.get("previous_score", 0))
            st.metric("New Score", result.get("new_score", 0))
            st.metric("Change", f"{result.get('score_delta', 0):+.0f}")
            
            if result.get("drift_detected"):
                st.warning("⚠️ Significant score drift detected! Certification may be revoked.")
            else:
                st.success("✓ No significant drift detected")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")


# ===== PAGE: VERIFY CERTIFICATE =====
elif page == "Verify Certificate":
    st.subheader("Verify Certification Badge")
    
    cert_id = st.text_input("Enter Certification ID to verify:")
    
    if st.button("Verify", use_container_width=True):
        try:
            response = requests.get(f"http://localhost:8000/verify/{cert_id}")
            result = response.json()
            
            if result.get("valid"):
                st.success("✓ Certification is valid")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Tier**: {result.get('tier')}")
                    st.write(f"**Score**: {result.get('score'):.0f}/900")
                with col2:
                    st.write(f"**Issued**: {result.get('issued_at')}")
                    st.write(f"**Expires**: {result.get('expires_at')}")
            else:
                st.error(f"Certificate invalid or revoked: {result.get('status')}")
        
        except Exception as e:
            st.error(f"Verification error: {str(e)}")


# ===== FOOTER =====
st.divider()
st.markdown("""
---
**RATIO Governance Certification Platform v1.0**

Built by: **Soumyadarshan Dash**, **Pranita Jagtap**, **Ramdev Chaudhary**

*Production-grade AI governance audit and certification ecosystem*
""")
