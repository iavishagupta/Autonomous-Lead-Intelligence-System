import requests
import streamlit as st
import pandas as pd
import altair as alt

API_BASE_URL = "https://autonomous-lead-intelligence-system.onrender.com"

st.set_page_config(
    page_title="Autonomous Lead Intelligence",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
    .main {
        background-color: #f7f9fc;
    }

    .hero {
        padding: 2rem;
        border-radius: 24px;
        background: linear-gradient(135deg, #101828 0%, #1d2939 45%, #344054 100%);
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 18px 40px rgba(16, 24, 40, 0.18);
    }

    .hero h1 {
        font-size: 2.4rem;
        margin-bottom: 0.3rem;
    }

    .hero p {
        font-size: 1rem;
        color: #d0d5dd;
        max-width: 780px;
    }

    .section-card {
        background: white;
        padding: 1.4rem;
        border-radius: 20px;
        border: 1px solid #eaecf0;
        box-shadow: 0 8px 24px rgba(16, 24, 40, 0.06);
        margin-bottom: 1rem;
    }

    .metric-card {
        background: white;
        padding: 1.2rem;
        border-radius: 18px;
        border: 1px solid #eaecf0;
        box-shadow: 0 6px 18px rgba(16, 24, 40, 0.06);
    }

    .metric-label {
        font-size: 0.82rem;
        color: #667085;
        margin-bottom: 0.3rem;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #101828;
    }

    .badge-qualified {
        background-color: #dcfae6;
        color: #067647;
        padding: 0.25rem 0.65rem;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.78rem;
    }

    .badge-rejected {
        background-color: #fee4e2;
        color: #b42318;
        padding: 0.25rem 0.65rem;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.78rem;
    }

    .lead-card {
        background: white;
        border-radius: 18px;
        padding: 1.1rem 1.2rem;
        border: 1px solid #eaecf0;
        margin-bottom: 0.9rem;
        box-shadow: 0 5px 16px rgba(16, 24, 40, 0.05);
    }

    .lead-title {
        font-size: 1.08rem;
        font-weight: 800;
        color: #101828;
    }

    .lead-subtitle {
        color: #667085;
        font-size: 0.9rem;
        margin-bottom: 0.6rem;
    }

    .reason-box {
        background: #f9fafb;
        border-left: 4px solid #98a2b3;
        padding: 0.85rem;
        border-radius: 12px;
        color: #344054;
        font-size: 0.9rem;
        line-height: 1.5;
    }

    .email-box {
        background: #eef4ff;
        border-left: 4px solid #3538cd;
        padding: 0.85rem;
        border-radius: 12px;
        color: #1d2939;
        font-size: 0.9rem;
        line-height: 1.5;
    }

    .stButton > button {
        background: linear-gradient(135deg, #3538cd, #7a5af8);
        color: white;
        border: none;
        border-radius: 14px;
        padding: 0.75rem 1.4rem;
        font-weight: 800;
        box-shadow: 0 8px 20px rgba(53, 56, 205, 0.25);
    }

    .stButton > button:hover {
        color: white;
        border: none;
        transform: translateY(-1px);
    }

    div[data-testid="stFileUploader"] {
        background: white;
        border-radius: 18px;
        padding: 1rem;
        border: 1px solid #eaecf0;
    }
</style>
""", unsafe_allow_html=True)


def badge(status):
    if status == "Qualified":
        return '<span class="badge-qualified">Qualified</span>'
    return '<span class="badge-rejected">Rejected</span>'


st.markdown("""
<div class="hero">
    <h1>Autonomous Lead Intelligence Dashboard</h1>
    <p>
        A business-facing R&D asset for evaluating lead quality, strategic fit,
        qualification confidence, and AI-generated outreach readiness.
    </p>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Input Control Center")

    col_upload_1, col_upload_2 = st.columns(2)

    with col_upload_1:
        host_file = st.file_uploader(
            "Upload Host Company JSON",
            type=["json"],
            help="Contains your company profile, mission, values, strategic goals, and market context."
        )

    with col_upload_2:
        leads_file = st.file_uploader(
            "Upload Leads JSON",
            type=["json"],
            help="Contains lead records to analyze and qualify."
        )

    run_clicked = st.button("Run Intelligence Pipeline")
    st.markdown('</div>', unsafe_allow_html=True)


if run_clicked:
    if not host_file or not leads_file:
        st.error("Upload both JSON files first. The machine cannot analyze imaginary files. Yet.")
        st.stop()

    try:
        progress = st.progress(0)
        status_text = st.empty()
        
        status_text.info("Initializing intelligence pipeline...")
        progress.progress(5)
        time.sleep(0.4)
        
        status_text.info("Saving host company profile...")
        progress.progress(12)
        
        host_response = requests.post(
            f"{API_BASE_URL}/host-company",
            files={"file": host_file}
        )
        
        if host_response.status_code != 200:
            st.error(host_response.json())
            st.stop()
        
        time.sleep(0.5)
        
        status_text.info("Parsing uploaded lead dataset...")
        progress.progress(22)
        time.sleep(0.5)
        
        status_text.info("Researching lead organizations...")
        progress.progress(35)
        time.sleep(0.7)
        
        status_text.info("Extracting strategic and cultural signals...")
        progress.progress(48)
        time.sleep(0.7)
        
        status_text.info("Evaluating business alignment...")
        progress.progress(60)
        time.sleep(0.6)
        
        status_text.info("Calculating qualification confidence...")
        progress.progress(72)
        time.sleep(0.5)
        
        status_text.info("Generating outreach recommendations...")
        progress.progress(84)
        
        leads_response = requests.post(
            f"{API_BASE_URL}/run-lead-intelligence",
            files={"file": leads_file}
        )
        
        if leads_response.status_code != 200:
            st.error(leads_response.json())
            st.stop()
        
        status_text.info("Building executive analytics dashboard...")
        progress.progress(94)
        time.sleep(0.4)
        
        data = leads_response.json()
        
        progress.progress(100)
        status_text.success("Intelligence pipeline completed successfully.")

        data = leads_response.json()
        analyzed_leads = data.get("analyzed_leads", [])
        summary = data.get("summary", {})

        if not analyzed_leads:
            st.warning("No analyzed leads returned.")
            st.stop()

        rows = []

        for lead in analyzed_leads:
            qualification = lead.get("qualification", {})

            rows.append({
                "Name": lead.get("personal_info", {}).get("name", "Unknown"),
                "Job Title": lead.get("personal_info", {}).get("job_title", "Unknown"),
                "Company": lead.get("company_info", {}).get("company_name", "Unknown"),
                "Role Relevance": lead.get("personal_info", {}).get("role_relevance", 0),
                "Market Presence": lead.get("company_info", {}).get("market_presence", 0),
                "Lead Score": lead.get("lead_score", {}).get("score", 0),
                "Qualification": qualification.get("status", "Unknown"),
                "Reason": qualification.get("reason", "No reason provided."),
                "Generated Email": lead.get("generated_email") or "Not generated because lead was rejected."
            })

        df = pd.DataFrame(rows)

        qualified_df = df[df["Qualification"] == "Qualified"]
        rejected_df = df[df["Qualification"] == "Rejected"]

        progress.progress(100)
        status_text.success("Analysis complete.")

        st.markdown("## Executive Summary")

        m1, m2, m3, m4 = st.columns(4)

        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Leads</div>
                <div class="metric-value">{summary.get("total_leads", len(df))}</div>
            </div>
            """, unsafe_allow_html=True)

        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Qualified</div>
                <div class="metric-value" style="color:#067647;">{summary.get("qualified_leads", len(qualified_df))}</div>
            </div>
            """, unsafe_allow_html=True)

        with m3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Rejected</div>
                <div class="metric-value" style="color:#b42318;">{summary.get("rejected_leads", len(rejected_df))}</div>
            </div>
            """, unsafe_allow_html=True)

        with m4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Average Score</div>
                <div class="metric-value">{round(df["Lead Score"].mean(), 2)}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("## Intelligence Visuals")

        tab1, tab2, tab3 = st.tabs([
            "Score Landscape",
            "Fit Matrix",
            "Qualification Mix"
        ])

        with tab1:
            score_chart = alt.Chart(df).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
                x=alt.X("Name", sort="-y", title="Lead"),
                y=alt.Y("Lead Score", scale=alt.Scale(domain=[0, 100])),
                color=alt.Color(
                    "Qualification",
                    scale=alt.Scale(
                        domain=["Qualified", "Rejected"],
                        range=["#12b76a", "#f04438"]
                    )
                ),
                tooltip=[
                    "Name",
                    "Company",
                    "Lead Score",
                    "Qualification",
                    "Reason"
                ]
            ).properties(height=360)

            st.altair_chart(score_chart, use_container_width=True)

        with tab2:
            scatter_chart = alt.Chart(df).mark_circle(size=220, opacity=0.85).encode(
                x=alt.X("Role Relevance", scale=alt.Scale(domain=[0, 10])),
                y=alt.Y("Market Presence", scale=alt.Scale(domain=[0, 10])),
                color=alt.Color(
                    "Qualification",
                    scale=alt.Scale(
                        domain=["Qualified", "Rejected"],
                        range=["#12b76a", "#f04438"]
                    )
                ),
                tooltip=[
                    "Name",
                    "Company",
                    "Role Relevance",
                    "Market Presence",
                    "Lead Score",
                    "Qualification"
                ]
            ).properties(height=360)

            st.altair_chart(scatter_chart, use_container_width=True)

        with tab3:
            split_df = df["Qualification"].value_counts().reset_index()
            split_df.columns = ["Qualification", "Count"]

            split_chart = alt.Chart(split_df).mark_arc(innerRadius=70).encode(
                theta="Count",
                color=alt.Color(
                    "Qualification",
                    scale=alt.Scale(
                        domain=["Qualified", "Rejected"],
                        range=["#12b76a", "#f04438"]
                    )
                ),
                tooltip=["Qualification", "Count"]
            ).properties(height=360)

            st.altair_chart(split_chart, use_container_width=True)

        st.markdown("## Lead Intelligence Table")

        st.dataframe(
            df[
                [
                    "Name",
                    "Company",
                    "Job Title",
                    "Lead Score",
                    "Qualification",
                    "Role Relevance",
                    "Market Presence"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.markdown("## Lead Review Cards")

        for _, row in df.sort_values("Lead Score", ascending=False).iterrows():
            st.markdown(f"""
            <div class="lead-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div class="lead-title">{row["Name"]} · {row["Company"]}</div>
                        <div class="lead-subtitle">{row["Job Title"]} · Score: {row["Lead Score"]}/100</div>
                    </div>
                    <div>{badge(row["Qualification"])}</div>
                </div>
                <div class="reason-box">
                    <strong>Qualification Reason:</strong><br>
                    {row["Reason"]}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if row["Qualification"] == "Qualified":
                st.markdown(f"""
                <div class="email-box">
                    <strong>Generated Outreach Email:</strong><br>
                    {row["Generated Email"]}
                </div>
                """, unsafe_allow_html=True)

        st.markdown("## Exportable Results")

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Analysis CSV",
            data=csv,
            file_name="lead_intelligence_results.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(str(e))
