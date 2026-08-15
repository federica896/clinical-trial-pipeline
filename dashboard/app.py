"""
MERIDIAN-3 Clinical Trial Safety Dashboard

Interactive Streamlit dashboard querying dbt mart tables in DuckDB.
Four tabs: Enrollment Overview, Adverse Events, Laboratory Monitoring, Site Performance.
"""
import duckdb
import streamlit as st
import pandas as pd 
import plotly.express as px
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, "data", "clinical_trial.duckdb")

st.set_page_config(
    page_title="MERIDIAN-3 Dashboard", 
    layout="wide", 
    initial_sidebar_state="auto"
)

# Load data: cached to avoid re-querying DuckDB on every interaction
@st.cache_data
def load_data():
    con = duckdb.connect(DB_PATH)
    data = {
        "adsl": con.execute("SELECT * FROM main_marts.adsl").fetchdf(),
        "adae": con.execute("SELECT * FROM main_marts.adae").fetchdf(),
        "ae_analysis": con.execute("SELECT * FROM main_marts.mart_ae_analysis").fetchdf(),
        "site": con.execute("SELECT * FROM main_marts.mart_site_performance").fetchdf(), 
        "labs": con.execute("SELECT * FROM main_staging.stg_lb").fetchdf()
    }
    con.close()
    return data
data = load_data()

st.title("MERIDIAN-3 Clinical Trial Safety Dashboard")
st.caption("Phase III Compound X and Compound Y vs Placebo in Advanced Solid Tumors")

# Sidebar: global filters
with st.sidebar:
    st.header("MERIDIAN-3")
    selected_site = st.selectbox("Filter by Site", ["All"] + data['site']['SITEID'].tolist())
    st.subheader("Date Range")
    min_date = pd.to_datetime(data["adsl"]["TRTSDT"]).min().date()
    max_date = pd.to_datetime(data["adsl"]["TRTEDT"]).max().date()
    date_range = st.date_input("Treatment Period", value=(min_date, max_date), min_value=min_date, max_value=max_date)

# Apply filter to datasets
if selected_site != "All":
    adsl = data["adsl"][data["adsl"]["SITEID"] == selected_site]
    adae = data["adae"][data["adae"]["USUBJID"].isin(adsl["USUBJID"])]
    labs = data["labs"][data["labs"]["USUBJID"].isin(adsl["USUBJID"])]
    site = data["site"][data["site"]["SITEID"] == selected_site]
else:
    adsl = data["adsl"]
    adae = data["adae"]
    labs = data["labs"]
    site = data["site"]
# Apply date filter
if len(date_range) == 2:
    start, end = date_range
    adsl = adsl[(pd.to_datetime(adsl["TRTSDT"]).dt.date >= start) & 
                (pd.to_datetime(adsl["TRTSDT"]).dt.date <= end)]
    adae = adae[adae["USUBJID"].isin(adsl["USUBJID"])]
    labs = labs[labs["USUBJID"].isin(adsl["USUBJID"])]

tab1, tab2, tab3, tab4 = st.tabs(["Enrollment Overview", "Adverse Event", "Laboratory Monitoring", "Site Performance"])

# Tab 1: Enrollment Overview 
with tab1:
    st.header("Enrollment Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Screened Patients", site['total_screened'].sum())
    with col2:
        st.metric("Total Enrolled Patients", site['total_enrolled'].sum())
    with col3:
        total_screened = site['total_screened'].sum()
        total_enrolled = site['total_enrolled'].sum()
        sfr = round((total_screened - total_enrolled) / total_screened * 100, 1)
        st.metric("Screen Failure Rate", f"{sfr}%")

    st.divider()

    # Monthly enrollment trend 
    adsl_plot = adsl.copy()
    adsl_plot["enroll_month"] = pd.to_datetime(adsl_plot["TRTSDT"]).dt.to_period("M").astype(str)
    monthly = adsl_plot.groupby("enroll_month").size().reset_index(name="count")
    fig = px.line(monthly, x="enroll_month", y="count", title="Enrollment Over Time", 
                labels={"enroll_month": "Month", "count": "Subjects Enrolled"})
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Patient Drill-Down")
    selected_patient = st.selectbox("Select Patient", adsl["USUBJID"].tolist())

    patient = adsl[adsl["USUBJID"] == selected_patient].iloc[0]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Age", int(patient["AGE"]))
    with col2:
        st.metric("Sex", patient["SEX"])
    with col3:
        st.metric("Arm", patient["ARMCD"])
    with col4:
        st.metric("Disposition", patient["DSDECOD"])

    # Patient's AEs
    patient_aes = adae[adae["USUBJID"] == selected_patient]
    if len(patient_aes) > 0:
        st.write(f"**Adverse Events ({len(patient_aes)})**")
        st.dataframe(patient_aes[["AETERM", "AESEV", "AESER", "AEREL", "AESTDTC", "AEENDTC"]], use_container_width=True)
    else:
        st.info("No adverse events recorded")

    # Patient's lab results
    patient_labs = labs[labs["USUBJID"] == selected_patient]
    if len(patient_labs) > 0:
        st.write(f"**Lab Results ({len(patient_labs)})**")
        fig = px.line(patient_labs, x="LBDTC", y="LBSTRESN", color="LBTESTCD", title="Lab Values Over Time",
                    labels={"LBDTC": "Date", "LBSTRESN": "Value", "LBTESTCD": "Test"})
        st.plotly_chart(fig, use_container_width=True)

    st.download_button("Download Enrollment Data", adsl.to_csv(index=False), "enrollment_data.csv", "text/csv")

# Tab 2: AEs
with tab2:
    st.header("Adverse Events")

    # Ae incidence rate by treatment arm
    ae_analysis = data["ae_analysis"]
    fig = px.bar(ae_analysis, x="ARMCD", y="ae_rate_pct", color="ARM", title="AE Rate by Treatment Arm (%)", 
                labels={"ARMCD": "Treatment Arm", "ae_rate_pct": "AE Rate (%)"})
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Severity distribution 
    severity_cols = ae_analysis[["ARMCD", "mild_count", "moderate_count", "severe_count"]]
    severity_melted = severity_cols.melt(id_vars="ARMCD", var_name="severity", value_name="count")
    fig = px.bar(severity_melted, x="ARMCD", y="count", color="severity", barmode="group", title="Severity Distribution by Arm", 
                labels={"ARMCD": "Treatment Arm", "count": "Number of AEs", "severity": "Severity"})
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Most frequently reported AE terms 
    top_aes = adae.groupby("AEDECOD").size().reset_index(name="count").sort_values("count", ascending=False).head(10)
    fig = px.bar(top_aes, x="count", y="AEDECOD", orientation="h", title="Top 10 Adverse Events by Frequency",
                labels={"count": "Frequency", "AEDECOD": "Adverse Event Term"})
    st.plotly_chart(fig, use_container_width=True)

    st.download_button("Download AE Data", adae.to_csv(index=False), "ae_data.csv", "text/csv")

# Tab3: Lab Monitoring 
with tab3:
    st.header("Laboratory Monitoring")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Lab Tests", len(labs))
    with col2:
        abnormal = labs[labs['LBNRIND'].isin(["LOW", "HIGH"])]
        st.metric("Abnormal Rate", f"{len(abnormal)/len(labs) * 100:.1f}%")

    st.divider()

    # Lab tests with the most OoR resuls
    abnormal_by_test = abnormal.groupby("LBTESTCD").size().reset_index(name="abnormal_count")
    fig = px.bar(abnormal_by_test, x="LBTESTCD", y="abnormal_count", title="Abnormal Rate by Test Type", 
                labels={"LBTESTCD": "Lab Test", "abnormal_count": "Abnormal Results"})
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Individual patient lab trajectories for filtered test
    selected_test = st.selectbox("Select Lab Test", labs["LBTESTCD"].unique())
    test_data = labs[labs["LBTESTCD"] == selected_test].copy()
    test_data["visit_order"] = test_data["VISITNUM"]
    normal_low = test_data["LBORNRLO"].iloc[0]
    normal_high = test_data["LBORNRHI"].iloc[0]

    # Aggregate: median, 25th, 75th percentile per visit
    summary = test_data.groupby(["VISITNUM", "VISIT"]).agg(
        median=("LBSTRESN", "median"),
        q25=("LBSTRESN", lambda x: x.quantile(0.25)),
        q75=("LBSTRESN", lambda x: x.quantile(0.75))
    ).reset_index().sort_values("VISITNUM")

    fig = px.line(summary, x="VISIT", y="median", title=f"{selected_test}: Median with IQR", 
                  labels={"VISIT": "Visit", "median": "Median Value"})
    fig.add_scatter(x=summary["VISIT"], y=summary["q25"], mode="lines", line=dict(dash="dash"), name="25th pct")
    fig.add_scatter(x=summary["VISIT"], y=summary["q75"], mode="lines", line=dict(dash="dash"), name="75th pct")
    fig.add_hline(y=normal_low, line_dash="dot", line_color="red", annotation_text="Lower Limit")
    fig.add_hline(y=normal_high, line_dash="dot", line_color="red", annotation_text="Upper Limit")
    st.plotly_chart(fig, use_container_width=True)

    st.download_button("Download Lab Data", labs.to_csv(index=False), "lab_data.csv", "text/csv")

# Tab 4: Site Performance 
with tab4:
    st.header("Site Performance")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Number of Sites", len(site))
    with col2:
        st.metric("Avg Enrollment per Site", round(site["total_enrolled"].mean(), 1))
    
    st.divider()

    # Enrollment by site bar chart
    fig = px.bar(site, x="SITEID", y="total_enrolled", color="COUNTRY", title="Enrollment by Site", 
                 labels={"SITEID": "Site", "total_enrolled": "Enrolled Subjects", "COUNTRY": "Country"})
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Screen failure rate by site
    fig = px.bar(site, x="SITEID", y="screen_failure_pct", color="COUNTRY", title="Screen Failure Rate by Site (%)", 
                 labels={"SITEID": "Site", "screen_failure_pct": "Screen Failure Rate (%)", "COUNTRY": "Country"})
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Full site metrics table
    st.subheader("Detailed Site Metrics")
    st.dataframe(site, use_container_width=True)

    st.download_button("Download Site Metrics", site.to_csv(index=False), "site_metrics.csv", "text/csv")