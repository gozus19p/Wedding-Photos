import streamlit as st
import os
from datetime import datetime
from pipeline.storage import upload_photo

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;1,300&family=Jost:wght@300;400&display=swap');

html, body, [class*="css"] { font-family: 'Jost', sans-serif; font-weight: 300; }
.stApp { background-color: #FAFAF8; }
h1,h2,h3 { font-family: 'Cormorant Garamond', serif !important; font-weight: 300 !important; color: #2C2A26 !important; letter-spacing: 0.04em; }
footer { display: none !important; }
#MainMenu { display: none !important; }
header { display: none !important; }

.page-header {
    text-align: center;
    padding: 2rem 0 1.5rem;
    border-bottom: 1px solid #E8E4DE;
    margin-bottom: 2rem;
}
.page-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2rem;
    font-style: italic;
    font-weight: 300;
    color: #2C2A26;
}
.page-subtitle {
    font-size: 0.75rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #8A7F72;
    margin-top: 0.4rem;
}

.upload-zone {
    border: 1px dashed #C8C0B5;
    border-radius: 2px;
    padding: 2.5rem 1.5rem;
    text-align: center;
    background: #FFFFFF;
    margin-bottom: 1.5rem;
}
.upload-hint {
    font-size: 0.78rem;
    color: #8A7F72;
    letter-spacing: 0.1em;
}

.stTextInput > label {
    font-family: 'Jost', sans-serif !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: #8A7F72 !important;
    font-weight: 400 !important;
}
.stTextInput input {
    border: 1px solid #DDD8D0 !important;
    border-radius: 2px !important;
    background: #FAFAF8 !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 0.9rem !important;
    color: #2C2A26 !important;
}
.stTextInput input:focus { border-color: #2C2A26 !important; box-shadow: none !important; }

.stButton > button {
    width: 100%;
    background: #2C2A26 !important;
    color: #FAFAF8 !important;
    border: none !important;
    border-radius: 2px !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.22em !important;
    text-transform: uppercase !important;
    padding: 0.7rem 1rem !important;
}
.stButton > button:hover { opacity: 0.75 !important; }

.success-msg {
    background: #F0F5EC;
    border: 1px solid #C8D9BB;
    border-radius: 2px;
    padding: 1rem 1.2rem;
    font-size: 0.82rem;
    color: #3B6D11;
    letter-spacing: 0.06em;
    text-align: center;
}
.error-msg {
    background: #FBF0EC;
    border: 1px solid #E8C4B5;
    border-radius: 2px;
    padding: 1rem 1.2rem;
    font-size: 0.82rem;
    color: #993C1D;
    letter-spacing: 0.06em;
    text-align: center;
}

.photo-count {
    font-size: 0.72rem;
    color: #8A7F72;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    text-align: center;
    margin-bottom: 1rem;
}

.logout-link {
    font-size: 0.7rem;
    color: #B0A898;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    text-align: center;
    cursor: pointer;
    text-decoration: underline;
    margin-top: 3rem;
    display: block;
}
</style>
"""


def render_upload_page():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    couple = os.getenv("COUPLE_NAMES", "Sofia & Marco")
    wedding_date = os.getenv("WEDDING_DATE", "14 Giugno 2025")

    st.markdown(
        f"""
    <div class="page-header">
        <div class="page-title">Condividi i tuoi scatti</div>
        <div class="page-subtitle">{couple} · {wedding_date}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="upload-zone">', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Carica le tue foto",
        type=["jpg", "jpeg", "png", "heic", "webp"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )
    st.markdown(
        '<div class="upload-hint">JPG, PNG, HEIC · più file contemporaneamente</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if uploaded_files:
        st.markdown(
            f'<div class="photo-count">{len(uploaded_files)} foto selezionate</div>',
            unsafe_allow_html=True,
        )

        cols = st.columns(min(len(uploaded_files), 4))
        for i, f in enumerate(uploaded_files[:8]):
            with cols[i % 4]:
                st.image(f, use_container_width=True)
        if len(uploaded_files) > 8:
            st.markdown(
                f'<div class="upload-hint">... e altre {len(uploaded_files) - 8}</div>',
                unsafe_allow_html=True,
            )

    if st.button("Carica le foto"):
        if not uploaded_files:
            st.markdown(
                '<div class="error-msg">Seleziona almeno una foto</div>',
                unsafe_allow_html=True,
            )
        else:
            progress = st.progress(0, text="Caricamento in corso…")
            errors = []
            success_count = 0

            for i, file in enumerate(uploaded_files):
                try:
                    file_bytes = file.read()
                    timestamp = datetime.utcnow().isoformat()
                    object_key = f"photos/{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{i}_{file.name}"

                    upload_photo(
                        file_bytes=file_bytes,
                        object_key=object_key,
                        content_type=file.type or "image/jpeg",
                    )

                    success_count += 1
                except Exception as e:
                    errors.append(f"{file.name}: {str(e)}")

                progress.progress(
                    (i + 1) / len(uploaded_files),
                    text=f"Caricamento {i+1}/{len(uploaded_files)}…",
                )

            progress.empty()

            if success_count > 0:
                st.markdown(
                    f'<div class="success-msg">Grazie! '
                    f"{success_count} foto caricate con successo.</div>",
                    unsafe_allow_html=True,
                )
            if errors:
                for err in errors:
                    st.markdown(
                        f'<div class="error-msg">Errore: {err}</div>',
                        unsafe_allow_html=True,
                    )
