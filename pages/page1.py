import streamlit as st

st.header("Page 1 - Mock Interview")

## --
st.subheader("Hello.")
col1, col2 = st.columns(2)

with col1:
    st.image(
        "https://www.zippia.com/wp-content/uploads/2021/02/tips-to-prepare-for-onsite-interview.jpg",
        width=500
    )

with col2:
    st.image(
        "https://cs.unc.edu/wp-content/uploads/sites/1265/2023/03/Helpful-Technical-Interview-Resources-1024x1024.png",
        width=450
    )

## --
st.subheader("World.")
col1, col2 = st.columns(2)

with col1:
    st.image(
        "https://www.blackstonetutors.com/wp-content/uploads/2024/03/AAMC-Professional-Readiness-Question-Bank-1024x844.png",
        width=450
    )

with col2:
    st.image(
        "https://www.blackstonetutors.com/wp-content/uploads/2024/03/AAMC-Professional-Readiness-Exam-Preparation-1024x844.png",
        width=450
    )

