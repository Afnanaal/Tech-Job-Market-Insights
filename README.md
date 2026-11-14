# Tech Job Market Insights Dashboard

## Project Overview
Tech Job Market Insights is a data analytics project that explores technology job postings to identify trends in job titles, required technical skills, remote work opportunities, and salary information.

The project uses Python, Pandas, and data visualization techniques for data analysis, with an interactive dashboard built using Streamlit.

## Project Objectives
- Analyze the most common technology job roles.
- Identify the most frequently requested technical skills.
- Explore job posting distribution across countries.
- Analyze remote and non-remote opportunities.
- Examine salary data availability and salary currencies.

## Dataset
- **Source:** [Hugging Face – Tech Job Postings Salary Dataset](https://huggingface.co/datasets/zalizedata/tech-job-postings-salary-dataset)
- **Snapshot date:** August 1, 2026.
- **Original records:** 35,417
- **Records after removing duplicate job IDs:** 31,676
- **Final analyzed records:** 29,194

The dataset is licensed under CC BY-NC 4.0. Please refer to the original dataset page for attribution and license details.

## Technologies Used
- Python
- Pandas
- Plotly
- Streamlit
- Google Colab

## Project Workflow
1. Data collection
2. Data cleaning and preprocessing
3. Exploratory Data Analysis (EDA)
4. Data visualization
5. Interactive dashboard development

## Key Findings
- Software Engineering and Data Engineering roles are highly represented.
- Python, SQL, and AWS are among the most frequently listed technical skills.
- The United States has the highest number of job postings.
- Full-time positions represent the largest known employment category.
- More than half of the postings do not disclose salary information.
- Approximately 29.3% of postings are classified as remote.

## Repository Structure
- `Tech_Job_Market_Insights.ipynb` – Data cleaning, analysis, and visualizations.
- `app.py` – Streamlit dashboard application.
- `tech_jobs_cleaned.csv` – Cleaned dataset used by the dashboard.

## Limitations
- The dataset represents a snapshot dated August 1, 2026, not live job market data.
- It is collected from public company career pages and does not represent all job postings.
- Salary values may use different currencies and pay periods, so direct comparisons require normalization.
- The analyzed subset was filtered based on Latin-character job titles and should not be interpreted as exclusively English-language postings.

## Future Improvements
- Add more interactive filters and visualizations.
- Improve salary analysis by normalizing currencies and pay periods.
- Expand market analysis across job categories and locations.

---

**Developed as part of an Applied AI Bootcamp project.**
# Team members:
- Afnan Alharbi
- Taif Alharbi 
- Nawaf Alshaye
