
import time
import streamlit as st

st.set_page_config(
    page_title="Simple Stopwatch",
    page_icon="⏱️",
    layout="centered"
)

# ---------- CSS DESIGN ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e1b4b, #312e81);
    color: white;
}

.block-container {
    max-width: 850px;
    padding-top: 3rem;
}

h1, h2, h3, p, label {
    color: white !important;
}

.stopwatch-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 8px;
}

.subtitle {
    text-align: center;
    color: #c7d2fe !important;
    font-size: 16px;
    margin-bottom: 35px;
}

.timer-card {
    background: rgba(255, 255, 255, 0.09);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 24px;
    padding: 35px 15px;
    text-align: center;
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.25);
    margin-bottom: 30px;
}

.timer-label {
    color: #c7d2fe;
    font-size: 14px;
    letter-spacing: 4px;
    margin-bottom: 15px;
}

.timer-display {
    color: #ffffff;
    font-size: clamp(32px, 7vw, 56px);
    font-weight: 800;
    font-family: monospace;
    letter-spacing: 2px;
}

div[data-testid="stButton"] button {
    width: 100%;
    min-height: 48px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.25);
    font-weight: 700;
    transition: all 0.2s ease;
}

div[data-testid="stButton"] button:hover {
    transform: translateY(-3px);
    border-color: #a5b4fc;
    color: white;
}

div[data-testid="stHorizontalBlock"] div[data-testid="column"]:nth-child(1)
div[data-testid="stButton"] button {
    background: #16a34a;
    color: white;
}

div[data-testid="stHorizontalBlock"] div[data-testid="column"]:nth-child(2)
div[data-testid="stButton"] button {
    background: #dc2626;
    color: white;
}

div[data-testid="stHorizontalBlock"] div[data-testid="column"]:nth-child(3)
div[data-testid="stButton"] button {
    background: #7c3aed;
    color: white;
}

div[data-testid="stHorizontalBlock"] div[data-testid="column"]:nth-child(4)
div[data-testid="stButton"] button {
    background: #2563eb;
    color: white;
}

.lap-card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 12px;
    padding: 13px 18px;
    margin: 8px 0;
    display: flex;
    justify-content: space-between;
    gap: 10px;
    color: white;
    font-family: monospace;
    font-size: 16px;
}

.footer {
    text-align: center;
    color: #a5b4fc;
    margin-top: 35px;
    font-size: 13px;
}

@media (max-width: 600px) {
    .stopwatch-title {
        font-size: 30px;
    }

    .timer-card {
        padding: 25px 5px;
    }

    .timer-display {
        letter-spacing: 0;
    }
}
</style>
""", unsafe_allow_html=True)


# ---------- SESSION STATE ----------
if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "elapsed_time" not in st.session_state:
    st.session_state.elapsed_time = 0.0

if "laps" not in st.session_state:
    st.session_state.laps = []


# ---------- TIME FORMAT FUNCTION ----------
def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60

    return f"{hours:02d}:{minutes:02d}:{secs:05.2f}"


# ---------- TITLE ----------
st.markdown("""
<div class="stopwatch-title">⏱️ Simple Stopwatch</div>
<div class="subtitle">
    Track every second. Make every moment count.
</div>
""", unsafe_allow_html=True)


# ---------- CALCULATE TIME ----------
current_time = st.session_state.elapsed_time

if st.session_state.start_time is not None:
    current_time += (
        time.perf_counter() - st.session_state.start_time
    )


# ---------- TIMER DISPLAY ----------
st.markdown(f"""
<div class="timer-card">
    <div class="timer-label">ELAPSED TIME</div>
    <div class="timer-display">{format_time(current_time)}</div>
</div>
""", unsafe_allow_html=True)


# ---------- BUTTONS ----------
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("▶ Start", use_container_width=True):
        if st.session_state.start_time is None:
            st.session_state.start_time = time.perf_counter()
            st.rerun()

with col2:
    if st.button("⏹ Stop", use_container_width=True):
        if st.session_state.start_time is not None:
            st.session_state.elapsed_time += (
                time.perf_counter() - st.session_state.start_time
            )
            st.session_state.start_time = None
            st.rerun()

with col3:
    if st.button("🔄 Reset", use_container_width=True):
        st.session_state.start_time = None
        st.session_state.elapsed_time = 0.0
        st.session_state.laps = []
        st.rerun()

with col4:
    if st.button("🚩 Lap", use_container_width=True):
        if st.session_state.start_time is not None:
            st.session_state.laps.append(
                format_time(current_time)
            )
            st.rerun()
        else:
            st.warning("Please start the stopwatch first!")


# ---------- LAP HISTORY ----------
if st.session_state.laps:
    st.markdown("### 🏁 Lap History")

    for idx, lap in enumerate(st.session_state.laps, 1):
        st.markdown(f"""
        <div class="lap-card">
            <span>🏁 Lap {idx}</span>
            <strong>{lap}</strong>
        </div>
        """, unsafe_allow_html=True)


# ---------- FOOTER ----------
st.markdown("""
<div class="footer">
    SIMPLE STOPWATCH • BUILT WITH PYTHON & STREAMLIT
</div>
""", unsafe_allow_html=True)
