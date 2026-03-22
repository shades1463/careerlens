# 🎯 CareerLens — Intelligent Job Fit Analyzer

CareerLens helps job seekers instantly understand how well they fit any role.
Paste a job posting URL and get a semantic gap analysis + tailored cover letter,
powered by Llama 3.1 and vector search.

## Live Demo
[careerlens-yourname.streamlit.app](https://careerlens-mrpxw67vhujwkvjd27xxvt.streamlit.app)

## Architecture
Job URL → WebLoader → Llama 3.1 (extract skills) → ChromaDB (semantic match) → Gap Analysis + Cover Letter

## Tech Stack
- **LLM:** Llama 3.1 70B via Groq
- **Framework:** LangChain
- **Vector DB:** ChromaDB
- **UI:** Streamlit
- **Testing:** Pytest

## Setup

### 1. Clone and install
\`\`\`bash
git clone https://github.com/YOUR_USERNAME/careerlens.git
cd careerlens
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
\`\`\`

### 2. Add your Groq API key
\`\`\`bash
echo "GROQ_API_KEY=your_key_here" > .env
\`\`\`
Get a free key at console.groq.com

### 3. Update your portfolio
Edit `app/resource/my_portfolio.csv` with your actual skills and GitHub links.

### 4. Run
\`\`\`bash
streamlit run app/main.py
\`\`\`

### 5. Run tests
\`\`\`bash
pytest tests/ -v
\`\`\`

## Why this project?
Traditional job matching is keyword-based — it misses that "built microservices"
and "distributed systems experience" mean the same thing. CareerLens uses
semantic vector search (the same pattern behind LinkedIn's recommendation engine)
to match your actual experience to what a role needs.