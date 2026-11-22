
import streamlit as st
import pandas as pd

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------
st.set_page_config(
    page_title="Student Grade Manager",
    page_icon="🎓",
    layout="wide"
)

# --------------------------------
# CUSTOM CSS
# --------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #101827, #1e293b);
    color: white;
}

.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #60a5fa;
}

.subtitle {
    color: #cbd5e1;
    font-size: 16px;
}

div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1e40af, #6d28d9);
    padding: 18px;
    border-radius: 15px;
    border: 1px solid #475569;
}

div.stButton > button {
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: bold;
    height: 45px;
}

div.stButton > button:hover {
    border: 1px solid white;
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #111c30;
}

h1, h2, h3, p, label {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------
# SESSION STATE
# --------------------------------
if "students" not in st.session_state:
    st.session_state.students = []

# --------------------------------
# GRADE CALCULATION
# --------------------------------
def calculate_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    elif percentage >= 40:
        return "E"
    else:
        return "Fail"

# --------------------------------
# HEADER
# --------------------------------
st.markdown(
    '<div class="main-title">🎓 Student Grade Manager</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Manage students • Track marks • Analyse performance</div>',
    unsafe_allow_html=True
)

st.divider()

# --------------------------------
# SIDEBAR
# --------------------------------
st.sidebar.title("📚 Navigation")

menu = st.sidebar.radio(
    "Select Menu",
    [
        "Dashboard",
        "Add Student",
        "Student Records",
        "Performance Report"
    ]
)

st.sidebar.info("Student Management System")

# --------------------------------
# DASHBOARD
# --------------------------------
if menu == "Dashboard":

    st.subheader("📊 Dashboard Overview")

    total_students = len(st.session_state.students)

    if total_students > 0:
        average = sum(
            s["Percentage"] for s in st.session_state.students
        ) / total_students

        passed = sum(
            1 for s in st.session_state.students
            if s["Percentage"] >= 40
        )

        failed = total_students - passed

    else:
        average = 0
        passed = 0
        failed = 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Students", total_students)
    col2.metric("Average Score", f"{average:.1f}%")
    col3.metric("Passed", passed)
    col4.metric("Failed", failed)

    st.divider()

    if total_students > 0:
        st.subheader("🏆 Recent Student Records")

        df = pd.DataFrame(st.session_state.students)
        st.dataframe(df, use_container_width=True)

        st.subheader("📈 Grade Distribution")

        grade_counts = df["Grade"].value_counts().sort_index()
        st.bar_chart(grade_counts)

    else:
        st.info("No student records yet. Go to Add Student to get started.")

# --------------------------------
# ADD STUDENT
# --------------------------------
elif menu == "Add Student":

    st.subheader("➕ Add New Student")

    with st.form("student_form"):

        name = st.text_input("Student Name")
        roll = st.text_input("Roll Number")
        class_name = st.text_input("Class / Department")

        st.markdown("### 📝 Enter Subject Marks")

        col1, col2 = st.columns(2)

        with col1:
            maths = st.number_input(
                "Mathematics",
                min_value=0,
                max_value=100,
                value=0
            )

            science = st.number_input(
                "Science",
                min_value=0,
                max_value=100,
                value=0
            )

        with col2:
            english = st.number_input(
                "English",
                min_value=0,
                max_value=100,
                value=0
            )

            computer = st.number_input(
                "Computer",
                min_value=0,
                max_value=100,
                value=0
            )

        submitted = st.form_submit_button(
            "✨ Save Student Record",
            use_container_width=True
        )

        if submitted:

            if not name.strip() or not roll.strip() or not class_name.strip():
                st.error("Please enter the student name, roll number and class.")

            elif any(s["Roll Number"].lower() == roll.strip().lower()
                     for s in st.session_state.students):
                st.error("This roll number already exists.")

            else:
                total = maths + science + english + computer
                percentage = total / 4
                grade = calculate_grade(percentage)

                student = {
                    "Name": name.strip(),
                    "Roll Number": roll.strip(),
                    "Class": class_name.strip(),
                    "Mathematics": maths,
                    "Science": science,
                    "English": english,
                    "Computer": computer,
                    "Total": total,
                    "Percentage": round(percentage, 2),
                    "Grade": grade,
                    "Result": "Pass" if percentage >= 40 else "Fail"
                }

                st.session_state.students.append(student)

                st.success(f"Student {name} added successfully!")
                st.balloons()

# --------------------------------
# STUDENT RECORDS
# --------------------------------
elif menu == "Student Records":

    st.subheader("📋 Student Records")

    if st.session_state.students:

        df = pd.DataFrame(st.session_state.students)

        search = st.text_input("🔍 Search by student name or roll number")

        if search:
            df = df[
                df["Name"].str.contains(search, case=False, na=False) |
                df["Roll Number"].str.contains(search, case=False, na=False)
            ]

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download Student Records (CSV)",
            data=csv,
            file_name="student_records.csv",
            mime="text/csv"
        )

        st.divider()

        st.subheader("🗑️ Delete Student Record")

        selected_roll = st.selectbox(
            "Select Roll Number",
            [s["Roll Number"] for s in st.session_state.students]
        )

        if st.button("Delete Selected Student"):
            st.session_state.students = [
                s for s in st.session_state.students
                if s["Roll Number"] != selected_roll
            ]
            st.success("Student record deleted.")
            st.rerun()

    else:
        st.info("No student records available.")

# --------------------------------
# PERFORMANCE REPORT
# --------------------------------
elif menu == "Performance Report":

    st.subheader("🏆 Student Performance Report")

    if st.session_state.students:

        df = pd.DataFrame(st.session_state.students)

        top_student = df.loc[df["Percentage"].idxmax()]

        col1, col2 = st.columns(2)

        col1.metric(
            "Top Performer",
            top_student["Name"]
        )

        col2.metric(
            "Highest Percentage",
            f'{top_student["Percentage"]:.2f}%'
        )

        st.divider()

        st.subheader("📊 Student Percentage Chart")

        chart_data = df.set_index("Name")[["Percentage"]]
        st.bar_chart(chart_data)

        st.subheader("📚 Subject Average Marks")

        subjects = [
            "Mathematics",
            "Science",
            "English",
            "Computer"
        ]

        subject_average = df[subjects].mean()

        st.bar_chart(subject_average)

        st.subheader("🎯 Grade Summary")

        st.dataframe(
            df[["Name", "Roll Number", "Percentage", "Grade", "Result"]],
            use_container_width=True,
            hide_index=True
        )

    else:
        st.warning("Add student records to view performance reports.")

# --------------------------------
# FOOTER
# --------------------------------
st.divider()

st.markdown(
    "<center>💙 Student Grade Manager | Built with Python & Streamlit</center>",
    unsafe_allow_html=True
)