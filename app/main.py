import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from app.chains import Chain
from app.portfolio import Portfolio
from app.utils import clean_text

# ── page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CareerLens",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600&family=IBM+Plex+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0a !important;
    color: #c8c8c8;
    font-family: 'IBM Plex Sans', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background:
        linear-gradient(rgba(255,180,0,0.015) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,180,0,0.015) 1px, transparent 1px),
        #0a0a0a !important;
    background-size: 48px 48px !important;
}

[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="collapsedControl"],
footer { display: none !important; }

section[data-testid="stSidebar"] { display: none !important; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0a0a0a; }
::-webkit-scrollbar-thumb { background: #2a2a2a; border-radius: 2px; }

.block-container {
    max-width: 1100px !important;
    padding: 0 2rem 4rem !important;
    margin: 0 auto !important;
}

.cl-hero {
    padding: 5rem 0 3.5rem;
    text-align: center;
    position: relative;
}

.cl-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.25em;
    color: #ffb400;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    opacity: 0;
    animation: fadeUp 0.6s ease forwards 0.1s;
}

.cl-logo {
    font-family: 'IBM Plex Mono', monospace;
    font-size: clamp(3.5rem, 8vw, 6rem);
    font-weight: 600;
    letter-spacing: -0.02em;
    line-height: 1;
    color: #f0f0f0;
    margin-bottom: 0.5rem;
    opacity: 0;
    animation: fadeUp 0.7s ease forwards 0.2s;
}

.cl-logo span {
    color: #ffb400;
    position: relative;
}

.cl-logo span::after {
    content: '';
    position: absolute;
    bottom: 4px;
    left: 0;
    width: 100%;
    height: 2px;
    background: #ffb400;
    transform: scaleX(0);
    transform-origin: left;
    animation: lineIn 0.5s ease forwards 0.9s;
}

.cl-tagline {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 1rem;
    font-weight: 300;
    color: #666;
    letter-spacing: 0.04em;
    margin-top: 1rem;
    opacity: 0;
    animation: fadeUp 0.7s ease forwards 0.4s;
}

.cl-hero::before, .cl-hero::after {
    content: '';
    position: absolute;
    width: 20px;
    height: 20px;
    border-color: #2a2a2a;
    border-style: solid;
    opacity: 0;
    animation: fadeIn 0.5s ease forwards 0.8s;
}
.cl-hero::before { top: 3.5rem; left: 0; border-width: 1px 0 0 1px; }
.cl-hero::after  { top: 3.5rem; right: 0; border-width: 1px 1px 0 0; }

.cl-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #2a2a2a 20%, #2a2a2a 80%, transparent);
    margin: 0.5rem 0 2.5rem;
    opacity: 0;
    animation: fadeIn 0.6s ease forwards 0.6s;
}

.cl-status {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    margin-bottom: 2.5rem;
    padding: 0.75rem 1.25rem;
    background: #0f0f0f;
    border: 1px solid #1e1e1e;
    border-left: 2px solid #ffb400;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: #444;
    letter-spacing: 0.08em;
    opacity: 0;
    animation: fadeUp 0.5s ease forwards 0.7s;
}
.cl-status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #2d5a1b;
    box-shadow: 0 0 6px #4caf50;
    animation: pulse 2s ease-in-out infinite;
    flex-shrink: 0;
}
.cl-status span { color: #555; }
.cl-status strong { color: #888; font-weight: 500; }

.cl-input-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    color: #444;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.cl-input-label::before {
    content: '//';
    color: #ffb400;
    font-size: 0.6rem;
}

[data-testid="stTextInput"] > div > div {
    background: #0f0f0f !important;
    border: 1px solid #222 !important;
    border-radius: 0 !important;
    padding: 0 !important;
    transition: border-color 0.2s ease !important;
}
[data-testid="stTextInput"] > div > div:focus-within {
    border-color: #ffb400 !important;
    box-shadow: 0 0 0 1px #ffb40020 !important;
}
[data-testid="stTextInput"] input {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.85rem !important;
    color: #d0d0d0 !important;
    background: transparent !important;
    padding: 0.9rem 1rem !important;
    letter-spacing: 0.02em !important;
    caret-color: #ffb400 !important;
}
[data-testid="stTextInput"] input::placeholder { color: #333 !important; }
[data-testid="stTextInput"] label { display: none !important; }

[data-testid="stButton"] button {
    background: #ffb400 !important;
    color: #0a0a0a !important;
    border: none !important;
    border-radius: 0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    padding: 0.85rem 2rem !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
}
[data-testid="stButton"] button:hover {
    background: #ffc933 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(255,180,0,0.25) !important;
}
[data-testid="stButton"] button:active {
    transform: translateY(0) !important;
}

[data-testid="stSpinner"] {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.75rem !important;
    color: #444 !important;
    letter-spacing: 0.05em !important;
}

.cl-panel {
    background: #0d0d0d;
    border: 1px solid #1e1e1e;
    padding: 1.75rem;
    position: relative;
    animation: panelIn 0.5s ease forwards;
}
.cl-panel::before {
    content: attr(data-label);
    position: absolute;
    top: -1px;
    left: 1.75rem;
    background: #0a0a0a;
    padding: 0 0.5rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    color: #ffb400;
    text-transform: uppercase;
    transform: translateY(-50%);
}
.cl-panel-index {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    color: #2a2a2a;
    position: absolute;
    top: 0.75rem;
    right: 1rem;
    letter-spacing: 0.1em;
}

.cl-field-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    color: #3a3a3a;
    text-transform: uppercase;
    margin-bottom: 0.35rem;
    margin-top: 1.25rem;
}
.cl-field-label:first-child { margin-top: 0.25rem; }

.cl-field-value {
    font-size: 0.9rem;
    color: #c0c0c0;
    line-height: 1.5;
    font-weight: 300;
}

.cl-role-badge {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
    font-weight: 500;
    color: #f0f0f0;
    border-bottom: 1px solid #ffb400;
    padding-bottom: 1px;
}

.cl-skill-chip {
    display: inline-block;
    background: #141414;
    border: 1px solid #222;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    color: #888;
    padding: 0.25rem 0.6rem;
    margin: 0.2rem 0.2rem 0.2rem 0;
    letter-spacing: 0.05em;
}

.cl-gap-content {
    font-size: 0.875rem;
    line-height: 1.8;
    color: #aaa;
    font-weight: 300;
    white-space: pre-wrap;
    border-left: 2px solid #1e1e1e;
    padding-left: 1rem;
    margin-top: 0.5rem;
}

.cl-letter {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    line-height: 1.9;
    color: #999;
    white-space: pre-wrap;
    background: #080808;
    border: 1px solid #191919;
    padding: 1.5rem;
    position: relative;
    overflow: hidden;
}
.cl-letter::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 2px;
    height: 100%;
    background: linear-gradient(180deg, #ffb400, transparent);
    opacity: 0.4;
}

[data-testid="stDownloadButton"] button {
    background: transparent !important;
    color: #ffb400 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    padding: 0.6rem 1.25rem !important;
    margin-top: 1rem !important;
    transition: all 0.15s ease !important;
    width: 100% !important;
}
[data-testid="stDownloadButton"] button:hover {
    border-color: #ffb400 !important;
    background: rgba(255,180,0,0.05) !important;
}

[data-testid="stAlert"] {
    background: #0f0f0f !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.75rem !important;
}

.cl-metric-row {
    display: flex;
    gap: 1px;
    margin-top: 2.5rem;
    opacity: 0;
    animation: fadeUp 0.5s ease forwards 0.9s;
}
.cl-metric {
    flex: 1;
    background: #0d0d0d;
    border: 1px solid #191919;
    padding: 1rem;
    text-align: center;
}
.cl-metric-val {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.5rem;
    font-weight: 600;
    color: #ffb400;
    line-height: 1;
    margin-bottom: 0.35rem;
}
.cl-metric-key {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 0.2em;
    color: #333;
    text-transform: uppercase;
}

.cl-footer {
    margin-top: 4rem;
    padding-top: 1.5rem;
    border-top: 1px solid #141414;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    color: #252525;
    letter-spacing: 0.1em;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
@keyframes lineIn {
    from { transform: scaleX(0); }
    to   { transform: scaleX(1); }
}
@keyframes panelIn {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.4; }
}

[data-testid="stColumns"] { gap: 1.5rem !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }

.stDeployButton,
#MainMenu,
[data-testid="stDecoration"] { display: none !important; }
</style>
""", unsafe_allow_html=True)


# ── helpers ───────────────────────────────────────────────────────────────────
def skill_chips(skills: list) -> str:
    return "".join(f'<span class="cl-skill-chip">{s}</span>' for s in skills)


def render_panel(label: str, index: str, content_html: str):
    st.markdown(
        f'<div class="cl-panel" data-label="{label}">'
        f'<span class="cl-panel-index">{index}</span>'
        f'{content_html}'
        f'</div>',
        unsafe_allow_html=True,
    )


# ── hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cl-hero">
    <div class="cl-eyebrow">Intelligent Job Fit Analysis</div>
    <div class="cl-logo">Career<span>Lens</span></div>
    <div class="cl-tagline">
        Paste a job URL &mdash; get a semantic gap analysis and a cover letter in seconds
    </div>
</div>
<div class="cl-divider"></div>
""", unsafe_allow_html=True)


# ── status bar ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cl-status">
    <div class="cl-status-dot"></div>
    <span>SYS</span><strong>ONLINE</strong>
    <span>&nbsp;|&nbsp;</span>
    <span>MODEL</span><strong>LLAMA-3.3-70B</strong>
    <span>&nbsp;|&nbsp;</span>
    <span>STORE</span><strong>CHROMADB</strong>
    <span>&nbsp;|&nbsp;</span>
    <span>PIPELINE</span><strong>LANGCHAIN</strong>
</div>
""", unsafe_allow_html=True)


# ── metrics row ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="cl-metric-row">
    <div class="cl-metric">
        <div class="cl-metric-val">3</div>
        <div class="cl-metric-key">Analysis steps</div>
    </div>
    <div class="cl-metric">
        <div class="cl-metric-val">70B</div>
        <div class="cl-metric-key">Model params</div>
    </div>
    <div class="cl-metric">
        <div class="cl-metric-val">~8s</div>
        <div class="cl-metric-key">Avg response</div>
    </div>
    <div class="cl-metric">
        <div class="cl-metric-val">RAG</div>
        <div class="cl-metric-key">Match method</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='margin-top:2.5rem'></div>", unsafe_allow_html=True)


# ── input ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="cl-input-label">Target job posting URL</div>', unsafe_allow_html=True)

col_input, col_btn = st.columns([5, 1])
with col_input:
    url_input = st.text_input(
        label="url",
        placeholder="https://jobs.example.com/software-engineer",
        label_visibility="collapsed",
    )
with col_btn:
    st.markdown("<div style='margin-top:0.05rem'></div>", unsafe_allow_html=True)
    analyze = st.button("ANALYZE →")

st.markdown("<div style='margin-top:0.25rem'></div>", unsafe_allow_html=True)


# ── analysis ──────────────────────────────────────────────────────────────────
if analyze:
    if not url_input.strip():
        st.warning("// No URL provided. Enter a job posting URL to continue.")
        st.stop()

    chain = Chain()
    portfolio = Portfolio()

    with st.spinner("// SCRAPING  →  fetching job posting..."):
        try:
            loader = WebBaseLoader([url_input])
            raw = loader.load().pop().page_content
            cleaned = clean_text(raw)
        except Exception as e:
            st.error(f"// ERR  →  Could not load URL: {e}")
            st.stop()

    with st.spinner("// EXTRACTING  →  parsing requirements with LLM..."):
        try:
            job = chain.extract_job_requirements(cleaned)
        except Exception as e:
            st.error(f"// ERR  →  Extraction failed: {e}")
            st.stop()

    with st.spinner("// MATCHING  →  querying vector store..."):
        portfolio.load_portfolio()
        skills = job.get("skills", [])
        links = portfolio.query_links(skills)
        flat_links = [m["links"] for sublist in links for m in sublist]

    st.markdown("<div style='margin-top:2rem'></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        role  = job.get("role", "N/A")
        exp   = job.get("experience", "N/A")
        desc  = job.get("description", "")
        chips = (
            skill_chips(skills)
            if skills
            else '<span style="color:#333;font-size:0.75rem;font-family:IBM Plex Mono,monospace">none extracted</span>'
        )

        render_panel("Job snapshot", "01 / 03", f"""
            <div class="cl-field-label">Role</div>
            <div class="cl-field-value"><span class="cl-role-badge">{role}</span></div>
            <div class="cl-field-label">Experience</div>
            <div class="cl-field-value">{exp}</div>
            <div class="cl-field-label">Description</div>
            <div class="cl-field-value">{desc}</div>
            <div class="cl-field-label">Required skills</div>
            <div style="margin-top:0.4rem">{chips}</div>
        """)

        st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)

        with st.spinner("// ANALYZING  →  comparing profile to requirements..."):
            gap_text = chain.generate_gap_analysis(job, skills)

        render_panel("Gap analysis", "02 / 03", f"""
            <div class="cl-gap-content">{gap_text}</div>
        """)

    with col_right:
        with st.spinner("// GENERATING  →  writing cover letter..."):
            letter = chain.generate_cover_letter(job, flat_links)

        render_panel("Cover letter", "03 / 03", f"""
            <div class="cl-letter">{letter}</div>
        """)

        st.download_button(
            label="⬇  EXPORT  COVER_LETTER.TXT",
            data=letter,
            file_name="cover_letter.txt",
            mime="text/plain",
        )


# ── footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cl-footer">
    <span>CAREERLENS &copy; 2025</span>
    <span>LLM + RAG PIPELINE</span>
    <span>BUILD v1.0.0</span>
</div>
""", unsafe_allow_html=True)

