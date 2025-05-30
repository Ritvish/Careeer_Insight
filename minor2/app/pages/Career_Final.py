import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util

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


@st.cache_resource
def load_model_and_data():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    knn_data = pd.read_csv('../knn_data.csv')
    temp = pd.read_csv('../temp.csv').drop(columns='Cluster_4')
    return model, knn_data, temp

model, knn_data, temp = load_model_and_data()

def predict_cluster_and_careers(O, C, E, A, N, num, spa, perc, absr, verb):
    input_vector = np.array([O, C, E, A, N, num, spa, perc, absr, verb]).reshape(1, -1)
    similarities = cosine_similarity(input_vector, temp.values)
    cluster = int(np.argmax(similarities))
    careers = knn_data[knn_data['Cluster_4'] == cluster]['Career'].unique().tolist()
    return cluster, careers

def suggest_careers(user_intro, selected_cluster_name, professions, top_n=3):
    user_embedding = model.encode(user_intro, convert_to_tensor=True)
    prof_embeddings = model.encode(professions, convert_to_tensor=True)
    similarities = util.cos_sim(user_embedding, prof_embeddings)[0]
    top_results = similarities.argsort(descending=True)[:top_n]
    return [(professions[i], float(similarities[i])) for i in top_results]


st.title("🎯 Career Recommendations")

required_keys = ['O_score', 'C_score', 'E_score', 'A_score', 'N_score', 'aptitude_scores']
if not all(k in st.session_state for k in required_keys):
    st.error("Required data missing. Please complete the personality and aptitude tests first.")
    st.stop()

user_intro = st.text_area("✍️ Briefly describe your interests, hobbies, or achievements:")

if st.button("Get Career Suggestions"):

    scores = st.session_state
    apt = scores.aptitude_scores

    cluster_id, careers = predict_cluster_and_careers(
        scores.O_score, scores.C_score, scores.E_score, scores.A_score, scores.N_score,
        apt.get('Numerical', 0), apt.get('Spatial', 0),
        apt.get('Perceptual', 0), apt.get('Abstract', 0), apt.get('Verbal', 0)
    )

    if not user_intro.strip():
        st.warning("Please enter your interests or achievements.")
    else:
        cluster_label = f"Cluster_4_{cluster_id}"
        suggestions = suggest_careers(user_intro, cluster_label, careers)

        st.subheader(f"🧠 Predicted Cluster: {cluster_label}")
        st.markdown("### 💡 Recommended Careers Based on Your Interests:")
        for career, score in suggestions:
            st.markdown(f"- {career} ")
