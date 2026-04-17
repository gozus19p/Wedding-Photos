import streamlit as st
import os
from pipeline.storage import get_all_photos

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;1,300&family=Jost:wght@300;400&display=swap');

html, body, [class*="css"] { font-family: 'Jost', sans-serif; font-weight: 300; }
.stApp { background-color: #FAFAF8; }
h1,h2,h3 { font-family: 'Cormorant Garamond', serif !important; font-weight: 300 !important; color: #2C2A26 !important; }
footer { display: none !important; }
#MainMenu { display: none !important; }
header { display: none !important; }

.page-header {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    padding: 1.5rem 0 1.2rem;
    border-bottom: 1px solid #E8E4DE;
    margin-bottom: 1.8rem;
}
.page-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.8rem;
    font-style: italic;
    color: #2C2A26;
    font-weight: 300;
}
.photo-total {
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #8A7F72;
}

.filter-bar {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-bottom: 1.8rem;
}
.filter-pill {
    display: inline-block;
    padding: 0.3rem 0.9rem;
    border: 1px solid #DDD8D0;
    border-radius: 20px;
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #8A7F72;
    cursor: pointer;
    background: #FFFFFF;
    transition: all 0.15s;
}
.filter-pill.active {
    background: #2C2A26;
    color: #FAFAF8;
    border-color: #2C2A26;
}

.stButton > button {
    background: #2C2A26 !important;
    color: #FAFAF8 !important;
    border: none !important;
    border-radius: 2px !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    padding: 0.5rem 1.2rem !important;
}
.stButton > button:hover { opacity: 0.75 !important; }

.classify-btn > button {
    background: #5A4E3C !important;
}

.stats-row {
    display: flex;
    gap: 1.5rem;
    margin-bottom: 1.8rem;
    flex-wrap: wrap;
}
.stat-card {
    background: #FFFFFF;
    border: 1px solid #E8E4DE;
    border-radius: 2px;
    padding: 0.8rem 1.2rem;
    min-width: 130px;
}
.stat-label {
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #8A7F72;
    margin-bottom: 0.25rem;
}
.stat-value {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.6rem;
    color: #2C2A26;
    font-weight: 300;
}

.photo-card {
    position: relative;
    overflow: hidden;
    border-radius: 2px;
}
.moment-badge {
    display: inline-block;
    font-size: 0.62rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #8A7F72;
    margin-top: 0.3rem;
    margin-bottom: 0.8rem;
}
.guest-name-small {
    font-size: 0.68rem;
    color: #B0A898;
    letter-spacing: 0.1em;
}

.classify-section {
    background: #FFFFFF;
    border: 1px solid #E8E4DE;
    border-radius: 2px;
    padding: 1.5rem;
    margin-bottom: 1.8rem;
}
.classify-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.1rem;
    font-style: italic;
    color: #2C2A26;
    margin-bottom: 0.5rem;
}
.classify-desc {
    font-size: 0.78rem;
    color: #8A7F72;
    letter-spacing: 0.06em;
    margin-bottom: 1rem;
}

.empty-state {
    text-align: center;
    padding: 3rem 1rem;
    color: #B0A898;
    font-size: 0.82rem;
    letter-spacing: 0.1em;
}
</style>
"""


def render_gallery_page():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    couple = os.getenv("COUPLE_NAMES", "Sofia & Marco")
    photos = get_all_photos()
    total = len(photos)

    st.markdown(
        f'<div class="page-title">Galleria · {couple}</div>', unsafe_allow_html=True
    )

    if total == 0:
        st.markdown(
            '<div class="empty-state">Nessuna foto ancora.</div>',
            unsafe_allow_html=True,
        )
        return

    st.markdown(
        f'<div class="photo-total" style="margin-bottom:1rem">{total} foto</div>',
        unsafe_allow_html=True,
    )

    num_cols = 3
    cols = st.columns(num_cols)
    for i, photo in enumerate(photos):
        with cols[i % num_cols]:
            url = photo.get("public_url")
            if url:
                st.image(url, use_container_width=True)
            else:
                st.markdown("📷")
