import streamlit as st
import datetime
import random

# --- CONFIGURATION & THEME ---
st.set_page_config(
    page_title="Unipath Assistant Chat",
    page_icon="🤖",
    layout="centered"
)

# Custom Styling for Chat Interface
st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .main { background-color: #f8fafc; }
    </style>
    """, unsafe_allow_html=True)

# --- KNOWLEDGE BASE (No Raw LLM Dependency) ---
PROGRAMS = [
    {"name": "Computer Science", "uni": "Global Institute of Technology", "deadline": "March 15", "req": "GPA 3.8, Math, TOEFL"},
    {"name": "Business Administration", "uni": "Heritage Institute", "deadline": "Feb 16", "req": "GPA 3.5, Leadership"},
    {"name": "Graphic Design", "uni": "Hyderabad University", "deadline": "Feb 20", "req": "Portfolio of 12 works"},
    {"name": "Mechanical Engineering", "uni": "BITS Pilani", "deadline": "Nov 30", "req": "Physics, Advanced Math"}
]

UNIVERSITIES = [
    {"name": "Global Institute of Technology", "location": "International", "specialty": "STEM & AI"},
    {"name": "Heritage Institute", "location": "Regional", "specialty": "Business & Management"},
    {"name": "Hyderabad University", "location": "India", "specialty": "Arts & Design"},
    {"name": "BITS Pilani", "location": "India", "specialty": "Engineering & Sciences"},
    {"name": "Silicon Valley Tech", "location": "USA", "specialty": "Computer Science"},
    {"name": "London School of Economics", "location": "UK", "specialty": "Social Sciences"}
]

# --- CHAT LOGIC ENGINE ---
def get_ai_response(user_input):
    user_input = user_input.lower()
    
    # 1. Greetings
    if any(word in user_input for word in ["hello", "hi", "hey"]):
        return "Hello! I'm your Unipath Assistant. Ask me about universities, deadlines, or admission requirements!"

    # 2. University Suggestions Logic
    if any(word in user_input for word in ["suggest", "recommend", "university names", "list of universities"]):
        if "stem" in user_input or "tech" in user_input or "computer" in user_input:
            match = [u["name"] for u in UNIVERSITIES if "STEM" in u["specialty"] or "Computer" in u["specialty"]]
            return f"For Tech/STEM, I highly suggest: **{', '.join(match)}**."
        
        if "india" in user_input:
            match = [u["name"] for u in UNIVERSITIES if u["location"] == "India"]
            return f"Based on your location preference, I suggest: **{', '.join(match)}**."
        
        # General Suggestion
        all_unis = [u["name"] for u in UNIVERSITIES]
        return f"I can suggest several top-tier universities such as: **{', '.join(random.sample(all_unis, 3))}**. Would you like to know more about a specific one?"

    # 3. Search for Programs
    for prog in PROGRAMS:
        if prog["name"].lower() in user_input or prog["uni"].lower() in user_input:
            return f"I found information on **{prog['name']}** at **{prog['uni']}**. The deadline is **{prog['deadline']}** and the requirements include: {prog['req']}."

    # 4. Specific Keywords
    if "deadline" in user_input:
        deadlines = ", ".join([f"{p['name']} ({p['deadline']})" for p in PROGRAMS[:3]])
        return f"Upcoming deadlines include: {deadlines}. Which one would you like more details on?"
    
    if "requirement" in user_input or "criteria" in user_input:
        return "Most programs require a minimum GPA of 3.5, academic transcripts, and a personal statement. Which specific major are you interested in?"

    if "thank" in user_input:
        return "You're very welcome! Good luck with your applications. Anything else?"

    # 5. Fallback
    return "I'm not sure I understand. You can ask me things like 'Suggest some universities for STEM' or 'What are the requirements for Computer Science?'"

# --- UI LAYOUT ---
st.title("🎓 Unipath Assistant AI")

# --- SIDEBAR PROGRESS ---
with st.sidebar:
    st.header("📋 Your Progress")
    if 'checklist' not in st.session_state:
        st.session_state.checklist = {"Transcripts": False, "Essay": False, "Tests": False}
    
    for key in st.session_state.checklist:
        st.session_state.checklist[key] = st.checkbox(key, value=st.session_state.checklist[key])
    
    done = sum(st.session_state.checklist.values())
    st.progress(done / len(st.session_state.checklist))
    st.caption(f"{done} of {len(st.session_state.checklist)} milestones reached.")

# --- CHAT INTERFACE ---
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome! I am your AI Admission Bot. How can I help you with your university journey today?"}
    ]

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask about programs, deadlines, or requirements..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate and display assistant response
    response = get_ai_response(prompt)
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

# --- FOOTER ---
st.caption("---")
st.caption("© 2026 Unipath Assistant")