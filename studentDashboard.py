import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Student Performance Analytics Dashboard",
    page_icon="🎓",
    layout="wide"
)

# ---------------- CUSTOM STYLING (HTML/CSS) ----------------
st.markdown("""
    <style>
    .main-title {
        font-size: 40px;
        font-weight: 800;
        color: #1f3b73;
        text-align: center;
        padding-bottom: 0px;
    }
    .sub-title {
        font-size: 18px;
        color: #4a4a4a;
        text-align: center;
        padding-bottom: 20px;
    }
    .metric-card {
        background-color: #f0f4ff;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.08);
    }
    .stButton>button {
        background-color: #1f3b73;
        color: white;
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 600;
    }
    section[data-testid="stSidebar"] {
        background-color: #eef2fa;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown('<div class="main-title">🎓 Student Performance Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Explore, filter, and visualize student marks and attendance data '
    'to uncover trends across departments and semesters.</div>',
    unsafe_allow_html=True
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("student_performance.csv")
    return df

df = load_data()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔍 Filter Options")

departments = sorted(df["Department"].unique())
selected_dept = st.sidebar.multiselect("Department", departments, default=departments)

semesters = sorted(df["Semester"].unique())
selected_sem = st.sidebar.multiselect("Semester", semesters, default=semesters)

min_att, max_att = int(df["Attendance"].min()), int(df["Attendance"].max())
attendance_range = st.sidebar.slider(
    "Attendance Range (%)", min_att, max_att, (min_att, max_att)
)

# ---------------- APPLY FILTERS ----------------
filtered_df = df[
    (df["Department"].isin(selected_dept)) &
    (df["Semester"].isin(selected_sem)) &
    (df["Attendance"] >= attendance_range[0]) &
    (df["Attendance"] <= attendance_range[1])
]

# ---------------- FILTERED DATA TABLE ----------------
st.subheader("📋 Filtered Student Data")
st.dataframe(filtered_df, use_container_width=True)

st.caption(f"Showing {len(filtered_df)} of {len(df)} total records")

# ---------------- SUMMARY STATISTICS ----------------
st.subheader("📊 Summary Statistics")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Average Marks", f"{filtered_df['Marks'].mean():.1f}" if len(filtered_df) else "N/A")
col2.metric("Average Attendance", f"{filtered_df['Attendance'].mean():.1f}%" if len(filtered_df) else "N/A")
col3.metric("Highest Marks", f"{filtered_df['Marks'].max()}" if len(filtered_df) else "N/A")
col4.metric("Total Students", f"{len(filtered_df)}")

with st.expander("View Detailed Statistics Table"):
    st.dataframe(filtered_df[["Marks", "Attendance"]].describe(), use_container_width=True)

# ---------------- VISUALIZATIONS ----------------
st.subheader("📈 Visual Insights")

if len(filtered_df) == 0:
    st.warning("No data available for the selected filters. Please adjust your filter options.")
else:
    row1_col1, row1_col2 = st.columns(2)

    # Bar chart: Average marks by department
    with row1_col1:
        st.markdown("**Average Marks by Department**")
        avg_marks = filtered_df.groupby("Department")["Marks"].mean().sort_values(ascending=False)
        fig1, ax1 = plt.subplots()
        ax1.bar(avg_marks.index, avg_marks.values, color="#4a6fdc")
        ax1.set_xlabel("Department")
        ax1.set_ylabel("Average Marks")
        ax1.set_ylim(0, 100)
        st.pyplot(fig1)

    # Pie chart: Semester distribution
    with row1_col2:
        st.markdown("**Semester-wise Distribution**")
        sem_counts = filtered_df["Semester"].value_counts().sort_index()
        fig2, ax2 = plt.subplots()
        ax2.pie(sem_counts.values, labels=[f"Sem {s}" for s in sem_counts.index],
                autopct="%1.1f%%", startangle=90)
        ax2.axis("equal")
        st.pyplot(fig2)

    row2_col1, row2_col2 = st.columns(2)

    # Histogram: Marks distribution
    with row2_col1:
        st.markdown("**Marks Distribution**")
        fig3, ax3 = plt.subplots()
        ax3.hist(filtered_df["Marks"], bins=10, color="#6fa8dc", edgecolor="black")
        ax3.set_xlabel("Marks")
        ax3.set_ylabel("Number of Students")
        st.pyplot(fig3)

    # Scatter plot: Attendance vs Marks
    with row2_col2:
        st.markdown("**Attendance vs Marks**")
        fig4, ax4 = plt.subplots()
        ax4.scatter(filtered_df["Attendance"], filtered_df["Marks"], color="#dc6f4a", alpha=0.7)
        ax4.set_xlabel("Attendance (%)")
        ax4.set_ylabel("Marks")
        st.pyplot(fig4)

# ---------------- DOWNLOAD BUTTON ----------------
st.subheader("⬇️ Download Filtered Data")

csv_data = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download Filtered Data as CSV",
    data=csv_data,
    file_name="filtered_student_performance.csv",
    mime="text/csv"
)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#999;'>Built with Streamlit • Student Performance Analytics Dashboard</div>",
    unsafe_allow_html=True
)