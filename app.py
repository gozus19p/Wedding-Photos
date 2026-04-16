import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Il nostro matrimonio",
    page_icon="💍",
    layout="centered",
    initial_sidebar_state="collapsed",
)

APP_PASSWORD = os.getenv("APP_PASSWORD", "matrimonio2025")

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=Jost:wght@300;400&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Jost', sans-serif;
    font-weight: 300;
    -webkit-text-size-adjust: 100%;
}
.stApp { background-color: #FAFAF8; }
h1, h2, h3 {
    font-family: 'Cormorant Garamond', serif !important;
    font-weight: 300 !important;
    letter-spacing: 0.04em;
    color: #2C2A26 !important;
}

/* ── Mobile viewport fix ── */
.block-container {
    padding-left: 1.2rem !important;
    padding-right: 1.2rem !important;
    padding-top: 0 !important;
    max-width: 480px !important;
}

/* ── Hero ── */
.wedding-hero { text-align: center; padding: 2.5rem 0 1.8rem; }
.wedding-hero .names {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(2rem, 8vw, 3.2rem);
    font-weight: 300;
    font-style: italic;
    color: #2C2A26;
    letter-spacing: 0.06em;
    line-height: 1.1;
}
.wedding-hero .date {
    font-size: 0.72rem;
    font-weight: 300;
    letter-spacing: 0.28em;
    color: #9A8C7E;
    text-transform: uppercase;
    margin-top: 0.6rem;
}
.divider { display: flex; align-items: center; gap: 1rem; margin: 1.4rem auto; max-width: 200px; }
.divider-line { flex: 1; height: 1px; background: #C0694A; opacity: 0.35; }
.divider-diamond { width: 5px; height: 5px; background: #C0694A; opacity: 0.5; transform: rotate(45deg); flex-shrink: 0; }

/* ── Auth card ── */
.auth-card {
    background: #FFFFFF;
    border: 1px solid #E8E2DA;
    border-radius: 4px;
    padding: 2rem 1.8rem;
    margin: 0 auto;
}
.auth-label {
    font-size: 0.68rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #9A8C7E;
    margin-bottom: 0.5rem;
}

/* ── Inputs ── */
.stTextInput > label { display: none; }
.stTextInput input {
    border: 1px solid #D8D0C6 !important;
    border-radius: 4px !important;
    background: #FAFAF8 !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 1rem !important;
    color: #2C2A26 !important;
    padding: 0.75rem 1rem !important;
    min-height: 48px !important;
}
.stTextInput input:focus { border-color: #C0694A !important; box-shadow: 0 0 0 2px rgba(192,105,74,0.15) !important; }

/* ── Buttons ── */
.stButton > button {
    width: 100% !important;
    background: #C0694A !important;
    color: #FAFAF8 !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    padding: 0.85rem 1rem !important;
    min-height: 48px !important;
    transition: opacity 0.2s ease !important;
    cursor: pointer !important;
}
.stButton > button:hover { opacity: 0.82 !important; }
.stButton > button:active { opacity: 0.65 !important; }

/* ── Error ── */
.error-msg {
    font-size: 0.82rem;
    color: #A84028;
    letter-spacing: 0.04em;
    text-align: center;
    margin-top: 0.8rem;
    padding: 0.6rem;
    background: #FBF0EC;
    border-radius: 4px;
    border: 1px solid #EDCABB;
}

/* ── Streamlit widget text — force visibility ── */
div[data-testid="stRadio"] label p,
div[data-testid="stRadio"] label span,
div[data-testid="stCheckbox"] label p,
div[data-testid="stCheckbox"] label span {
    color: #2C2A26 !important;
    opacity: 1 !important;
    visibility: visible !important;
    font-family: 'Jost', sans-serif !important;
}

footer { display: none !important; }
#MainMenu { display: none !important; }
header { display: none !important; }
</style>
"""


def render_hero():
    couple_name = os.getenv("COUPLE_NAMES", "Sofia & Marco")
    wedding_date = os.getenv("WEDDING_DATE", "14 Giugno 2025")
    st.markdown(
        f"""
    <div class="wedding-hero">
        <div class="names">{couple_name}</div>
        <div class="date">{wedding_date}</div>
        <div class="divider">
            <div class="divider-line"></div>
            <div class="divider-diamond"></div>
            <div class="divider-line"></div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def main():

    from pages.main import render_main_page

    render_main_page()


if __name__ == "__main__":
    main()
