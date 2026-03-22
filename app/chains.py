import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        try:
            api_key = st.secrets["GROQ_API_KEY"]
        except Exception:
            api_key = os.getenv("GROQ_API_KEY")

        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            groq_api_key=api_key,
        )

    def extract_job_requirements(self, cleaned_text: str) -> dict:
        prompt = PromptTemplate.from_template(
            """
            ### SCRAPED JOB POSTING:
            {page_data}
            ### INSTRUCTION:
            Extract the job requirements. Return ONLY valid JSON with keys:
            role, experience, skills (list), description (one sentence).
            ### VALID JSON ONLY (NO PREAMBLE):
            """
        )
        chain = prompt | self.llm | JsonOutputParser()
        return chain.invoke({"page_data": cleaned_text})

    def generate_gap_analysis(self, job: dict, candidate_skills: list) -> str:
        prompt = PromptTemplate.from_template(
            """
            ### JOB REQUIREMENTS: {job}
            ### CANDIDATE SKILLS: {candidate_skills}
            ### INSTRUCTION:
            You are a career advisor. Respond with:
            1. MATCHED SKILLS: what the candidate already has
            2. GAPS: what is missing
            3. ADVICE: one actionable step to close the biggest gap
            Under 200 words. No preamble.
            """
        )
        # Build formatted prompt string, then call llm.invoke directly
        formatted = prompt.format(job=str(job), candidate_skills=str(candidate_skills))
        return self.llm.invoke(formatted).content

    def generate_cover_letter(self, job: dict, portfolio_links: list) -> str:
        prompt = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION: {job}
            ### PORTFOLIO LINKS: {links}
            ### INSTRUCTION:
            Write a professional cover letter. Reference the specific role,
            use portfolio links as evidence, and close with a call to action.
            Under 250 words. No preamble.
            """
        )
        formatted = prompt.format(job=str(job), links=str(portfolio_links))
        return self.llm.invoke(formatted).content