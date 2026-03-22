import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def run_app(chain: Chain, portfolio: Portfolio):
    st.set_page_config(page_title="CareerLens", page_icon="🎯", layout="wide")
    st.title("🎯 CareerLens — Job Fit Analyzer")
    st.markdown(
        "Paste a job posting URL below. CareerLens will analyze how well your "
        "profile fits the role and generate a tailored cover letter."
    )

    url_input = st.text_input(
        "Job Posting URL",
        placeholder="https://jobs.example.com/software-engineer-123",
    )

    if st.button("Analyze", type="primary"):
        if not url_input.strip():
            st.warning("Please enter a job posting URL.")
            return

        with st.spinner("Scraping job posting..."):
            try:
                loader = WebBaseLoader([url_input])
                raw_text = loader.load().pop().page_content
                cleaned = clean_text(raw_text)
            except Exception as e:
                st.error(f"Could not load the URL: {e}")
                return

        with st.spinner("Extracting job requirements..."):
            try:
                job = chain.extract_job_requirements(cleaned)
            except Exception as e:
                st.error(f"Could not parse job requirements: {e}")
                return

        portfolio.load_portfolio()
        skills = job.get("skills", [])
        links = portfolio.query_links(skills)
        flat_links = [m["links"] for sublist in links for m in sublist]

        # Layout: two columns
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📋 Job Summary")
            st.markdown(f"**Role:** {job.get('role', 'N/A')}")
            st.markdown(f"**Experience:** {job.get('experience', 'N/A')}")
            st.markdown(f"**Skills Required:** {', '.join(skills)}")
            st.markdown(f"**Description:** {job.get('description', 'N/A')}")

            st.subheader("🔍 Gap Analysis")
            with st.spinner("Analyzing your fit..."):
                gap = chain.generate_gap_analysis(job, skills)
            st.markdown(gap)

        with col2:
            st.subheader("✉️ Cover Letter")
            with st.spinner("Generating cover letter..."):
                letter = chain.generate_cover_letter(job, flat_links)
            st.code(letter, language="markdown")
            st.download_button(
                "Download Cover Letter",
                data=letter,
                file_name="cover_letter.txt",
                mime="text/plain",
            )


if __name__ == "__main__":
    run_app(Chain(), Portfolio())