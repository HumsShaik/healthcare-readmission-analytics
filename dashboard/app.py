import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Healthcare Readmission Analytics",
    page_icon="🏥",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================
dashboard_df = pd.read_csv("data/processed/dashboard_healthcare_data.csv")
executive_kpis = pd.read_csv("outputs/executive_kpis.csv")
risk_summary = pd.read_csv("outputs/risk_segment_summary.csv")
feature_importance = pd.read_csv("outputs/final_feature_importance.csv")
model_comparison = pd.read_csv("outputs/tuned_model_comparison.csv")
diag_summary = pd.read_csv("outputs/diagnosis_readmission_summary.csv")

# =========================
# TITLE
# =========================
st.title("🏥 Healthcare Readmission Analytics Dashboard")

st.markdown("""
This dashboard analyzes hospital readmission patterns using the UCI Diabetes 130-US Hospitals dataset.

It combines healthcare analytics, machine learning insights, and risk segmentation to support readmission reduction strategies.
""")
with st.expander("📖 Project Overview"):

    st.markdown("""
    ### Healthcare Readmission Analytics

    This project analyzes hospital readmission patterns using over 100,000 patient encounters.

    Objectives:

    - Identify readmission risk factors
    - Analyze healthcare utilization
    - Build machine learning models
    - Create executive dashboards

    Best Model:
    - Tuned Random Forest
    - F1 Score: 57.24%
    - Recall: 54.73%
    """)
# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.title("🏥 Dashboard Controls")

st.sidebar.markdown("""
Healthcare Readmission Analytics

Filter patient populations and explore readmission patterns.
""")

risk_filter = st.sidebar.multiselect(
    "Select Risk Segment",
    options=dashboard_df["risk_segment"].unique(),
    default=dashboard_df["risk_segment"].unique()
)

filtered_df = dashboard_df[
    dashboard_df["risk_segment"].isin(risk_filter)
]

# =========================
# KPI CARDS
# =========================
st.subheader("📊 Executive KPI Overview")
total_encounters = len(filtered_df)
unique_patients = filtered_df["patient_nbr"].nunique()
readmission_rate = filtered_df["readmitted_flag"].mean() * 100
avg_los = filtered_df["time_in_hospital"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Encounters", f"{total_encounters:,}")
col2.metric("Unique Patients", f"{unique_patients:,}")
col3.metric("Readmission Rate", f"{readmission_rate:.2f}%")
col4.metric("Avg Length of Stay", f"{avg_los:.2f} days")
st.info("""
Key Finding:

Healthcare utilization history and prior inpatient visits were the strongest predictors of readmission risk.

Patients with multiple prior inpatient visits exhibited substantially higher readmission rates.
""")
# =========================
# TABS
# =========================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Executive Overview",
    "Patient Demographics",
    "Risk Analysis",
    "Machine Learning",
    "Business Recommendations"
])

# =========================
# TAB 1
# =========================
with tab1:
    st.subheader("Readmission Distribution")

    readmission_counts = filtered_df["readmitted"].value_counts().reset_index()
    readmission_counts.columns = ["Readmission Status", "Count"]

    fig = px.pie(
        readmission_counts,
        names="Readmission Status",
        values="Count",
        title="Readmission Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Diagnosis Readmission Rate")

    fig = px.bar(
        diag_summary,
        x="diagnosis_category",
        y="readmission_rate",
        title="Readmission Rate by Diagnosis Category",
        labels={
            "diagnosis_category": "Diagnosis Category",
            "readmission_rate": "Readmission Rate (%)"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# TAB 2
# =========================
with tab2:
    st.subheader("Age Distribution")

    age_counts = filtered_df["age"].value_counts().reset_index()
    age_counts.columns = ["Age Group", "Count"]

    fig = px.bar(
        age_counts,
        x="Age Group",
        y="Count",
        title="Patient Encounters by Age Group"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Gender Distribution")

    gender_counts = filtered_df["gender"].value_counts().reset_index()
    gender_counts.columns = ["Gender", "Count"]

    fig = px.bar(
        gender_counts,
        x="Gender",
        y="Count",
        title="Patient Encounters by Gender"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# TAB 3
# =========================
with tab3:
    st.subheader("Risk Segment Summary")

    st.dataframe(risk_summary)

    fig = px.bar(
        risk_summary,
        x="risk_segment",
        y="readmission_rate",
        title="Readmission Rate by Risk Segment",
        labels={
            "risk_segment": "Risk Segment",
            "readmission_rate": "Readmission Rate (%)"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# TAB 4
# =========================
with tab4:
    st.subheader("Model Performance")
    
    st.success("""
Best Model: Tuned Random Forest

Accuracy: 62.32%
Recall: 54.73%
F1 Score: 57.24%

The tuned model improved identification of high-risk patients compared to the baseline model.
""")
    st.dataframe(model_comparison)

    fig = px.bar(
        model_comparison,
        x="model",
        y=["accuracy", "precision", "recall", "f1_score"],
        barmode="group",
        title="Baseline vs Tuned Model Performance"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top Readmission Risk Factors")

    fig = px.bar(
        feature_importance.head(10),
        x="importance",
        y="feature",
        orientation="h",
        title="Top Feature Importance"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# TAB 5
# =========================
with tab5:
    st.subheader("Business Recommendations")

    st.markdown("""
    ### 1. Prioritize Patients With Prior Inpatient Visits
    Patients with previous inpatient visits showed higher readmission risk.

    ### 2. Monitor High Utilization Patients
    Patients with frequent outpatient, emergency, or inpatient visits should be flagged for follow-up.

    ### 3. Review Medication Complexity
    Patients with high medication counts may benefit from medication reconciliation.

    ### 4. Focus on Diabetes and Respiratory Conditions
    These diagnosis groups showed elevated readmission rates.

    ### 5. Use Risk Segmentation
    Risk segments can help hospital teams prioritize care management resources.
    """)

st.markdown("---")

st.caption(
    """
    Healthcare Readmission Analytics
    
    Built using Python, Scikit-Learn, Streamlit, Plotly, and the UCI Diabetes 130-US Hospitals Dataset.
    """
)