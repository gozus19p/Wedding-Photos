import streamlit as st
import os
from datetime import datetime
from pipeline.storage import upload_photo, save_metadata, get_all_photos, update_moment
from pipeline.clip_classifier import classify_image_bytes, MOMENT_LABELS

# ── Palette ──────────────────────────────────────────────────────────────────
# Terracotta: #C0694A  |  Salvia: #7A8C6E  |  Panna: #FAFAF8  |  Scuro: #2C2A26

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;1,300&family=Jost:wght@300;400&display=swap');

html, body, [class*="css"] {
    font-family: 'Jost', sans-serif;
    font-weight: 300;
    -webkit-text-size-adjust: 100%;
}
.stApp { background-color: #FAFAF8; }
h1,h2,h3 {
    font-family: 'Cormorant Garamond', serif !important;
    font-weight: 300 !important;
    color: #2C2A26 !important;
    letter-spacing: 0.04em;
}
footer { display: none !important; }
#MainMenu { display: none !important; }
header { display: none !important; }

/* ── Mobile layout ── */
.block-container {
    padding-left: 1.1rem !important;
    padding-right: 1.1rem !important;
    padding-top: 0.5rem !important;
    max-width: 560px !important;
}

/* ── Page header ── */
.page-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    padding: 1rem 0 1rem;
    border-bottom: 1px solid rgba(192,105,74,0.2);
    margin-bottom: 1.4rem;
}
.page-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(1.5rem, 5vw, 1.9rem);
    font-style: italic;
    font-weight: 300;
    color: #2C2A26;
    line-height: 1.1;
}
.page-subtitle {
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #9A8C7E;
    margin-top: 0.3rem;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    border-bottom: 1px solid #E8E2DA !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Jost', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: #9A8C7E !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    padding: 0.8rem 1.4rem !important;
    border-radius: 0 !important;
    min-height: 44px !important;
}
.stTabs [aria-selected="true"] {
    color: #C0694A !important;
    border-bottom: 2px solid #C0694A !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ── Inputs ── */
.stTextInput > label {
    font-family: 'Jost', sans-serif !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: #7A8C6E !important;
    font-weight: 400 !important;
}
.stTextInput input {
    border: 1px solid #D0CCBF !important;
    border-radius: 4px !important;
    background: #FAFAF8 !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 1rem !important;
    color: #2C2A26 !important;
    padding: 0.75rem 1rem !important;
    min-height: 48px !important;
}
.stTextInput input:focus {
    border-color: #7A8C6E !important;
    box-shadow: 0 0 0 2px rgba(122,140,110,0.18) !important;
}

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

/* Logout button — secondary style */
.btn-secondary > button {
    background: transparent !important;
    color: #9A8C7E !important;
    border: 1px solid #D0CCBF !important;
    font-size: 0.68rem !important;
    padding: 0.5rem 0.9rem !important;
    min-height: 36px !important;
    width: auto !important;
    letter-spacing: 0.18em !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    border: 1.5px dashed rgba(192,105,74,0.35) !important;
    border-radius: 8px !important;
    background: #FFFFFF !important;
    padding: 1.2rem !important;
}
[data-testid="stFileUploader"] label {
    font-family: 'Jost', sans-serif !important;
    font-size: 0.78rem !important;
    color: #9A8C7E !important;
    letter-spacing: 0.1em !important;
}
[data-testid="stFileUploaderDropzone"] button {
    background: transparent !important;
    border: 1px solid #C0694A !important;
    color: #C0694A !important;
    border-radius: 4px !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.14em !important;
    min-height: 40px !important;
}

/* ── Messages ── */
.success-banner {
    background: #F3F7F0;
    border-left: 3px solid #7A8C6E;
    border-radius: 4px;
    padding: 1rem 1.2rem;
    margin: 1rem 0;
    text-align: center;
}
.success-banner .big {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.4rem;
    font-style: italic;
    color: #4A5C40;
    display: block;
    margin-bottom: 0.2rem;
}
.success-banner .sub {
    font-size: 0.75rem;
    color: #7A8C6E;
    letter-spacing: 0.1em;
}
.result-row {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.55rem 0.8rem;
    background: #FFFFFF;
    border: 1px solid #E8E2DA;
    border-radius: 4px;
    margin: 0.35rem 0;
    font-size: 0.8rem;
    color: #2C2A26;
}
.result-row .fname {
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    color: #5C5448;
    font-size: 0.75rem;
}
.result-row .tag {
    background: rgba(122,140,110,0.12);
    color: #4A5C40;
    border-radius: 20px;
    padding: 0.2rem 0.6rem;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    white-space: nowrap;
}
.error-row {
    padding: 0.55rem 0.8rem;
    background: #FBF0EC;
    border: 1px solid #EDCABB;
    border-radius: 4px;
    margin: 0.35rem 0;
    font-size: 0.78rem;
    color: #A84028;
}
.hint {
    font-size: 0.72rem;
    color: #9A8C7E;
    letter-spacing: 0.08em;
    text-align: center;
    margin-top: 0.4rem;
}

/* ── Gallery ── */
.stats-strip {
    display: flex;
    gap: 0.7rem;
    margin-bottom: 1.2rem;
}
.stat-pill {
    flex: 1;
    background: #FFFFFF;
    border: 1px solid #E8E2DA;
    border-radius: 6px;
    padding: 0.6rem 0.5rem;
    text-align: center;
}
.stat-n {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.6rem;
    color: #C0694A;
    font-weight: 300;
    line-height: 1;
    display: block;
}
.stat-l {
    font-size: 0.6rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #9A8C7E;
    display: block;
    margin-top: 0.15rem;
}

/* Radio filter pills */
.stRadio > label {
    font-family: 'Jost', sans-serif !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: #9A8C7E !important;
    font-weight: 400 !important;
    margin-bottom: 0.5rem !important;
}
div[data-testid="stRadio"] > div {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 0.4rem !important;
}
div[data-testid="stRadio"] label {
    display: flex !important;
    align-items: center !important;
    min-height: 36px !important;
    cursor: pointer !important;
}
div[data-testid="stRadio"] label p,
div[data-testid="stRadio"] label span {
    font-family: 'Jost', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 400 !important;
    color: #2C2A26 !important;
    opacity: 1 !important;
    visibility: visible !important;
}

.moment-tag {
    font-size: 0.6rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #7A8C6E;
    margin-top: 0.2rem;
    display: block;
}
.guest-tag {
    font-size: 0.62rem;
    color: #B0A898;
    display: block;
}

.empty-state {
    text-align: center;
    padding: 3rem 1rem;
    color: #B0A898;
    font-size: 0.85rem;
    letter-spacing: 0.08em;
}

/* ── Gallery grid: 2 cols on mobile ── */
@media (max-width: 480px) {
    .block-container { padding-left: 0.8rem !important; padding-right: 0.8rem !important; }
}
</style>
"""

MOMENT_EMOJI = {
    "cerimonia": "⛪",
    "cena": "🍽",
    "ricevimento": "🥂",
    "balli": "🎶",
    "altro": "📷",
}


def _upload_and_classify(file) -> dict:
    file_bytes = file.read()
    timestamp = datetime.utcnow().isoformat()
    safe_ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S%f")
    object_key = f"photos/{safe_ts}_{file.name}"

    public_url = upload_photo(
        file_bytes=file_bytes,
        object_key=object_key,
        content_type=file.type or "image/jpeg",
    )
    save_metadata(
        object_key=object_key,
        public_url=public_url,
        filename=file.name,
        file_size=len(file_bytes),
        uploaded_at=timestamp,
    )
    moment, confidence = classify_image_bytes(file_bytes)
    update_moment(object_key=object_key, moment=moment, confidence=round(confidence, 4))

    return {"filename": file.name, "moment": moment, "confidence": confidence}


def render_upload_tab():
    # ── State machine: "form" | "done" ──────────────────────────
    if st.session_state.get("upload_state") == "done":
        results = st.session_state.get("upload_results", [])
        errors = st.session_state.get("upload_errors", [])

        st.markdown(
            f"""
        <div class="success-banner">
            <span class="big">Grazie!</span>
            <span class="sub">{len(results)} foto condivise con gli sposi</span>
        </div>
        """,
            unsafe_allow_html=True,
        )

        for r in results:
            emoji = MOMENT_EMOJI.get(r["moment"], "📷")
            st.markdown(
                f"""
            <div class="result-row">
                <span>{emoji}</span>
                <span class="fname">{r["filename"]}</span>
                <span class="tag">{r["moment"]}</span>
            </div>
            """,
                unsafe_allow_html=True,
            )

        for err in errors:
            st.markdown(f'<div class="error-row">{err}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Carica altre foto"):
            st.session_state.pop("upload_state", None)
            st.session_state.pop("upload_results", None)
            st.session_state.pop("upload_errors", None)
            st.rerun()
        return

    # ── Form ─────────────────────────────────────────────────────
    uploaded_files = st.file_uploader(
        "Seleziona le foto da condividere",
        type=["jpg", "jpeg", "png", "heic", "webp"],
        accept_multiple_files=True,
        key="file_uploader",
    )
    st.markdown(
        '<div class="hint">JPG · PNG · HEIC — puoi selezionare più file</div>',
        unsafe_allow_html=True,
    )

    if uploaded_files:
        st.markdown(
            f'<div class="hint" style="margin-top:.8rem">{len(uploaded_files)} foto selezionate</div>',
            unsafe_allow_html=True,
        )
        # Preview: 2 cols on mobile, up to 4
        n_cols = min(len(uploaded_files), 4)
        cols = st.columns(n_cols)
        for i, f in enumerate(uploaded_files[:8]):
            with cols[i % n_cols]:
                st.image(f, use_container_width=True)
        if len(uploaded_files) > 8:
            st.markdown(
                f'<div class="hint">… e altre {len(uploaded_files) - 8}</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Carica e condividi"):
        if not uploaded_files:
            st.markdown(
                '<div class="error-row">Seleziona almeno una foto</div>',
                unsafe_allow_html=True,
            )
            return

        progress = st.progress(0, text="Caricamento in corso…")
        results, errors = [], []

        for i, file in enumerate(uploaded_files):
            progress.progress(
                (i + 0.5) / len(uploaded_files),
                text=f"Elaboro {i+1}/{len(uploaded_files)}…",
            )
            try:
                results.append(_upload_and_classify(file))
            except Exception as e:
                errors.append(f"{file.name}: {e}")
            progress.progress((i + 1) / len(uploaded_files))

        progress.empty()

        # Salva nome per riproporlo al prossimo caricamento
        st.session_state["upload_state"] = "done"
        st.session_state["upload_results"] = results
        st.session_state["upload_errors"] = errors
        st.rerun()


def render_gallery_tab():
    photos = get_all_photos()
    total = len(photos)

    if total == 0:
        st.markdown(
            '<div class="empty-state">Nessuna foto ancora.<br>Sii il primo a condividere!</div>',
            unsafe_allow_html=True,
        )
        return

    unclassified = sum(1 for p in photos if not p.get("moment"))

    st.markdown(
        f"""
    <div class="stats-strip">
        <div class="stat-pill"><span class="stat-n">{total}</span><span class="stat-l">Foto</span></div>
        <div class="stat-pill"><span class="stat-n">{len(MOMENT_LABELS)}</span><span class="stat-l">Momenti</span></div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    filter_options = ["Tutte"] + [
        f"{MOMENT_EMOJI.get(m,'📷')} {m.capitalize()}" for m in MOMENT_LABELS
    ]
    selected = st.radio("Filtra", filter_options, horizontal=True, key="gallery_filter")

    if selected == "Tutte":
        filtered = photos
    else:
        moment_key = selected.split(" ", 1)[1].lower()
        filtered = [p for p in photos if p.get("moment") == moment_key]

    if not filtered:
        st.markdown(
            '<div class="empty-state">Nessuna foto in questa categoria</div>',
            unsafe_allow_html=True,
        )
        return

    st.markdown(
        f'<div class="hint" style="text-align:left;margin-bottom:.8rem">{len(filtered)} foto</div>',
        unsafe_allow_html=True,
    )

    # 2 columns on mobile, 3 on wider screens
    cols = st.columns(2)
    for i, photo in enumerate(filtered):
        with cols[i % 2]:
            url = photo.get("public_url")
            if url:
                st.image(url, use_container_width=True)
            else:
                st.markdown("📷")
            moment = photo.get("moment", "")

            emoji = MOMENT_EMOJI.get(moment, "") if moment else ""
            st.markdown(
                f'<span class="moment-tag">{emoji} {moment}</span>',
                unsafe_allow_html=True,
            )


def render_main_page():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    couple = os.getenv("COUPLE_NAMES", "Sofia & Marco")
    wedding_date = os.getenv("WEDDING_DATE", "14 Giugno 2025")

    col_title, col_btn = st.columns([4, 1])
    with col_title:
        st.markdown(
            f"""
        <div class="page-header">
            <div>
                <div class="page-title">{couple}</div>
                <div class="page-subtitle">{wedding_date}</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col_btn:
        st.markdown("<div style='padding-top:1rem'>", unsafe_allow_html=True)
        st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    tab_upload, tab_gallery = st.tabs(["Carica foto", "Galleria"])

    with tab_upload:
        render_upload_tab()

    with tab_gallery:
        render_gallery_tab()
