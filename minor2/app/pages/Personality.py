import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
try:
    from app.main import predict_cluster_and_careers
except ImportError:
    def predict_cluster_and_careers(O, C, E, A, N, numerical, spatial, perceptual, abstract, verbal):
        cluster = 3  
        careers = ["Software Developer", "Data Analyst", "UX Designer"]
        return cluster, careers



hide_sidebar = """
    <style>
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        div[data-testid="stSidebarNav"] {
            display: none !important;
        }

    </style>
"""
st.markdown(hide_sidebar, unsafe_allow_html=True)

questions = {
    1: ("Am the life of the party.", False),
    2: ("Feel little concern for others.", True),
    3: ("Am always prepared.", False),
    4: ("Get stressed out easily.", True),
    5: ("Have a rich vocabulary.", False),
    6: ("Don't talk a lot.", True),
    7: ("Am interested in people.", False),
    8: ("Leave my belongings around.", True),
    9: ("Am relaxed most of the time.", False),
    10: ("Have difficulty understanding abstract ideas.", True),
    11: ("Feel comfortable around people.", False),
    12: ("Insult people.", True),
    13: ("Pay attention to details.", False),
    14: ("Worry about things.", True),
    15: ("Have a vivid imagination.", False),
    16: ("Keep in the background.", True),
    17: ("Sympathize with others' feelings.", False),
    18: ("Make a mess of things.", True),
    19: ("Seldom feel blue.", False),
    20: ("Am not interested in abstract ideas.", True),
    21: ("Start conversations.", False),
    22: ("Am not interested in other people's problems.", True),
    23: ("Get chores done right away.", False),
    24: ("Am easily disturbed.", True),
    25: ("Have excellent ideas.", False),
    26: ("Have little to say.", True),
    27: ("Have a soft heart.", False),
    28: ("Often forget to put things back in their proper place.", True),
    29: ("Get upset easily.", True),
    30: ("Do not have a good imagination.", True),
    31: ("Talk to a lot of different people at parties.", False),
    32: ("Am not really interested in others.", True),
    33: ("Like order.", False),
    34: ("Change my mood a lot.", True),
    35: ("Am quick to understand things.", False),
    36: ("Don't like to draw attention to myself.", True),
    37: ("Take time out for others.", False),
    38: ("Shirk my duties.", True),
    39: ("Have frequent mood swings.", True),
    40: ("Use difficult words.", False),
    41: ("Don't mind being the center of attention.", False),
    42: ("Feel others' emotions.", False),
    43: ("Follow a schedule.", False),
    44: ("Get irritated easily.", True),
    45: ("Spend time reflecting on things.", False),
    46: ("Am quiet around strangers.", True),
    47: ("Make people feel at ease.", False),
    48: ("Am exacting in my work.", False),
    49: ("Often feel blue.", True),
    50: ("Am full of ideas.", False)
}

traits = {
    "E": {"base": 20, "items": [+1, -6, +11, -16, +21, -26, +31, -36, +41, -46]},
    "A": {"base": 14, "items": [-2, +7, -12, +17, -22, +27, -32, +37, +42, +47]},
    "C": {"base": 14, "items": [+3, -8, +13, -18, +23, -28, +33, -38, +43, +48]},
    "N": {"base": 38, "items": [-4, +9, -14, +19, -24, -29, -34, -39, -44, -49]},
    "O": {"base": 8, "items": [+5, -10, +15, -20, +25, -30, +35, +40, +45, +50]},
}

def main():
 
    st.title("🌟 Personality Assessment")
    if not st.session_state.get('aptitude_scores'):
        
        st.info("Run the aptitude test application first, complete all test sections, and then return to this application.")
        return
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Questions 1-10", "Questions 11-20", "Questions 21-30", "Questions 31-40", "Questions 41-50"])
    
    if 'personality_responses' not in st.session_state:
        st.session_state.personality_responses = {i: 3 for i in range(1, 51)} 
    
    with tab1:
        for i in range(1, 11):
            question, _ = questions[i]
            st.session_state.personality_responses[i] = st.slider(
                f"{i}. {question}", 
                1, 5, 
                st.session_state.personality_responses[i], 
                key=f"q_{i}"
            )
    
    with tab2:
        for i in range(11, 21):
            question, _ = questions[i]
            st.session_state.personality_responses[i] = st.slider(
                f"{i}. {question}", 
                1, 5, 
                st.session_state.personality_responses[i], 
                key=f"q_{i}"
            )
    
    with tab3:
        for i in range(21, 31):
            question, _ = questions[i]
            st.session_state.personality_responses[i] = st.slider(
                f"{i}. {question}", 
                1, 5, 
                st.session_state.personality_responses[i], 
                key=f"q_{i}"
            )
    
    with tab4:
        for i in range(31, 41):
            question, _ = questions[i]
            st.session_state.personality_responses[i] = st.slider(
                f"{i}. {question}", 
                1, 5, 
                st.session_state.personality_responses[i], 
                key=f"q_{i}"
            )
    
    with tab5:
        for i in range(41, 51):
            question, _ = questions[i]
            st.session_state.personality_responses[i] = st.slider(
                f"{i}. {question}", 
                1, 5, 
                st.session_state.personality_responses[i], 
                key=f"q_{i}"
            )
        
        if st.button("🔍 Submit and Continue"):
            results = {}
            for trait, data in traits.items():
                score = data["base"]
                for op in data["items"]:
                    index = abs(op)
                    value = st.session_state.personality_responses[index]
                    score += value if op > 0 else (6 - value)
                results[trait] = score

            O_score_normal = round(results["O"] / 4, 2)
            C_score_normal = round(results["C"] / 4, 2)
            E_score_normal = round(results["E"] / 4, 2)
            A_score_normal = round(results["A"] / 4, 2)
            N_score_normal = round(results["N"] / 4, 2)

            st.session_state.O_score = O_score_normal
            st.session_state.C_score = C_score_normal
            st.session_state.E_score = E_score_normal
            st.session_state.A_score = A_score_normal
            st.session_state.N_score = N_score_normal

            st.switch_page("pages/Career_Final.py")

            O_score = st.session_state.get('O_score', None)
            C_score = st.session_state.get('C_score', None)
            E_score = st.session_state.get('E_score', None)
            A_score = st.session_state.get('A_score', None)
            N_score = st.session_state.get('N_score', None)

            has_results = 'personality_results' in st.session_state
            
if __name__ == "__main__":
    main()