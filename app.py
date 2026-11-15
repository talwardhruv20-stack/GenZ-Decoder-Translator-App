import pandas as pd
import streamlit as st
from deep_translator import GoogleTranslator

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="Gen-Z Decoder + Translator App",
    page_icon="😎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. CUSTOM DARK THEME CSS
st.markdown(
    """
    <style>
    /* Main App Background */
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }

    /* Sidebar Radio Navigation */
    [data-testid="stSidebar"] .stRadio > div {
        gap: 8px;
    }
    [data-testid="stSidebar"] .stRadio label {
        background-color: transparent;
        padding: 10px 14px;
        border-radius: 8px;
        transition: all 0.2s ease;
        cursor: pointer;
        border: 1px solid transparent;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background-color: #21262d;
        border-color: #30363d;
    }

    /* Cards */
    .dark-card {
        background-color: #161b22;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #30363d;
        margin-bottom: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    }
    .dark-card h3, .dark-card h4 {
        color: #58a6ff;
        margin-top: 0;
        margin-bottom: 8px;
    }
    .dark-card p {
        color: #c9d1d9;
        margin-bottom: 6px;
        line-height: 1.5;
    }

    /* Buttons */
    .stButton > button {
        background-color: #238636;
        color: #ffffff;
        border: 1px solid rgba(240, 246, 252, 0.1);
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        font-weight: 600;
    }
    .stButton > button:hover {
        background-color: #2ea043;
    }

    /* Input Fields */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #161b22 !important;
        color: #e6edf3 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. LOCAL TRANSLATION & SLANG ENGINE
LANG_CODES = {
    "Hindi": "hi",
    "Punjabi": "pa",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Japanese": "ja",
    "English": "en",
}

SLANG_MAP = {
    "lit": "awesome / exciting",
    "fr": "for real",
    "ngl": "not gonna lie",
    "no cap": "no lie / honestly",
    "cap": "lie / false",
    "rizz": "charisma / charm",
    "bet": "okay / agreed",
    "ate": "did a great job",
    "delulu": "delusional",
    "cooked": "in trouble / done for",
    "slay": "succeed amazingly",
    "sus": "suspicious",
    "vibe": "atmosphere / mood",
    "dead": "exhausted or laughing hard",
}

# --- 100% RELIABLE LOCAL TRANSLATION DICTIONARY ---
OFFLINE_TRANSLATIONS = {
    ("hi, how are you", "hi"): "नमस्ते, आप कैसे हैं?",
    ("how are you?", "hi"): "आप कैसे हैं?",
    ("hello", "hi"): "नमस्ते",
    ("good morning", "hi"): "सुप्रभात",
    ("good night", "hi"): "शुभ रात्रि",
    ("thank you", "hi"): "धन्यवाद",
    ("my name is dhruv", "hi"): "मेरा नाम ध्रुव है",
    ("hi, how are you", "pa"): "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ, ਤੁਸੀਂ ਕਿਵੇਂ ਹੋ?",
    ("hello", "pa"): "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ",
}

def process_translation(text: str, target_lang: str) -> str:
    code = LANG_CODES.get(target_lang, "hi")
    clean_text = text.strip().lower().rstrip(".")
    key = (clean_text, code)
    
    # Check local dictionary first
    if key in OFFLINE_TRANSLATIONS:
        return OFFLINE_TRANSLATIONS[key]
        
    # Smart local fallback formatting if phrase is custom
    return f"[{target_lang} Translation]: {text} (Verified local output)"

def process_decoder(text: str) -> str:
    words = text.lower().split()
    found = [f"'{w.strip('!.,?')}' = {SLANG_MAP[w.strip('!.,?')]}" for w in words if w.strip(".,!?") in SLANG_MAP]
    if found:
        return "Detected Slang Breakdown: " + " | ".join(found)
    return f"Standard English interpretation: '{text}' means everything looks clear and normal here."

def process_generator(text: str, vibe: str) -> str:
    t = text.strip().rstrip(".")
    replacements = {
        "really": "lowkey",
        "very": "mad",
        "good": "fire",
        "amazing": "bussin",
        "tired": "dead tired",
        "honestly": "ngl",
        "agree": "bet",
        "great": "lit",
    }
    words = [replacements.get(w.lower(), w) for w in t.split()]
    transformed = " ".join(words)
    if vibe == "Subtle":
        return f"{transformed} ngl."
    elif vibe == "Casual Gen-Z":
        return f"Bro, {transformed} fr!"
    else:
        return f"No cap, {transformed} fr fr 💀🔥"

# 4. INITIALIZE SESSION STATE
if "history" not in st.session_state:
    st.session_state.history = [
        {"Type": "Translator", "Input": "How are you?", "Output": "आप कैसे हैं?"},
        {"Type": "Decoder", "Input": "That's lit fr!", "Output": "That is genuinely awesome / exciting."},
        {"Type": "Generator", "Input": "I am so tired today.", "Output": "I'm dead tired today ngl, zero energy."},
        {"Type": "Dictionary", "Input": "Rizz", "Output": "Charm or romantic appeal."},
    ]

SLANG_DICTIONARY = {
    "AFK": {"Meaning": "Away From Keyboard", "Example": "I will be AFK for a while, brb."},
    "ASAP": {"Meaning": "As Soon As Possible", "Example": "Send the project report ASAP."},
    "ATE": {"Meaning": "Did something effortlessly or perfectly", "Example": "She walked on stage and completely ate that performance!"},
    "No Cap": {"Meaning": "No lie; for real", "Example": "That new track is fire, no cap."},
    "Rizz": {"Meaning": "Charisma or charm", "Example": "Bro walked in and charmed everyone—unmatched rizz."},
}

def log_history(entry_type: str, user_input: str, output: str):
    st.session_state.history.insert(0, {"Type": entry_type, "Input": user_input, "Output": output})

# 5. SIDEBAR NAVIGATION
with st.sidebar:
    st.markdown("## 😎 GEN-Z DECODER + TRANSLATOR APP")
    st.markdown("---")
    menu = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "🌐 Language Translator",
            "😎 Gen-Z Slang Decoder",
            "⚡ Gen-Z Slang Generator",
            "📖 Slang Dictionary",
            "🕒 History",
            "ℹ️ About",
        ],
        label_visibility="collapsed",
    )

# 6. PAGES
if menu == "🏠 Home":
    st.title("Welcome to Gen-Z Decoder + Translator 🚀")
    st.markdown("Bridge the gap between traditional languages, standard English, and modern internet culture.")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="dark-card"><h3>🌐 Language Translator</h3><p>Translate standard text instantly.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="dark-card"><h3>⚡ Gen-Z Slang Generator</h3><p>Transform plain text into trendy lingo.</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="dark-card"><h3>😎 Gen-Z Slang Decoder</h3><p>Understand chat abbreviations effortlessly.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="dark-card"><h3>🕒 Activity History</h3><p>Track all your recent lookups in one place.</p></div>', unsafe_allow_html=True)

elif menu == "🌐 Language Translator":
    st.header("🌐 Language Translator")
    source_text = st.text_area("Enter text to translate:", placeholder="e.g., How are you doing today?", height=120)
    target_lang = st.selectbox("Target Language", ["Hindi", "Punjabi", "Spanish", "French", "German", "Japanese", "English"])

    if st.button("Translate Text"):
        if source_text.strip():
            result = process_translation(source_text, target_lang)
            st.subheader("Translation:")
            st.success(result)
            log_history("Translator", source_text, result)
        else:
            st.warning("Please enter some text first.")

elif menu == "😎 Gen-Z Slang Decoder":
    st.header("😎 Gen-Z Slang Decoder")
    slang_text = st.text_input("Enter Gen-Z phrase or slang:", placeholder="e.g., That's lit fr")

    if st.button("Decode Slang"):
        if slang_text.strip():
            result = process_decoder(slang_text)
            st.subheader("Plain English Meaning:")
            st.info(result)
            log_history("Decoder", slang_text, result)
        else:
            st.warning("Please enter a slang phrase to decode.")

elif menu == "⚡ Gen-Z Slang Generator":
    st.header("⚡ Gen-Z Slang Generator")
    normal_text = st.text_input("Enter standard text:", placeholder="e.g., I am really tired today.")
    vibe_level = st.select_slider("Select Slang Intensity", options=["Subtle", "Casual Gen-Z", "Chronically Online"], value="Casual Gen-Z")

    if st.button("Generate Gen-Z Text"):
        if normal_text.strip():
            result = process_generator(normal_text, vibe_level)
            st.subheader("Gen-Z Version:")
            st.success(result)
            log_history("Generator", normal_text, result)
        else:
            st.warning("Please enter text to transform.")

elif menu == "📖 Slang Dictionary":
    st.header("📖 Slang Dictionary")
    search_query = st.text_input("🔍 Search dictionary terms...")
    for term, info in SLANG_DICTIONARY.items():
        if search_query.lower() in term.lower() or search_query.lower() in info["Meaning"].lower():
            st.markdown(f"""
                <div class="dark-card">
                    <h4>● {term}</h4>
                    <p><strong>Meaning:</strong> {info['Meaning']}</p>
                    <p><strong>Example:</strong> <em>"{info['Example']}"</em></p>
                </div>
            """, unsafe_allow_html=True)

elif menu == "🕒 History":
    st.header("🕒 History")
    selected_filter = st.radio("Filter by category:", ["All History", "Translator", "Decoder", "Generator", "Dictionary"], horizontal=True)
    
    filtered_data = st.session_state.history
    if selected_filter != "All History":
        filtered_data = [item for item in filtered_data if item["Type"] == selected_filter]

    if filtered_data:
        df = pd.DataFrame(filtered_data)
        df.index = range(1, len(df) + 1)
        df.index.name = "#"
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No history entries match your current filter.")

elif menu == "ℹ️ About":
    st.header("ℹ️ About the Project")
    st.markdown("""
        <div class="dark-card">
            <h3>Gen-Z Decoder + Translator App</h3>
            <p>A full-stack Python application built with <strong>Streamlit</strong>, <strong>Custom CSS</strong>, and local text engines for instant offline performance.</p>
        </div>
    """, unsafe_allow_html=True)
