import requests
import streamlit as st
import pandas as pd
import altair as alt

API_BASE_URL = "https://autonomous-lead-intelligence-system.onrender.com"

st.set_page_config(
    page_title="Lead Intelligence Dashboard",
    layout="wide"
)

st.title("Autonomous Lead Intelligence Dashboard")

st.write(
    "Upload host company JSON once, upload leads JSON, then run the pipeline."
)

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

            analyzed_leads = data.get("analyzed_leads", [])
            summary = data.get("summary", {})

            if not analyzed_leads:
                st.warning("No analyzed leads returned.")
                st.stop()

            st.success("Analysis complete.")

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

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Total Leads",
                summary.get("total_leads", len(df))
            )

            col2.metric(
                "Qualified",
                summary.get("qualified_leads", len(qualified_df))
            )

            col3.metric(
                "Rejected",
                summary.get("rejected_leads", len(rejected_df))
            )

            col4.metric(
                "Average Score",
                round(df["Lead Score"].mean(), 2)
            )

            st.subheader("Lead Score Comparison")

            score_chart = alt.Chart(df).mark_bar().encode(
                x=alt.X("Name", sort="-y"),
                y=alt.Y("Lead Score", scale=alt.Scale(domain=[0, 100])),
                color="Qualification",
                tooltip=[
                    "Name",
                    "Company",
                    "Lead Score",
                    "Qualification",
                    "Reason"
                ]
            )

            st.altair_chart(score_chart, use_container_width=True)

            st.subheader("Role Relevance vs Market Presence")

            scatter_chart = alt.Chart(df).mark_circle(size=140).encode(
                x=alt.X("Role Relevance", scale=alt.Scale(domain=[0, 10])),
                y=alt.Y("Market Presence", scale=alt.Scale(domain=[0, 10])),
                color="Qualification",
                tooltip=[
                    "Name",
                    "Company",
                    "Role Relevance",
                    "Market Presence",
                    "Lead Score",
                    "Qualification"
                ]
            )

            st.altair_chart(scatter_chart, use_container_width=True)

            st.subheader("Qualification Split")

            split_df = df["Qualification"].value_counts().reset_index()
            split_df.columns = ["Qualification", "Count"]

            split_chart = alt.Chart(split_df).mark_arc().encode(
                theta="Count",
                color="Qualification",
                tooltip=["Qualification", "Count"]
            )

            st.altair_chart(split_chart, use_container_width=True)

            st.subheader("All Lead Analysis")

            st.dataframe(
                df[
                    [
                        "Name",
                        "Company",
                        "Job Title",
                        "Lead Score",
                        "Qualification",
                        "Reason"
                    ]
                ],
                use_container_width=True
            )

            st.subheader("Qualified Lead Emails")

            if qualified_df.empty:
                st.info("No qualified leads, so no emails were generated.")
            else:
                for _, row in qualified_df.iterrows():
                    with st.expander(f"{row['Name']} - {row['Company']}"):
                        st.write(row["Generated Email"])

            st.subheader("Rejected Lead Reasons")

            if rejected_df.empty:
                st.info("No rejected leads.")
            else:
                for _, row in rejected_df.iterrows():
                    with st.expander(f"{row['Name']} - {row['Company']}"):
                        st.write(row["Reason"])

        except Exception as e:
            st.error(str(e))
