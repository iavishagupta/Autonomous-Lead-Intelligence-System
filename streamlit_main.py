import requests
import streamlit as st
import pandas as pd
import altair as alt

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Lead Intelligence Dashboard",
    layout="wide"
)

st.title("Autonomous Lead Intelligence Dashboard")

st.write("Upload host company JSON once, upload leads JSON, then run the pipeline.")

host_file = st.file_uploader(
    "Upload Host Company JSON",
    type=["json"]
)

leads_file = st.file_uploader(
    "Upload Leads JSON",
    type=["json"]
)

if st.button("Start Processing"):
    if not host_file or not leads_file:
        st.error("Upload both JSON files first.")
    else:
        try:
            with st.spinner("Saving host company profile..."):
                host_response = requests.post(
                    f"{API_BASE_URL}/host-company",
                    files={"file": host_file}
                )

                if host_response.status_code != 200:
                    st.error(host_response.json())
                    st.stop()

            with st.spinner("Processing leads... this may take some time."):
                leads_response = requests.post(
                    f"{API_BASE_URL}/run-lead-intelligence",
                    files={"file": leads_file}
                )

                if leads_response.status_code != 200:
                    st.error(leads_response.json())
                    st.stop()

            data = leads_response.json()
            qualified_leads = data.get("qualified_leads", [])

            if not qualified_leads:
                st.warning("No qualified leads found.")
                st.stop()

            st.success("Analysis complete.")

            rows = []

            for lead in qualified_leads:
                rows.append({
                    "Name": lead["personal_info"]["name"],
                    "Job Title": lead["personal_info"]["job_title"],
                    "Company": lead["company_info"]["company_name"],
                    "Role Relevance": lead["personal_info"]["role_relevance"],
                    "Market Presence": lead["company_info"]["market_presence"],
                    "Lead Score": lead["lead_score"]["score"],
                    "Generated Email": lead.get("generated_email", "")
                })

            df = pd.DataFrame(rows)

            col1, col2, col3 = st.columns(3)

            col1.metric("Qualified Leads", len(df))
            col2.metric("Average Score", round(df["Lead Score"].mean(), 2))
            col3.metric("Top Score", df["Lead Score"].max())

            st.subheader("Lead Scores")

            score_chart = alt.Chart(df).mark_bar().encode(
                x="Name",
                y="Lead Score",
                tooltip=["Name", "Company", "Lead Score"]
            )

            st.altair_chart(score_chart, use_container_width=True)

            st.subheader("Role Relevance vs Market Presence")

            scatter_chart = alt.Chart(df).mark_circle(size=120).encode(
                x="Role Relevance",
                y="Market Presence",
                color="Company",
                tooltip=["Name", "Company", "Role Relevance", "Market Presence", "Lead Score"]
            )

            st.altair_chart(scatter_chart, use_container_width=True)

            st.subheader("Qualified Lead Details")
            st.dataframe(df, use_container_width=True)

            st.subheader("Generated Emails")

            for _, row in df.iterrows():
                with st.expander(f"{row['Name']} - {row['Company']}"):
                    st.write(row["Generated Email"])

        except Exception as e:
            st.error(str(e))
