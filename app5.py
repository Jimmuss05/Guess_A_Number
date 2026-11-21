
import streamlit as st
import time

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="Number Hunt Game",
    page_icon="🎯",
    layout="centered"
)

# -----------------------------
# SESSION STATE INITIALIZATION
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "low" not in st.session_state:
    st.session_state.low = 1

if "high" not in st.session_state:
    st.session_state.high = 1000

if "guess" not in st.session_state:
    st.session_state.guess = 500

if "guesses" not in st.session_state:
    st.session_state.guesses = 0

if "start_time" not in st.session_state:
    st.session_state.start_time = 0

if "time_limit" not in st.session_state:
    st.session_state.time_limit = 60

if "result" not in st.session_state:
    st.session_state.result = ""

# -----------------------------
# START / RESET GAME
# -----------------------------
def start_game():
    st.session_state.low = 1
    st.session_state.high = 1000
    st.session_state.guess = 500
    st.session_state.guesses = 1
    st.session_state.start_time = time.time()
    st.session_state.result = ""
    st.session_state.page = "game"

# -----------------------------
# CHECK REMAINING TIME
# -----------------------------
def get_remaining_time():
    elapsed = time.time() - st.session_state.start_time
    return max(0, int(st.session_state.time_limit - elapsed))

# -----------------------------
# PROCESS PLAYER RESPONSE
# -----------------------------
def process_response(response):
    if response == "Too low":
        st.session_state.low = st.session_state.guess + 1

    elif response == "Too high":
        st.session_state.high = st.session_state.guess - 1

    elif response == "Correct":
        st.session_state.result = "won"
        st.session_state.page = "result"
        return

    # Check for contradictory feedback
    if st.session_state.low > st.session_state.high:
        st.session_state.result = "invalid"
        st.session_state.page = "result"
        return

    # Generate next midpoint guess
    st.session_state.guess = (
        st.session_state.low + st.session_state.high
    ) // 2

    st.session_state.guesses += 1

# -----------------------------
# HOME SCREEN
# -----------------------------
if st.session_state.page == "home":

    st.title("🎯 Number Hunt Game")

    st.markdown("""
    ### Welcome to Number Hunt!

    Think of a secret integer between **1 and 1000**.

    Do not enter your secret number!

    The computer will try to guess your number.

    ### How to Play

    1. Think of a secret number between 1 and 1000.
    2. Click **Start Game**.
    3. The computer will make its first guess.
    4. Tell the computer whether its guess is:
       - 🔽 **Too low** – Your secret number is higher.
       - 🔼 **Too high** – Your secret number is lower.
       - 🎉 **Correct** – The computer guessed your number!
    5. The computer will use your feedback to make another guess.
    6. Try to complete the game before the 60-second timer expires!

    **Important:** Give honest and consistent feedback.
    """)

    st.divider()

    if st.button("🚀 Start Game", use_container_width=True):
        start_game()
        st.rerun()

# -----------------------------
# GAME SCREEN
# -----------------------------
elif st.session_state.page == "game":

    remaining = get_remaining_time()

    # Timer expiration
    if remaining <= 0:
        st.session_state.result = "timeout"
        st.session_state.page = "result"
        st.rerun()

    st.title("🎯 Number Hunt Game")

    st.info("Think of your secret number. Do not enter it!")

    # Countdown timer
    st.subheader(f"⏳ Time Remaining: {remaining} seconds")

    st.progress(remaining / st.session_state.time_limit)

    st.divider()

    # Display computer guess
    st.subheader("🤖 Computer's Guess")

    st.markdown(
        f"<h1 style='text-align:center; color:#2196F3;'>"
        f"{st.session_state.guess}</h1>",
        unsafe_allow_html=True
    )

    # Display game information
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Possible Range",
            f"{st.session_state.low} - {st.session_state.high}"
        )

    with col2:
        st.metric(
            "Number of Guesses",
            st.session_state.guesses
        )

    st.divider()

    st.subheader("What is your response?")

    # Player response buttons
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔽 Too Low", use_container_width=True):
            process_response("Too low")
            st.rerun()

    with col2:
        if st.button("🔼 Too High", use_container_width=True):
            process_response("Too high")
            st.rerun()

    with col3:
        if st.button("🎉 Correct", use_container_width=True):
            process_response("Correct")
            st.rerun()

    st.caption("The timer continues while you play.")

    # Refresh screen to update countdown
    time.sleep(1)
    st.rerun()

# -----------------------------
# RESULT SCREEN
# -----------------------------
elif st.session_state.page == "result":

    st.title("🏁 Game Over!")

    st.divider()

    if st.session_state.result == "won":

        st.success("🎉 Congratulations! The computer found your number!")

        st.balloons()

        st.write(
            f"The computer guessed your number in "
            f"**{st.session_state.guesses} guesses**."
        )

    elif st.session_state.result == "timeout":

        st.warning("⏰ Time's up!")

        st.write(
            "The computer did not receive a Correct response "
            "before the timer expired."
        )

        st.write(
            "The computer's success was not confirmed."
        )

        st.write(
            f"Total guesses made: **{st.session_state.guesses}**"
        )

    elif st.session_state.result == "invalid":

        st.error("❌ Contradictory Feedback Detected!")

        st.write(
            "Your responses resulted in an empty possible number range."
        )

        st.write(
            "Please provide consistent feedback when playing again."
        )

        st.write(
            f"Total guesses made: **{st.session_state.guesses}**"
        )

    st.divider()

    if st.button("🔄 Play Again", use_container_width=True):
        start_game()
        st.rerun()
