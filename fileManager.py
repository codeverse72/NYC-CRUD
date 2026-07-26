"""
NEXUS FILE MANAGER — a futuristic Streamlit UI wrapper around a
Create / Read / Update / Delete file-management toolkit.

Run with:
    streamlit run file_manager_app.py
"""

import os
from pathlib import Path
from datetime import datetime

import streamlit as st

# --------------------------------------------------------------------------
# CONFIG
# --------------------------------------------------------------------------
STORAGE_DIR = Path("nexus_storage")
STORAGE_DIR.mkdir(exist_ok=True)

st.set_page_config(
    page_title="NEXUS // File Manager",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------------------------------
# FUTURISTIC THEME (CSS)
# --------------------------------------------------------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@400;600;700&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Rajdhani', sans-serif;
        }

        .stApp {
            background: radial-gradient(circle at 20% 20%, #0d1b2a 0%, #050912 55%, #000000 100%);
            color: #d8f3ff;
        }

        /* Glowing title */
        .nexus-title {
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            font-size: 2.6rem;
            text-align: center;
            background: linear-gradient(90deg, #00f0ff, #7b2ff7, #00f0ff);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: shine 4s linear infinite;
            letter-spacing: 3px;
            margin-bottom: 0;
        }
        .nexus-subtitle {
            text-align: center;
            color: #7fdcff;
            font-family: 'Rajdhani', sans-serif;
            letter-spacing: 4px;
            font-size: 0.95rem;
            margin-top: 4px;
            opacity: 0.8;
        }
        @keyframes shine {
            to { background-position: 200% center; }
        }

        /* Card containers */
        .nexus-card {
            background: rgba(13, 27, 42, 0.55);
            border: 1px solid rgba(0, 240, 255, 0.35);
            border-radius: 14px;
            padding: 22px 26px;
            box-shadow: 0 0 18px rgba(0, 240, 255, 0.12), inset 0 0 24px rgba(123, 47, 247, 0.06);
            backdrop-filter: blur(6px);
            margin-bottom: 18px;
        }

        /* Buttons */
        .stButton>button {
            font-family: 'Orbitron', sans-serif;
            background: linear-gradient(90deg, #00f0ff33, #7b2ff733);
            border: 1px solid #00f0ffaa;
            color: #e6fbff;
            border-radius: 10px;
            padding: 0.55em 1.4em;
            letter-spacing: 1.5px;
            transition: all 0.25s ease;
        }
        .stButton>button:hover {
            border-color: #00f0ff;
            box-shadow: 0 0 16px #00f0ff88;
            color: #ffffff;
            transform: translateY(-1px);
        }

        /* Inputs */
        .stTextInput>div>div>input, .stTextArea textarea {
            background: rgba(255,255,255,0.03) !important;
            border: 1px solid rgba(0,240,255,0.3) !important;
            color: #d8f3ff !important;
            border-radius: 8px !important;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #060b16 0%, #0a1424 100%);
            border-right: 1px solid rgba(0,240,255,0.15);
        }

        /* Divider glow */
        hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, #00f0ffaa, transparent);
        }

        .status-ok {
            color: #4dffa1;
            font-weight: 600;
        }
        .status-err {
            color: #ff5c7c;
            font-weight: 600;
        }
        .file-chip {
            display: inline-block;
            background: rgba(0,240,255,0.08);
            border: 1px solid rgba(0,240,255,0.35);
            padding: 4px 12px;
            border-radius: 20px;
            margin: 3px;
            font-size: 0.85rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# HEADER
# --------------------------------------------------------------------------
st.markdown('<div class="nexus-title">⟨ NEXUS FILE MANAGER ⟩</div>', unsafe_allow_html=True)
st.markdown('<div class="nexus-subtitle">CREATE · READ · UPDATE · DELETE — SYSTEM ONLINE</div>', unsafe_allow_html=True)
st.write("")

# --------------------------------------------------------------------------
# SIDEBAR — NAVIGATION + FILE LIST
# --------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🛰️ CONTROL PANEL")
    action = st.radio(
        "Select operation",
        ["📁 Create", "📖 Read", "✏️ Update", "🗑️ Delete"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("### 📡 STORED FILES")
    files = sorted(p.name for p in STORAGE_DIR.iterdir() if p.is_file())
    if files:
        for f in files:
            st.markdown(f'<span class="file-chip">{f}</span>', unsafe_allow_html=True)
    else:
        st.caption("No files in storage yet.")

    st.markdown("---")
    st.caption(f"Storage path: `{STORAGE_DIR.resolve()}`")
    st.caption(datetime.now().strftime("SYSTEM TIME %H:%M:%S"))

# --------------------------------------------------------------------------
# HELPERS
# --------------------------------------------------------------------------
def safe_path(filename: str) -> Path:
    """Keep all file operations sandboxed inside STORAGE_DIR."""
    return STORAGE_DIR / Path(filename).name


# --------------------------------------------------------------------------
# CREATE
# --------------------------------------------------------------------------
if action == "📁 Create":
    st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
    st.subheader("📁 Create a New File")

    fn = st.text_input("File name", placeholder="e.g. logs.txt")
    data = st.text_area("File content", placeholder="Type the content to write inside the file...", height=150)

    if st.button("🚀 Create File"):
        if not fn.strip():
            st.markdown('<span class="status-err">⚠ Please enter a file name.</span>', unsafe_allow_html=True)
        else:
            path = safe_path(fn)
            if path.exists():
                st.markdown('<span class="status-err">⚠ File already exists.</span>', unsafe_allow_html=True)
            else:
                try:
                    with open(path, "w") as fs:
                        fs.write(data)
                    st.markdown('<span class="status-ok">✅ File created successfully.</span>', unsafe_allow_html=True)
                    st.balloons()
                except Exception as ex:
                    st.markdown(f'<span class="status-err">⚠ Error: {ex}</span>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# READ
# --------------------------------------------------------------------------
elif action == "📖 Read":
    st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
    st.subheader("📖 Read a File")

    if files:
        fn = st.selectbox("Choose a file", files)
    else:
        fn = st.text_input("File name", placeholder="e.g. logs.txt")

    if st.button("🔍 Read File"):
        path = safe_path(fn) if fn else None
        if path and path.exists():
            try:
                with open(path, "r") as fs:
                    content = fs.read()
                st.markdown('<span class="status-ok">✅ File read successfully.</span>', unsafe_allow_html=True)
                st.code(content if content.strip() else "(file is empty)", language="text")
            except Exception as ex:
                st.markdown(f'<span class="status-err">⚠ Error: {ex}</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-err">⚠ File does not exist.</span>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# UPDATE
# --------------------------------------------------------------------------
elif action == "✏️ Update":
    st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
    st.subheader("✏️ Update a File")

    if files:
        fn = st.selectbox("Choose a file", files)
    else:
        fn = st.text_input("File name", placeholder="e.g. logs.txt")

    op = st.radio(
        "Operation",
        ["Rename", "Append content", "Overwrite content"],
        horizontal=True,
    )

    path = safe_path(fn) if fn else None

    if op == "Rename":
        new_name = st.text_input("New file name")
        if st.button("🔄 Rename"):
            if path and path.exists():
                new_path = safe_path(new_name)
                if new_path.exists():
                    st.markdown('<span class="status-err">⚠ Target name already exists.</span>', unsafe_allow_html=True)
                else:
                    try:
                        path.rename(new_path)
                        st.markdown('<span class="status-ok">✅ File renamed successfully.</span>', unsafe_allow_html=True)
                    except Exception as ex:
                        st.markdown(f'<span class="status-err">⚠ Error: {ex}</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="status-err">⚠ File does not exist.</span>', unsafe_allow_html=True)

    elif op == "Append content":
        add_text = st.text_area("Content to append")
        if st.button("➕ Append"):
            if path and path.exists():
                try:
                    with open(path, "a") as fs:
                        fs.write("\n" + add_text)
                    st.markdown('<span class="status-ok">✅ Content appended successfully.</span>', unsafe_allow_html=True)
                except Exception as ex:
                    st.markdown(f'<span class="status-err">⚠ Error: {ex}</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="status-err">⚠ File does not exist.</span>', unsafe_allow_html=True)

    elif op == "Overwrite content":
        new_text = st.text_area("New content (replaces everything)")
        if st.button("♻️ Overwrite"):
            if path and path.exists():
                try:
                    with open(path, "w") as fs:
                        fs.write(new_text)
                    st.markdown('<span class="status-ok">✅ File overwritten successfully.</span>', unsafe_allow_html=True)
                except Exception as ex:
                    st.markdown(f'<span class="status-err">⚠ Error: {ex}</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="status-err">⚠ File does not exist.</span>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# DELETE
# --------------------------------------------------------------------------
elif action == "🗑️ Delete":
    st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
    st.subheader("🗑️ Delete a File")

    if files:
        fn = st.selectbox("Choose a file", files)
    else:
        fn = st.text_input("File name", placeholder="e.g. logs.txt")
        st.info("No files currently in storage.")

    confirm = st.checkbox("I understand this action is irreversible.")

    if st.button("💥 Delete File", disabled=not confirm):
        path = safe_path(fn) if fn else None
        if path and path.exists():
            try:
                path.unlink()
                st.markdown('<span class="status-ok">✅ File deleted successfully.</span>', unsafe_allow_html=True)
            except Exception as ex:
                st.markdown(f'<span class="status-err">⚠ Error: {ex}</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-err">⚠ File does not exist.</span>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# FOOTER
# --------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    '<div style="text-align:center; opacity:0.55; font-size:0.8rem; letter-spacing:2px;">'
    "NEXUS FILE MANAGER · BUILT WITH PYTHON + STREAMLIT"
    "</div>",
    unsafe_allow_html=True,
)