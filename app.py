import streamlit as st
import time
from streamlit_autorefresh import st_autorefresh

# Oldal konfigurációja
st.set_page_config(page_title="Kvízjáték", page_icon="🧠", layout="centered")

# --- PRÉMIUM, EGYSÉGESÍTETT GOMB DESIGN (CSS) ---
st.markdown("""
    <style>
    /* Fő konténer szélessége és igazítása */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 0rem !important;
        max-width: 550px !important;
    }
    
    /* Cím */
    h1 {
        font-size: 26px !important;
        font-weight: 800 !important;
        color: #4ADE80 !important;
        margin-bottom: 15px !important;
    }
    
    /* Kérdés kártya (szürkéskék doboz) */
    .quiz-card {
        background-color: #1E293B;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 20px;
    }
    
    .question-text {
        font-size: 17px !important;
        font-weight: 600 !important;
        color: #F8FAFC !important;
        line-height: 1.4;
    }

    /* FIX: Kényszerítjük a Streamlit gombkonténereit, hogy töltsék ki a teljes szélességet (így középre kerülnek) */
    div[data-testid="stVerticalBlock"] > div.element-container {
        width: 100% !important;
    }

    /* --- ALAPÉRTELMEZETT VÁLASZ GOMBOK DESIGNJA (SECONDARY) --- */
    div.element-container button[kind="secondary"] {
        width: 100% !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        background-color: #1E293B !important;   /* Sötétkék háttér */
        color: #E2E8F0 !important;               /* Világos szövegszín */
        border: 1px solid #334155 !important;    /* Finom szürke szegély */
        padding: 14px !important;
        margin-bottom: 2px !important;
        cursor: pointer !important;
        text-align: center !important;           /* Középre igazított szöveg a gombon belül */
        display: block !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    /* Alap gombok hover állapota (Amikor ráviszed az egeret) */
    div.element-container button[kind="secondary"]:hover {
        border-color: #4ADE80 !important;        
        box-shadow: 0 0 12px rgba(74, 222, 128, 0.25) !important; 
        color: #4ADE80 !important;               
    }

    /* --- A KIJELÖLT GOMB DESIGNJA (PRIMARY) --- */
    div.element-container button[kind="primary"] {
        width: 100% !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        background-color: #1E293B !important;   /* Háttér sötétkék marad */
        color: #4ADE80 !important;               /* Szöveg fixen zöld */
        border: 2px solid #4ADE80 !important;    /* Szegély fixen világít zölden */
        box-shadow: 0 0 12px rgba(74, 222, 128, 0.35) !important; /* Fix neon ragyogás */
        padding: 14px !important;
        margin-bottom: 2px !important;
        text-align: center !important;           /* Középre igazított szöveg a gombon belül */
        display: block !important;
    }

    /* A Tovább és Újrakezdés gombok középre igazítása */
    div.action-btn button {
        text-align: center !important;
    }
    </style>
""", unsafe_allow_html=True)

# Kvízkérdések adatbázisa
QUESTIONS = [
    {
        "question": "Melyik évben jelent meg a Python programozási nyelv?",
        "options": ["1989", "1991", "1995", "2000"],
        "answer": "1991",
        "explanation": "Guido van Rossum 1989-ben kezdte el fejleszteni, de az első hivatalos verzió (0.9.0) 1991 februárjában megjelent."
    },
    {
        "question": "Mit jelent az Ubuntu szó afrikai nyelveken?",
        "options": ["Gyorsaság", "Szabadság", "Emberiesség mások iránt", "Nyílt forráskód"],
        "answer": "Emberiesség mások iránt",
        "explanation": "Az Ubuntu egy dél-afrikai humanista filozófia, amelynek jelentése: 'Vagyok, mert mi vagyunk', azaz emberiesség mások iránt."
    },
    {
        "question": "Melyik parancs frissíti a csomaglistát Ubuntu-n a terminálban?",
        "options": ["sudo apt upgrade", "sudo apt install", "sudo apt update", "sudo apt search"],
        "answer": "sudo apt update",
        "explanation": "A 'sudo apt update' letölti a legfrissebb csomaginformációkat a tárolókból. A tényleges frissítést az 'upgrade' végzi."
    }
]

# Session State inicializálás
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "user_choice" not in st.session_state:
    st.session_state.user_choice = None
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
if "time_over" not in st.session_state:
    st.session_state.time_over = False

st.title("🍏 Kvízjáték")

q_idx = st.session_state.current_question

if q_idx < len(QUESTIONS):
    current_q = QUESTIONS[q_idx]
    
    # --- IDŐZÍTŐ ---
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = max(0, 30 - int(elapsed_time))
    
    if not st.session_state.answered and remaining_time > 0:
        st_autorefresh(interval=1000, key=f"quiz_ref_{q_idx}")
    
    if remaining_time <= 0 and not st.session_state.answered:
        st.session_state.time_over = True
        st.session_state.answered = True
        st.session_state.user_choice = "LEJÁRT AZ IDŐ"
        st.rerun()

    # --- FEJLÉC (Időzítő teljesen a jobb szélen) ---
    hdr_col1, hdr_col2 = st.columns(2)
    with hdr_col1:
        st.write(f"**{q_idx + 1} / {len(QUESTIONS)} Kérdés**")
        st.progress(q_idx / len(QUESTIONS))
    
    with hdr_col2:
        max_offset = 213.6
        offset = max_offset - (remaining_time / 30) * max_offset if not st.session_state.answered else 0
        text_val = remaining_time if not st.session_state.answered else "⏱️"
        
        js_timer = f"""
        <div style="display: flex; justify-content: center; align-items: center; width: 100%; height: 80px;">
            <svg width="60" height="60" viewBox="0 0 80 80" style="overflow: visible;">
                <circle cx="40" cy="40" r="34" stroke="#334155" stroke-width="8" fill="none" />
                <circle cx="40" cy="40" r="34" stroke="#4ADE80" stroke-width="8" fill="none" 
                        stroke-dasharray="213.6" stroke-dashoffset="{offset}" transform="rotate(-90 40 40)" stroke-linecap="round" />
                <text x="40" y="48" text-anchor="middle" font-size="24" font-weight="800" fill="#4ADE80" font-family="sans-serif">{text_val}</text>
            </svg>
        </div>
        """
        st.components.v1.html(js_timer, height=80)
    
    st.write("") 

    # --- KÉRDÉS KÁRTYA ---
    st.markdown(f'<div class="quiz-card"><div class="question-text">{current_q["question"]}</div></div>', unsafe_allow_html=True)
    
    # --- VÁLASZOK MEGJELENÍTÉSE ---
    for idx, option in enumerate(current_q["options"]):
        is_selected = (st.session_state.user_choice == option)
        btn_kind = "primary" if is_selected else "secondary"
            
        if st.button(option, disabled=st.session_state.answered, key=f"btn_{q_idx}_{idx}", type=btn_kind):
            st.session_state.user_choice = option
            st.rerun()
            
    st.write("---")

    # Első lépés: Tovább gomb (Beküldés)
    if not st.session_state.answered:
        st.markdown('<div class="action-btn">', unsafe_allow_html=True)
        if st.button("Tovább ➡️", disabled=st.session_state.user_choice is None, key="submit_btn", type="secondary"):
            st.session_state.answered = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Kiértékelés utáni állapot
    if st.session_state.answered:
        if st.session_state.time_over:
            st.error("❌ Nem választottál időben! Lejárt a 30 másodperc.")
        elif st.session_state.user_choice == current_q["answer"]:
            st.success("🎉 Helyes válasz!")
            if f"scored_{q_idx}" not in st.session_state:
                st.session_state.score += 1
                st.session_state[f"scored_{q_idx}"] = True
        else:
            st.error(f"❌ Helytelen! A jó megoldás: **{current_q['answer']}**")
        
        st.info(f"💡 {current_q['explanation']}")
        
        # Második kattintás: ugrás a következő kérdésre
        st.markdown('<div class="action-btn">', unsafe_allow_html=True)
        if st.button("Következő kérdés ➡️", key="next_btn", type="secondary"):
            st.session_state.current_question += 1
            st.session_state.answered = False
            st.session_state.user_choice = None
            st.session_state.time_over = False
            st.session_state.start_time = time.time()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# Végeredmény
else:
    st.success("🏆 Gratulálok, sikeresen teljesítetted a kvízt!")
    st.balloons()
    
    final_score = st.session_state.score
    total_q = len(QUESTIONS)
    percentage = int((final_score / total_q) * 100)
    
    st.metric(label="Elért Pontszámod", value=f"{final_score} / {total_q}", delta=f"{percentage}% Siker")
    
    st.markdown('<div class="action-btn">', unsafe_allow_html=True)
    if st.button("Új játék indítása 🔄", key="restart_btn", type="secondary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
