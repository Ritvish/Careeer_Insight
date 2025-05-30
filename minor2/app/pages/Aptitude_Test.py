import streamlit as st
import os
import random
from PIL import Image
import pandas as pd

st.set_page_config(page_title="Aptitude Test", layout="centered")
BASE_DIR = "../../Screenshots"

NUM_QUESTIONS_PER_SECTION = 5
ANSWER_KEY_DF = pd.read_csv('../../answer_key.csv')
ANSWER_KEY = {
    (row['section'], row['image_name']): row['correct_answer']
    for _, row in ANSWER_KEY_DF.iterrows()
}

def set_custom_styles():
    st.markdown("""
    <style>
    .test-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 60vh;
        gap: 20px;
    }
    .test-button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 15px 40px;
        text-align: center;
        font-size: 20px;
        border-radius: 12px;
        cursor: pointer;
        transition: background-color 0.3s, transform 0.2s;
        width: 300px;
    }
    .test-button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .back-button {
        background-color: #f44336;
        color: white;
        padding: 8px 20px;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        margin-top: 20px;
    }
    .back-button:hover {
        background-color: #d32f2f;
    }
    </style>
    """, unsafe_allow_html=True)



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

def show_title():
    st.markdown("""
    <h1 style='text-align: center; font-size: 55px; color: #4CAF50;'>
        📝 Aptitude Test
    </h1>
    <h3 style='text-align: center; color: gray;'>
        Select your test below
    </h3>
    """, unsafe_allow_html=True)

def go_to_page(page):
    st.session_state.page = page

def get_random_questions(section, num_questions):
    section_key = f"{section}_questions"
    if section_key not in st.session_state:
        section_path = os.path.join(BASE_DIR, section)
        images = [f for f in os.listdir(section_path) if f.endswith(('.png', '.jpg'))]
        selected_images = random.sample(images, min(num_questions, len(images)))
        st.session_state[section_key] = selected_images
    return st.session_state[section_key]

def home_page():
    show_title()
    tests = ['Abstract', 'Numerical', 'Perceptual', 'Spatial', 'Verbal']
    col1, col2, col3 = st.columns([1, 2, 1])

    all_tests_completed = all(st.session_state.get(f"{test}_submitted", False) for test in tests)

    with col2:
        for test in tests:
            submission_key = f"{test}_submitted"
            is_submitted = st.session_state.get(submission_key, False)
            status = " ✅" if is_submitted else ""
            if st.button(f"{test} Reasoning{status}", key=f"btn_{test}", use_container_width=True):
                st.session_state.page = test
                st.session_state.questions = get_random_questions(test, NUM_QUESTIONS_PER_SECTION)
                if 'answers' not in st.session_state:
                    st.session_state.answers = {}

        if st.button("View Final Dashboard", key="view_dashboard", disabled=not all_tests_completed, use_container_width=True):
            st.session_state.page = "dashboard"

        if st.button("Proceed to Personality Test", key="to_personality", disabled=not all_tests_completed, use_container_width=True):
            st.session_state.aptitude_tests_completed = True
            st.switch_page("pages/Personality.py")
            st.stop()

def test_page(test_section):
    st.markdown(f"<h2 style='text-align: center; color: #4CAF50;'>{test_section} Reasoning Test</h2>", unsafe_allow_html=True)

    questions = st.session_state.get('questions', [])
    submission_key = f"{test_section}_submitted"
    if submission_key not in st.session_state:
        st.session_state[submission_key] = False

    if test_section == 'Verbal':
        options = ['A', 'B', 'C', 'D', 'E']
    else:
        options = ['A', 'B', 'C', 'D']

    is_submitted = st.session_state[submission_key]
    if is_submitted:
        st.info(f"You have already submitted this {test_section} test. Your answers are locked.")

    for i, image_name in enumerate(questions, start=1):
        st.subheader(f"Q{i}")
        img_path = os.path.join(BASE_DIR, test_section, image_name)
        image = Image.open(img_path)
        st.image(image, use_container_width=True)

        q_tuple = (test_section, image_name)
        prev_answer = st.session_state.answers.get(q_tuple, None)
        selected_index = options.index(prev_answer) if prev_answer in options else -1

        answer_input = st.radio(
            f"Your answer for Q{i}:",
            options=options,
            key=f"radio_{test_section}_{i}_{image_name}",
            index=selected_index if selected_index >= 0 else None,
            disabled=is_submitted
        )

        if answer_input and not is_submitted:
            st.session_state.answers[q_tuple] = answer_input

    if not is_submitted:
        if st.button("Submit Answers"):
            score = 0
            total = len(questions)
            st.session_state[submission_key] = True
            st.write("### Your Responses:")
            for i, image_name in enumerate(questions, start=1):
                q_tuple = (test_section, image_name)
                user_ans = st.session_state.answers.get(q_tuple, None)
                correct_ans = ANSWER_KEY.get(q_tuple, None)
                result = "Correct" if user_ans == correct_ans else "Incorrect"
                st.write(f"Q{i}: Your answer = {user_ans} → {result}")
                if user_ans == correct_ans:
                    score += 1

            final_score = round((score / total) * 10, 2)
            if 'aptitude_scores' not in st.session_state:
                st.session_state.aptitude_scores = {}
            st.session_state.aptitude_scores[test_section] = final_score
            st.success(f"Your final score (out of 10): {final_score}")
            st.rerun()
    else:
        score = 0
        total = len(questions)
        st.write("### Your Responses:")
        for i, image_name in enumerate(questions, start=1):
            q_tuple = (test_section, image_name)
            user_ans = st.session_state.answers.get(q_tuple, None)
            correct_ans = ANSWER_KEY.get(q_tuple, None)
            result = "Correct" if user_ans == correct_ans else "Incorrect"
            st.write(f"Q{i}: Your answer = {user_ans} → {result}")
            if user_ans == correct_ans:
                score += 1

        final_score = round((score / total) * 10, 2)
        st.success(f"Your final score (out of 10): {final_score}")

    if st.button("Back to Home", key=f"back_{test_section}"):
        go_to_page('home')

def dashboard_page():
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Final Results Dashboard</h1>", unsafe_allow_html=True)
    tests = ['Abstract', 'Numerical', 'Perceptual', 'Spatial', 'Verbal']
    if 'aptitude_scores' not in st.session_state:
        st.session_state.aptitude_scores = {}

    scores = []
    for test_section in tests:
        section_key = f"{test_section}_questions"
        if section_key in st.session_state:
            questions = st.session_state[section_key]
            total = len(questions)
            score = 0
            for image_name in questions:
                q_tuple = (test_section, image_name)
                user_ans = st.session_state.answers.get(q_tuple, None)
                correct_ans = ANSWER_KEY.get(q_tuple, None)
                if user_ans == correct_ans:
                    score += 1
            percentage = round((score / total) * 100, 1)
            final_score = round((score / total) * 10, 2)
            st.session_state.aptitude_scores[test_section] = final_score
            scores.append({
                "Test Section": test_section,
                "Score": f"{score}/{total}",
                "Percentage": f"{percentage}%",
                "Final Score (out of 10)": final_score
            })

    df = pd.DataFrame(scores)
    st.table(df)

    if scores:
        overall_score = round(sum(item["Final Score (out of 10)"] for item in scores) / len(scores), 2)
        st.markdown(f"### Overall Performance: {overall_score}/10")

        chart_data = pd.DataFrame({
            'Test Section': [item["Test Section"] for item in scores],
            'Score': [item["Final Score (out of 10)"] for item in scores]
        })
        st.markdown("### Performance by Section")
        st.bar_chart(chart_data.set_index('Test Section'))

    if st.button("Proceed to Personality Test", key="proceed_to_personality"):
        st.session_state.aptitude_tests_completed = True
        st.switch_page("pages/Personality.py")
        st.stop()

    if st.button("Back to Home", key="back_dashboard"):
        go_to_page('home')

def main():
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    if 'answers' not in st.session_state:
        st.session_state.answers = {}

    set_custom_styles()

    if st.session_state.page == 'home':
        home_page()
    elif st.session_state.page in ['Abstract', 'Numerical', 'Perceptual', 'Spatial', 'Verbal']:
        test_page(st.session_state.page)
    elif st.session_state.page == 'dashboard':
        dashboard_page()

if __name__ == "__main__":
    main()
