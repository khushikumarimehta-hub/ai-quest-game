import streamlit as st
import random
import json
from pathlib import Path

st.set_page_config(page_title="AI QUEST", page_icon="🧠", layout="centered")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0b1120, #152743);
    color: #f1f5f9;
}
.block-container {
    max-width: 900px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}
h1 {
    color: #93c5fd !important;
    font-weight: 800 !important;
}
h2, h3 {
    color: #dbeafe !important;
}
div.stButton > button {
    background: linear-gradient(90deg, #2563eb, #4f46e5);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.65rem 1.2rem;
    font-weight: 700;
    transition: 0.2s;
}
div.stButton > button:hover {
    background: linear-gradient(90deg, #1d4ed8, #4338ca);
    color: white;
    border: none;
    transform: translateY(-2px);
}
div[data-testid="stProgressBar"] > div > div > div {
    background: linear-gradient(90deg, #60a5fa, #818cf8);
}
div[data-testid="stMetric"] {
    background: rgba(30, 41, 59, 0.8);
    border: 1px solid #334155;
    padding: 16px;
    border-radius: 14px;
}
div[data-testid="stAlert"] {
    border-radius: 12px;
}
hr {
    border-color: #334155;
}
</style>
""", unsafe_allow_html=True)

QUESTIONS = [
    ("What is Artificial Intelligence?", ["Machines performing tasks requiring intelligence", "Only storing data", "Only doing calculations", "Computer hardware"], 0, "AI enables learning, reasoning and problem-solving."),
    ("What is the purpose of the Turing Test?", ["Measure computer speed", "Evaluate human-like machine conversation", "Measure memory", "Test internet speed"], 1, "It evaluates whether a machine's conversation resembles a human's."),
    ("A rational agent selects actions to:", ["Act randomly", "Maximize expected performance", "Use maximum memory", "Avoid all actions"], 1, "A rational agent chooses actions expected to perform best."),
    ("An agent receives information using:", ["Actuators", "Sensors", "Printers", "Compilers"], 1, "Sensors gather information from the environment."),
    ("Which component helps an agent act?", ["Sensors", "Actuators", "Databases", "Memory cards"], 1, "Actuators carry out actions."),
    ("Which is an AI application?", ["Medical diagnosis support", "A wooden chair", "A blank sheet", "A ruler"], 0, "AI can analyze medical information."),
    ("A fully observable environment provides:", ["All relevant state information", "Only hidden information", "No information", "Random information"], 0, "The agent can observe all relevant aspects of the state."),
    ("An environment with several interacting agents is:", ["Multi-agent", "Single-agent", "Always static", "Always observable"], 0, "Multi-agent environments contain multiple interacting agents."),
    ("A problem space includes:", ["States, actions and goals", "Only a screen", "Only a database", "Only an answer"], 0, "Problem spaces describe states, actions and goal conditions."),
    ("Which structure is used by BFS?", ["Queue", "Stack", "Printer", "Compiler"], 0, "BFS explores nodes level by level using a queue."),
    ("Which structure is associated with DFS?", ["Queue", "Stack", "Monitor", "Scanner"], 1, "DFS commonly uses a stack or recursion."),
    ("A heuristic is:", ["An estimate guiding search", "A guaranteed solution", "A virus", "A storage device"], 0, "A heuristic estimates how promising a state is."),
    ("Hill climbing normally selects:", ["An improving neighboring state", "Every state at once", "A random answer only", "The oldest record"], 0, "It moves toward a neighboring state with a better evaluation."),
    ("A CSP consists of:", ["Variables, domains and constraints", "Only images", "Only actions", "Only databases"], 0, "These are the three basic components of a constraint satisfaction problem."),
    ("Means-end analysis attempts to:", ["Reduce the gap between current and goal states", "Ignore the goal", "Delete every state", "Avoid planning"], 0, "It chooses actions that reduce the difference between current and goal states."),
    ("AI is used in speech recognition.", ["True", "False"], 0, "AI can identify spoken words from audio."),
    ("BFS explores the deepest node first.", ["True", "False"], 1, "BFS explores level by level; DFS goes deep first."),
    ("A static environment does not change while an agent decides.", ["True", "False"], 0, "A static environment remains unchanged during decision-making."),
    ("A rational agent must know the future with certainty.", ["True", "False"], 1, "Rational decisions can be made under uncertainty."),
    ("CSPs can be used for timetable scheduling.", ["True", "False"], 0, "Timetables can be represented with variables and constraints."),
    ("BFS finds a shortest path in an unweighted graph because it explores by depth.", ["Both true and reason explains assertion", "Both true but no explanation", "Assertion true, reason false", "Assertion false, reason true"], 0, "Level-order exploration finds a minimum-edge path."),
    ("DFS can follow an infinite branch and miss another solution.", ["Both true and reason explains assertion", "Both true but no explanation", "Assertion true, reason false", "Assertion false, reason true"], 0, "An infinite branch can prevent DFS from backtracking."),
    ("Heuristics can guide informed search by estimating goal proximity.", ["Both true and reason explains assertion", "Both true but no explanation", "Assertion true, reason false", "Assertion false, reason true"], 0, "Heuristics help prioritize promising states."),
    ("Sensors perceive the environment, while actuators perform actions.", ["Both true and reason explains assertion", "Both true but no explanation", "Assertion true, reason false", "Assertion false, reason true"], 1, "Both statements are true, but the second does not explain the first."),
    ("Hill climbing can get stuck at a local maximum because it examines neighbors.", ["Both true and reason explains assertion", "Both true but no explanation", "Assertion true, reason false", "Assertion false, reason true"], 0, "Local improvement may not lead to the global best solution."),
    ("Exploring possible states to find a solution is called ____.", ["Search", "Printing", "Formatting", "Encryption"], 0, "Search explores states or paths."),
    ("BFS uses a ____ to manage waiting nodes.", ["Queue", "Stack", "Monitor", "Printer"], 0, "A queue follows first-in, first-out order."),
    ("DFS commonly uses a ____.", ["Stack", "Queue", "Camera", "Scanner"], 0, "A stack supports depth-first exploration."),
    ("In a CSP, allowed values for a variable form its ____.", ["Domain", "Actuator", "Heuristic", "Percept"], 0, "A domain lists possible values."),
    ("An agent's success is assessed by its ____ measure.", ["Performance", "Storage", "Display", "Network"], 0, "The performance measure defines success."),
    ("BFS is best matched with:", ["Exploring level by level", "Exploring one branch deeply", "Local improvement", "Constraint assignment"], 0, "BFS explores each depth before the next."),
    ("DFS is best matched with:", ["Level-by-level exploration", "Deep exploration before backtracking", "Human conversation testing", "Scheduling only"], 1, "DFS explores deeply before backtracking."),
    ("The Turing Test is associated with:", ["Human-like machine conversation", "Timetable creation", "Shortest routes only", "Screen size"], 0, "It tests whether machine responses resemble human responses."),
    ("CSP is useful for:", ["Exam scheduling", "Printing a photo", "Changing volume", "Renaming files"], 0, "Scheduling problems can be expressed as constraints."),
    ("Hill climbing is based on:", ["Improving neighboring states", "Expanding the oldest node", "Exploring every state at once", "Ignoring evaluations"], 0, "It repeatedly seeks a better neighboring state."),
    ("A navigation app estimates remaining route cost. This can use:", ["Heuristic search", "Turing Test", "Random guessing", "File compression"], 0, "Heuristics estimate progress toward a destination."),
    ("An online shop suggests products from customer history. This is:", ["AI recommendation", "Manual typing only", "Printing", "Static display"], 0, "Recommendation systems personalize suggestions."),
    ("A hospital system analyzes symptoms and test results. This is:", ["Medical decision support", "Game animation", "Word formatting", "Network cabling"], 0, "AI can help interpret clinical information."),
    ("A robot vacuum senses obstacles and changes direction. It uses:", ["Sensors and actuators", "Only a printer", "Only a monitor", "Only a keyboard"], 0, "Sensors detect obstacles; actuators control movement."),
    ("An email service flags suspicious phishing messages. This is:", ["AI-assisted fraud detection", "A physical actuator", "A search tree only", "Manual printing"], 0, "AI can classify suspicious message patterns."),
    ("Converting spoken words into text is called:", ["Speech recognition", "Hill climbing", "Scheduling", "Depth-first traversal"], 0, "Speech recognition converts audio into words."),
    ("A car detects a pedestrian and brakes. This shows an agent:", ["Perceiving and acting", "Working without input", "Only storing images", "Never changing actions"], 0, "It senses its surroundings and responds."),
    ("A factory system identifies defective products. This is:", ["Automated quality inspection", "Turing Test only", "Random search only", "Static environment only"], 0, "AI-based inspection can identify product defects."),
    ("A streaming service suggests films from viewing history to:", ["Personalize recommendations", "Find maze paths", "Move robot arms", "Schedule exams"], 0, "It uses user data to suggest relevant content."),
    ("A smart thermostat senses temperature and controls heating. It is:", ["An agent interacting with its environment", "A Turing examiner", "A search tree", "A CSP domain"], 0, "It senses conditions and acts to regulate temperature."),
    ("S connects to A and B; A connects to C; B connects to G. BFS finds which path to G?", ["S-A-C-G", "S-B-G", "S-C-G", "S-A-B-G"], 1, "S-B-G reaches G using two edges."),
    ("S connects to A and B; A connects to C; C connects to G. DFS explores A first. Which path can it find first?", ["S-B", "S-A-C-G", "S-B-G", "S only"], 1, "DFS follows the A branch deeply first."),
    ("Iterative deepening starts with depth limit 0. What is the next limit?", ["0", "1", "5", "Infinity"], 1, "The depth limit increases by one each iteration."),
    ("Greedy best-first search compares heuristic values A=3 and B=8. Which is preferred?", ["A", "B", "Both rejected", "Cannot compare"], 0, "It prefers the lower estimated remaining cost."),
    ("Hill climbing has current score 5 and neighbors 7, 4 and 6. Which best improving neighbor is selected?", ["4", "5", "7", "6"], 2, "Score 7 is the highest neighboring score and improves on 5.")
]


for i, (question, options, answer, explanation) in enumerate(QUESTIONS):
    option_pairs = list(enumerate(options))
    random.shuffle(option_pairs)

    shuffled_options = [option for original_index, option in option_pairs]

    shuffled_answer = next(
        position
        for position, (original_index, option) in enumerate(option_pairs)
        if original_index == answer
    )

    QUESTIONS[i] = (
        question,
        shuffled_options,
        shuffled_answer,
        explanation
    )


st.markdown("""
<div style="text-align:center; padding:18px 0 10px 0;">
    <h1 style="font-size:42px;">🧠 AI QUEST</h1>
    <p style="font-size:17px; color:#94a3b8;">
        Learn AI. Solve challenges. Earn XP.
    </p>
</div>
""", unsafe_allow_html=True)


if "xp" not in st.session_state:
    st.session_state.xp = 0

level = (st.session_state.xp // 50) + 1

st.markdown(f"""
<div style="
    background: linear-gradient(120deg, #172554, #312e81);
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #6366f1;
    margin: 12px 0;
">
    <div style="font-size:13px; color:#c7d2fe;">YOUR PLAYER LEVEL</div>
    <div style="font-size:28px; font-weight:800; color:white;">
        ⚡ Level {level}
    </div>
    <div style="color:#c7d2fe;">Earn 50 XP to reach the next level.</div>
</div>
""", unsafe_allow_html=True)

st.markdown("### ⭐ Your Progress")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("⭐ Total XP", st.session_state.xp)

with col2:
    st.metric("🎯 Questions", 50)

with col3:
    if st.session_state.xp >= 100:
        badge = "🏆 AI Expert"
    elif st.session_state.xp >= 50:
        badge = "🥈 AI Explorer"
    else:
        badge = "🌱 Beginner"
    st.metric("🎖️ Badge", badge)

st.markdown("## 🗺️ Choose Your Mission")

mission = st.selectbox(
    "Select a mission to begin",
    [
        "📘 Learn AI — Concepts and Agents",
        "🌳 Search Lab — BFS, DFS and Heuristics",
        "⏱️ Exam Mode — 10 Random Questions",
        "🏆 Final Boss — Full AI Challenge"
    ],
    key="ai_quest_mission"
)

st.markdown("---")

st.write("### Test your intelligence. Challenge your knowledge.")
st.write("DSC401-6 Artificial Intelligence | Units I & II")
st.write("50 questions • Random order • Instant feedback • Final score")

RESULT_FILE = Path("/content/ai_quiz_result.json")

if "quiz" not in st.session_state:
    st.session_state.quiz = []
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.finished = False

if "quiz_result" not in st.session_state:
    st.session_state.quiz_result = None
    if RESULT_FILE.exists():
        try:
            st.session_state.quiz_result = json.loads(RESULT_FILE.read_text())
        except Exception:
            st.session_state.quiz_result = None

if not st.session_state.quiz and st.session_state.quiz_result:
    st.title("🧠 AI QUEST")
    st.success("Your previous quiz result is saved.")
    st.metric("Final Score", f"{st.session_state.quiz_result['score']} / {st.session_state.quiz_result['total']}")
    st.metric("Percentage", f"{st.session_state.quiz_result['percentage']:.1f}%")
    if st.button("Start a New Quiz"):
        RESULT_FILE.unlink(missing_ok=True)
        st.session_state.quiz_result = None
        st.rerun()
    st.stop()

if not st.session_state.quiz:
    st.info("Test your AI knowledge with 50 questions.")
    if st.button("🚀 Start Quiz"):
        if st.session_state.get("ai_quest_mission", "").startswith("⏱️ Exam Mode"):
            st.session_state.quiz = random.sample(QUESTIONS, 10)
        else:
            st.session_state.quiz = random.sample(QUESTIONS, len(QUESTIONS))
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.finished = False
        st.rerun()

elif not st.session_state.finished:
    q = st.session_state.quiz[st.session_state.index]
    total = len(st.session_state.quiz)
    n = st.session_state.index + 1

    st.progress(st.session_state.index / total)
    st.caption(f"Question {n} of {total}  |  Score: {st.session_state.score}")
    st.subheader(q[0])

    selected = st.radio("Choose your answer:", q[1], key=f"answer_{n}")

    if not st.session_state.answered:
        if st.button("Submit Answer"):
            st.session_state.answered = True
            if q[1].index(selected) == q[2]:
                st.session_state.score += 1
                st.session_state.xp += 10
            st.rerun()
    else:
        if q[1].index(selected) == q[2]:
            st.success("Correct answer!")
        else:
            st.error(f"Correct answer: {q[1][q[2]]}")

        st.info(q[3])

        if st.button("Next Question" if n < total else "View Results"):
            st.session_state.index += 1
            st.session_state.answered = False
            if st.session_state.index >= total:
                st.session_state.finished = True
            st.rerun()

else:
    total = len(st.session_state.quiz)
    score = st.session_state.score
    percentage = score / total * 100
    result = {"score": score, "total": total, "percentage": percentage}
    RESULT_FILE.write_text(json.dumps(result))
    st.session_state.quiz_result = result

    st.balloons()
    st.header("🎉 Quiz Completed!")
    st.metric("Final Score", f"{score} / {total}")
    st.metric("Percentage", f"{percentage:.1f}%")

    if percentage >= 80:
        st.success("Excellent work!")
    elif percentage >= 60:
        st.success("Good job!")
    elif percentage >= 40:
        st.warning("Keep practising!")
    else:
        st.error("Review the concepts and try again.")

    if st.button("🔄 Play Again"):
        st.session_state.quiz = []
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.finished = False
        st.rerun()

st.divider()
st.caption("Interactive AI QUEST | Educational Project")

