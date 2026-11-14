import ast
import re
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Tech Job Market Insights", layout="wide")

TEAL = "#0F766E"
PURPLE = "#6D5BD0"
CSV_PATH = Path(__file__).with_name("tech_jobs_cleaned.csv")


def parse_skills(value):
    if not isinstance(value, str):
        return []

    tokens = re.findall(
        r"""'(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*" """.strip(),
        value
    )

    skills = []
    for token in tokens:
        try:
            skill = ast.literal_eval(token).strip()
            if skill:
                skills.append(skill)
        except (ValueError, SyntaxError):
            continue

    return list(dict.fromkeys(skills))


@st.cache_data
def load_jobs(path, modified_at):
    jobs = pd.read_csv(path, dtype="string", keep_default_na=False)

    for column in ["job_title", "country", "employment_type"]:
        jobs[column] = jobs[column].str.strip()

    jobs["skills"] = jobs["required_skills"].map(parse_skills)
    return jobs


def ranking_chart(counts, label, color, axis_title):
    chart_data = (
        counts.sort_values()
        .rename_axis(label)
        .reset_index(name="Postings")
    )

    fig = px.bar(
        chart_data,
        x="Postings",
        y=label,
        orientation="h",
        text="Postings",
        color_discrete_sequence=[color],
        template="plotly_white",
    )

    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(
        height=max(240, 36 * len(chart_data) + 80),
        margin=dict(l=12, r=30, t=16, b=45),
        font=dict(color="#1E293B", size=13),
        bargap=0.3,
    )

    if not counts.empty:
        fig.update_xaxes(
            title=axis_title,
            range=[0, counts.max() * 1.2],
            tickformat="d",
            gridcolor="#E8EDF3",
        )

    fig.update_yaxes(title=None, automargin=True)
    return fig


st.title("Tech Job Market Insights")
st.caption("Explore technology job postings, skills, and market trends.")

with st.sidebar:
    st.header("Dataset")
    st.markdown(
        "Technology job postings dataset.\n\n"
        "Snapshot: August 1, 2026.\n\n"
        "[View dataset on Hugging Face]"
        "(https://huggingface.co/datasets/zalizedata/tech-job-postings-salary-dataset)"
    )

if not CSV_PATH.is_file():
    st.error("Dataset file not found: tech_jobs_cleaned.csv")
    st.stop()

jobs = load_jobs(str(CSV_PATH), CSV_PATH.stat().st_mtime_ns)

with st.sidebar:
    st.header("Filters")

    countries = st.multiselect(
        "Country",
        sorted(jobs.loc[jobs["country"].ne(""), "country"].unique()),
        placeholder="All countries",
    )

    employment_types = st.multiselect(
        "Employment type",
        sorted(jobs.loc[jobs["employment_type"].ne(""), "employment_type"].unique()),
        placeholder="All employment types",
    )

if countries:
    jobs = jobs.loc[jobs["country"].isin(countries)]

if employment_types:
    jobs = jobs.loc[jobs["employment_type"].isin(employment_types)]

if jobs.empty:
    st.info("No postings match these filters.")
    st.stop()

title_counts = jobs.loc[
    jobs["job_title"].ne(""), "job_title"
].value_counts()

has_skills = jobs["skills"].map(bool)

total, top_title, coverage = st.columns([1, 2, 1])

total.metric("Job postings", f"{len(jobs):,}")
top_title.metric(
    "Most common job title",
    title_counts.index[0] if not title_counts.empty else "—"
)
coverage.metric("Postings with recorded skills", f"{has_skills.mean():.0%}")

overview_tab, skills_tab, data_tab = st.tabs(
    ["Market Overview", "Skills Explorer", "Job Postings"]
)

with overview_tab:
    st.subheader("Top 10 Job Titles")

    if not title_counts.empty:
        st.plotly_chart(
            ranking_chart(
                title_counts.head(10),
                "Job title",
                TEAL,
                "Number of postings",
            ),
            use_container_width=True,
        )

    st.subheader("Top 10 Countries")
    country_counts = jobs.loc[
        jobs["country"].ne("Unknown"), "country"
    ].value_counts().head(10)

    if not country_counts.empty:
        st.plotly_chart(
            ranking_chart(
                country_counts,
                "Country",
                PURPLE,
                "Number of postings",
            ),
            use_container_width=True,
        )

    st.subheader("Remote Work Distribution")

    if "is_remote" in jobs.columns:
        remote_values = jobs["is_remote"].astype(str).str.lower()
        remote_counts = remote_values.map(
            {"true": "Remote", "false": "Non-Remote"}
        ).value_counts()

        if not remote_counts.empty:
            fig = px.pie(
                names=remote_counts.index,
                values=remote_counts.values,
                hole=0.45,
                template="plotly_white",
            )
            st.plotly_chart(fig, use_container_width=True)

with skills_tab:
    st.subheader("Top Skills by Job Title")

    if not title_counts.empty:
        available_titles = title_counts.index.tolist()

        default_index = (
            available_titles.index("AI Engineer")
            if "AI Engineer" in available_titles else 0
        )

        selected_title = st.selectbox(
            "Choose a job title",
            available_titles,
            index=default_index,
        )

        role_jobs = jobs.loc[jobs["job_title"].eq(selected_title)]
        recorded_skills = role_jobs.loc[
            role_jobs["skills"].map(bool), "skills"
        ]

        st.caption(
            f"{len(role_jobs):,} matching postings · "
            f"{len(recorded_skills):,} with recorded skills"
        )

        if not recorded_skills.empty:
            top_skills = (
                recorded_skills.explode().value_counts().head(10)
            )

            st.plotly_chart(
                ranking_chart(
                    top_skills,
                    "Skill",
                    PURPLE,
                    "Number of postings mentioning the skill",
                ),
                use_container_width=True,
            )
        else:
            st.info("No skills recorded for this job title.")

with data_tab:
    st.subheader("Job Postings Preview")

    preview_columns = [
        col for col in [
            "job_title", "company", "country",
            "employment_type", "is_remote",
            "min_salary", "max_salary"
        ]
        if col in jobs.columns
    ]

    preview = jobs[preview_columns].head(20)
    st.dataframe(preview, hide_index=True, use_container_width=True)

    st.caption(
        f"Showing {len(preview):,} of {len(jobs):,} matching postings."
    )
