import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import shared.navbar as navbar_module
import globals
import ast

st.set_page_config(page_title="Dashboard", layout="wide")
globals.load_global_styles("globals.css")

if "page" not in st.session_state:
    st.session_state.page = "dashboard"

pages = {
    "Home": "home",
    "Rubric": "rubric",
    "Practice": "select_criteria",
    "Dashboard": "dashboard",
    "About": "about",
}

navbar_module.apply_navbar_styles()
navbar_module.navbar(pages, st.session_state.page)


## --
st.header("LeetCode Practice Dashboard")
st.divider()

#### DATASET #####
@st.cache_data
def load_data():
    df = pd.read_csv('backend/leetcode_dataset.csv')
    df['related_topics'] = df['related_topics'].fillna('')
    df['companies'] = df['companies'].fillna('')
    df['similar_questions'] = df['similar_questions'].fillna('')
    # Parse similar_questions if possible
    def parse_similar(x):
        try:
            return ast.literal_eval(x)
        except Exception:
            return []
    df['similar_questions_parsed'] = df['similar_questions'].apply(parse_similar)
    return df

df = load_data()

## --
uniq_topics = set()
for tlist in df['related_topics']:
    uniq_topics.update([t.strip() for t in tlist.split(',') if t.strip()])
uniq_topics = sorted(uniq_topics)

uniq_companies = set()
for clist in df['companies']:
    uniq_companies.update([c.strip() for c in clist.split(',') if c.strip()])
uniq_companies = sorted(uniq_companies)

col1, col2 = st.columns([0.65,1.35])

with col1:
    # LEETCODE PREMIUMS
    sel_premium = st.selectbox('Include Leetcode Premium?', options=['No', 'Yes', 'Either'], index=0)

    # ASKED BY FAANG? (Facebook, Apple, Amazon, Google, or Netflix)
    faang_options = [0, 1]
    asked_by_faang = st.selectbox(
        'Asked by FAANG? \n\n (Facebook, Apple, Amazon, Google, or Netflix)', 
        options=["All", "Yes", "No"]
    )
    if asked_by_faang == "Yes":
        faang_filter = 1
    elif asked_by_faang == "No":
        faang_filter = 0
    else:
        faang_filter = None

with col2:
    # DIFFICULTY
    selected_diffs = st.multiselect(
        "Difficulty", df["difficulty"].unique().tolist(),
        default=['Easy'])

    # COMPANIES
    st.write("")
    sel_companies = st.multiselect('Asked by SELECT Companies?', uniq_companies, default=['Google', 'Bloomberg'])

# TOPICS
default_topics = ['Array', 'Binary Search']
sel_topics = st.multiselect("Core Topics", uniq_topics, default=default_topics)
df['related_topics'] = df['related_topics'].str.replace(',', ', ', regex=False)



###### APPLY FILTERS ##### 
filtered = df[
    df['difficulty'].isin(selected_diffs) &
    (df['related_topics'].apply(lambda x: any(t in x for t in sel_topics)))
]

if sel_premium == "No":
    filtered = filtered[filtered['is_premium'] == 0]
elif sel_premium == "Yes":
    filtered = filtered[filtered['is_premium'] == 1]

if sel_companies:
    filtered = filtered[filtered['companies'].apply(lambda x: any(c in x for c in sel_companies))]

if faang_filter is not None:
    filtered = filtered[filtered["asked_by_faang"] == faang_filter]


##### STUDY PLAN ##### 
st.divider()
st.markdown(f"### Study Plan: {len(filtered)} core questions")

plan_table = filtered.groupby(['difficulty', 'related_topics']).agg(
    count=('id', 'count'),
).reset_index().sort_values(['difficulty', 'count'], ascending=[True, False])

st.write("**Practice the following number of problems for each area:**")
st.dataframe(plan_table, hide_index=True)


# SAMPLE ADDITIONAL PROBLEMS
st.divider()
st.markdown(f"### Sample Practice: {len(filtered.groupby('related_topics'))} sets")

st.markdown("""
    - Add 1-2 **Medium-Hard** problems in each topic for stretch practice if you finish all core topics. 
""")

st.markdown("""
    - You can also follow [**NeetCode's** Blind 75](https://neetcode.io/practice/practice/blind75) or FAANG-specific lists for targeted practice.
""")

for i, (topic, group) in enumerate(filtered.groupby('related_topics')):
    topics_list = topic.split(',')
    topics_md = ", ".join([f"{c.strip()}" for c in topics_list if c.strip()])

    st.markdown(f"##### {topics_md} ({len(group)} questions)")
    for _, row in group.head(2).iterrows():
        with st.expander(f"- [{row['title']}]({row['url']}) ({row['difficulty']})"):
            # TOPICS
            topics_list = row['related_topics'].split(',')
            topics_md = ", ".join([f"{c.strip()}" for c in topics_list if c.strip()])
            st.markdown(f"**Core Topics:**\n{topics_md}")

            # DIFFICULTY
            st.markdown(f"**Difficulty:** {row['difficulty']}")

            # DESCRIPTION
            st.markdown(f"**Description:**")
            st.code(f"{row['description']}")

            # ASKED BY COMPANIES
            companies_list = row['companies'].split(',')
            companies_md = ", ".join([f"{c.strip()}" for c in companies_list if c.strip()])
            st.markdown(f"**Companies:**\n{companies_md}")

            # ETC.
            st.markdown(f"**Asked by FAANG:** {'Yes' if row['asked_by_faang'] else 'No'}")
            st.markdown(f"**Acceptance Rate:** {row['acceptance_rate']}%")
            st.markdown(f"**Rating:** {row['rating']:.2f} ({row['likes']} likes / {row['dislikes']} dislikes)")
            # SOLUTION LINKS -- CSV file contents for solution_link are outdated
            st.markdown(f"**Solution Link:** [{row['url']}/editorial/)]({row['url']}/editorial/)")
