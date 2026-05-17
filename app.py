import streamlit as st
import plotly.express as px
from utils import load_data, parse_clinical_summary

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Patient Intelligence Dashboard",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

/* Main app background */
[data-testid="stAppViewContainer"] {
    background-color: #edf7f2;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #dff1e7;
}

/* KPI cards */
div[data-testid="metric-container"] {
    background-color: white;
    border: 1px solid #d1d5db;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* Main text */
h1, h2, h3, p, label {
    color: #0f172a;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
patients, visits, actions, calls = load_data()
patients = parse_clinical_summary(patients)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🏥 Docstribe Dashboard")
st.sidebar.markdown("Healthcare Intelligence Platform")

# ---------------- TITLE ----------------
st.title("Patient Intelligence Dashboard")
st.subheader("Clinical + Operational Intelligence for CXO")
st.markdown("---")

# ---------------- KPI CALCULATIONS ----------------
total_patients = len(patients)

high_risk = patients["risk"].isin(
    ["high", "critical", "rising"]
).sum()

total_revenue = 0
if "Revenue Potential" in actions.columns:
    total_revenue = actions["Revenue Potential"].fillna(0).sum()

pending_tasks = 0
if "Status" in actions.columns:
    pending_tasks = actions[
        actions["Status"].astype(str).str.lower() == "pending"
    ].shape[0]

# ---------------- KPI DISPLAY ----------------
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("Total Patients", total_patients)

with k2:
    st.metric("High Risk Patients", high_risk)

with k3:
    st.metric("Revenue Potential", f"₹{total_revenue:,.0f}")

with k4:
    st.metric("Pending Tasks", pending_tasks)

st.markdown("---")

# =========================================================
# CLINICAL ANALYTICS
# =========================================================
st.header("Clinical Analytics")

col1, col2 = st.columns(2)

with col1:
    risk_counts = patients["risk"].value_counts().reset_index()
    risk_counts.columns = ["Risk", "Count"]

    fig1 = px.pie(
        risk_counts,
        names="Risk",
        values="Count",
        title="Risk Distribution"
    )
    st.plotly_chart(fig1, width="stretch")

with col2:
    if "Visit Date" in visits.columns:
        visit_trend = visits.groupby(
            "Visit Date"
        ).size().reset_index(name="Count")

        fig2 = px.line(
            visit_trend,
            x="Visit Date",
            y="Count",
            title="Patient Visits Trend Over Time",
            markers=True
        )
        st.plotly_chart(fig2, width="stretch")

st.markdown("---")

# =========================================================
# OPERATIONAL ANALYTICS
# =========================================================
st.header("Operational Analytics")

col3, col4 = st.columns(2)

with col3:
    if "Department" in visits.columns:
        dept_counts = visits["Department"].value_counts().reset_index()
        dept_counts.columns = ["Department", "Count"]

        fig3 = px.bar(
            dept_counts,
            x="Count",
            y="Department",
            orientation="h",
            color="Department",
            title="Visits by Department"
        )
        st.plotly_chart(fig3, width="stretch")

with col4:
    if "Urgency" in actions.columns:
        urgency_counts = actions["Urgency"].value_counts().reset_index()
        urgency_counts.columns = ["Urgency", "Count"]

        fig4 = px.bar(
            urgency_counts,
            x="Urgency",
            y="Count",
            color="Urgency",
            title="Task Urgency Distribution"
        )
        st.plotly_chart(fig4, width="stretch")

st.markdown("---")

# =========================================================
# FINANCIAL ANALYTICS
# =========================================================
st.header("Financial Overview")

if "Status" in actions.columns:
    status_counts = actions["Status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]

    fig5 = px.pie(
        status_counts,
        names="Status",
        values="Count",
        title="Task Status Distribution"
    )
    st.plotly_chart(fig5, width="stretch")

st.markdown("---")

# =========================================================
# CALL ANALYTICS
# =========================================================
st.header("Call Analytics")

total_calls = len(calls)

completed_calls = 0
missed_calls = 0
pending_followups = 0

if "Call Status" in calls.columns:
    completed_calls = calls[
        calls["Call Status"].astype(str).str.lower() == "completed"
    ].shape[0]

    missed_calls = calls[
        calls["Call Status"].astype(str).str.lower() == "missed"
    ].shape[0]

if "Follow-up Date" in calls.columns:
    pending_followups = calls["Follow-up Date"].notna().sum()

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Total Calls", total_calls)

with c2:
    st.metric("Completed Calls", completed_calls)

with c3:
    st.metric("Pending Follow-ups", pending_followups)

col5, col6 = st.columns(2)

with col5:
    if "Call Status" in calls.columns:
        call_status_counts = calls["Call Status"].value_counts().reset_index()
        call_status_counts.columns = ["Status", "Count"]

        fig6 = px.pie(
            call_status_counts,
            names="Status",
            values="Count",
            title="Call Status Distribution"
        )
        st.plotly_chart(fig6, width="stretch")

with col6:
    if "Agent Name" in calls.columns:
        agent_counts = calls["Agent Name"].value_counts().reset_index()
        agent_counts.columns = ["Agent", "Count"]

        fig7 = px.bar(
            agent_counts,
            x="Agent",
            y="Count",
            color="Agent",
            title="Calls Handled by Agent"
        )
        st.plotly_chart(fig7, width="stretch")

st.markdown("---")

# =========================================================
# PATIENT TABLE
# =========================================================
st.header("Patient Intelligence")

display_cols = [
    col for col in [
        "Patient ID",
        "Patient Name",
        "risk",
        "revenue",
        "next_follow_up"
    ]
    if col in patients.columns
]

st.dataframe(
    patients[display_cols],
    width="stretch"
)

st.markdown("---")

# =========================================================
# ALERTS
# =========================================================
st.subheader("Alerts")

critical_no_followup = patients[
    (patients["risk"] == "critical") &
    (patients["next_follow_up"].isna())
]

st.warning(
    f"{len(critical_no_followup)} critical patients have no follow-up scheduled"
)

st.markdown("---")

# =========================================================
# CHATBOT / NL QUERY
# =========================================================
st.header("Natural Language Query Interface")

query = st.text_input(
    "Ask a question about patients or operations"
)

st.caption(
    "Examples: HbA1C issues, high-risk no follow-up, diabetic cardiology patients, missed calls"
)

if query:
    query = query.lower()

    # -------------------------------------------------
    # 1. HbA1C issues
    # -------------------------------------------------
    if "hba1c" in query:
        result = patients[
            patients["Clinical Summary"]
            .astype(str)
            .str.contains("hba1c", case=False, na=False)
        ]

        st.write(f"Found {len(result)} patients with HbA1C concerns")
        st.dataframe(result, width="stretch")

        high_ip = result[
            result["risk"].isin(["high", "critical", "rising"])
        ].shape[0]

        st.info(
            f"{len(result)} patients flagged with HbA1C concerns, "
            f"{high_ip} have elevated risk or IP potential."
        )

    # -------------------------------------------------
    # 2. High-risk patients with no follow-up
    # -------------------------------------------------
    elif (
        "high-risk" in query
        or "high risk" in query
    ) and "follow-up" in query:

        result = patients[
            (patients["risk"].isin(["high", "critical", "rising"])) &
            (patients["next_follow_up"].isna())
        ]

        st.write(
            f"Found {len(result)} high-risk patients with no follow-up scheduled"
        )
        st.dataframe(result, width="stretch")

    # -------------------------------------------------
    # 3. Diabetic patients referred to cardiology
    # -------------------------------------------------
    elif "diabetic" in query and "cardiology" in query:

        diabetic = patients[
            patients["Clinical Summary"]
            .astype(str)
            .str.contains("diabetes", case=False, na=False)
        ]

        cardiology = visits[
            visits["Department"]
            .astype(str)
            .str.contains("cardiology", case=False, na=False)
        ]

        result = diabetic.merge(
            cardiology,
            on="Patient ID",
            how="inner"
        )

        st.write(
            f"Found {len(result)} diabetic patients referred to cardiology"
        )
        st.dataframe(result, width="stretch")

    # -------------------------------------------------
    # 4. Missed calls / no response
    # -------------------------------------------------
    elif (
        "missed call" in query
        or "no call response" in query
        or "unanswered" in query
    ):

        result = calls[
            calls["Call Status"]
            .astype(str)
            .str.lower()
            .isin(["unanswered", "no response", "missed"])
        ]

        st.write(
            f"Found {len(result)} patients with missed or unanswered calls"
        )
        st.dataframe(result, width="stretch")

    # -------------------------------------------------
    # Existing queries
    # -------------------------------------------------
    elif "medium risk" in query:
        result = patients[
            patients["risk"].isin(["medium", "rising"])
        ]
        st.write(f"Found {len(result)} medium-risk patients")
        st.dataframe(result, width="stretch")

    elif "high risk" in query or "risk" in query:
        result = patients[
            patients["risk"].isin(["high", "critical", "rising"])
        ]
        st.write(f"Found {len(result)} high-risk patients")
        st.dataframe(result, width="stretch")

    elif "pending task" in query:
        result = actions[
            actions["Status"].astype(str).str.lower() == "pending"
        ]
        st.write(f"Found {len(result)} pending tasks")
        st.dataframe(result, width="stretch")

    elif "revenue" in query:
        st.write(f"Total revenue potential is ₹{total_revenue:,.0f}")

    else:
        st.write("Sorry, query not understood yet.")