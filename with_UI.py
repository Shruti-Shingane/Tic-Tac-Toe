import streamlit as st
import numpy as np

st.set_page_config(
    page_title="Tic Tac Toe",
    page_icon="🎮",
    layout="centered"
)

# ---------- Styling ----------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #312e81 100%);
        color: white;
    }

    .main-title {
        text-align: center;
        font-size: 3.2rem;
        font-weight: 800;
        margin-bottom: 0;
        background: linear-gradient(90deg, #60a5fa, #c084fc, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle {
        text-align: center;
        color: #cbd5e1;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }

    .turn-card {
        text-align: center;
        padding: 12px;
        border-radius: 16px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.12);
        margin-bottom: 18px;
        font-size: 1.15rem;
        font-weight: 700;
    }

    div.stButton > button {
        width: 100%;
        height: 95px;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.16);
        background: rgba(255,255,255,0.09);
        color: white;
        font-size: 2.5rem;
        font-weight: 800;
        box-shadow: 0 8px 25px rgba(0,0,0,0.18);
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        border-color: #a78bfa;
        background: rgba(167,139,250,0.18);
    }

    .score-box {
        text-align: center;
        padding: 14px;
        border-radius: 16px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.10);
    }

    .score-number {
        font-size: 2rem;
        font-weight: 800;
    }

    .small-label {
        color: #cbd5e1;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


# ---------- Game Logic ----------
def new_game():
    st.session_state.board = np.zeros((3, 3), dtype=int)
    st.session_state.current = 1
    st.session_state.result = None


def check_winner(board):
    if 3 in np.sum(board, axis=0) or 3 in np.sum(board, axis=1):
        return "X"

    if -3 in np.sum(board, axis=0) or -3 in np.sum(board, axis=1):
        return "O"

    if np.trace(board) == 3 or np.trace(np.fliplr(board)) == 3:
        return "X"

    if np.trace(board) == -3 or np.trace(np.fliplr(board)) == -3:
        return "O"

    if 0 not in board:
        return "Draw"

    return None


if "board" not in st.session_state:
    new_game()


# ---------- Header ----------
st.markdown('<div class="main-title">🎮 Tic Tac Toe</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Classic game • Built with Python, NumPy & Streamlit</div>',
    unsafe_allow_html=True
)

# ---------- Turn ----------
if st.session_state.result is None:
    player = "X" if st.session_state.current == 1 else "O"
    st.markdown(
        f'<div class="turn-card">Current Turn: <span style="color:#c084fc;">{player}</span></div>',
        unsafe_allow_html=True
    )
else:
    result = st.session_state.result
    if result == "Draw":
        st.warning("🤝 It's a Draw!")
    else:
        st.success(f"🏆 Player {result} Wins!")


# ---------- Board ----------
symbols = {0: " ", 1: "✕", -1: "◯"}

for r in range(3):
    cols = st.columns(3, gap="small")

    for c in range(3):
        value = st.session_state.board[r, c]

        if value == 0 and st.session_state.result is None:
            label = " "
        else:
            label = symbols[value]

        if cols[c].button(label, key=f"cell_{r}_{c}", use_container_width=True):
            if st.session_state.board[r, c] == 0:
                st.session_state.board[r, c] = st.session_state.current

                result = check_winner(st.session_state.board)

                if result is not None:
                    st.session_state.result = result
                else:
                    st.session_state.current *= -1

                st.rerun()


# ---------- Score / Controls ----------
st.markdown("---")

x_wins = st.session_state.get("x_wins", 0)
o_wins = st.session_state.get("o_wins", 0)
draws = st.session_state.get("draws", 0)

# Update persistent score only when a new result appears
if st.session_state.result is not None:
    score_key = "counted_result"
    if st.session_state.get(score_key) != st.session_state.result:
        if st.session_state.result == "X":
            st.session_state.x_wins = x_wins + 1
        elif st.session_state.result == "O":
            st.session_state.o_wins = o_wins + 1
        else:
            st.session_state.draws = draws + 1
        st.session_state[score_key] = st.session_state.result

x_wins = st.session_state.get("x_wins", 0)
o_wins = st.session_state.get("o_wins", 0)
draws = st.session_state.get("draws", 0)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        f'<div class="score-box"><div class="small-label">Player X</div>'
        f'<div class="score-number">{x_wins}</div></div>',
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f'<div class="score-box"><div class="small-label">Draws</div>'
        f'<div class="score-number">{draws}</div></div>',
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f'<div class="score-box"><div class="small-label">Player O</div>'
        f'<div class="score-number">{o_wins}</div></div>',
        unsafe_allow_html=True
    )

st.write("")

if st.button("🔄 New Game", use_container_width=True):
    new_game()
    st.rerun()

if st.button("🗑️ Reset Score", use_container_width=True):
    st.session_state.x_wins = 0
    st.session_state.o_wins = 0
    st.session_state.draws = 0
    st.session_state.pop("counted_result", None)
    new_game()
    st.rerun()

st.caption("Tip: X always starts. Click an empty square to make your move.")
