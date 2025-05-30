import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

knn_data = pd.read_csv('../knn_data.csv')
temp = pd.read_csv('../temp.csv')
temp = temp.drop(columns='Cluster_4')

def predict_cluster_and_careers(O_score, C_score, E_score, A_score, N_score,
                                Numerical_Aptitude, Spatial_Aptitude,
                                Perceptual_Aptitude, Abstract_Reasoning,
                                Verbal_Reasoning):
    new_input = pd.Series({
        'O_score': O_score,
        'C_score': C_score,
        'E_score': E_score,
        'A_score': A_score,
        'N_score': N_score,
        'Numerical Aptitude': Numerical_Aptitude,
        'Spatial Aptitude': Spatial_Aptitude,
        'Perceptual Aptitude': Perceptual_Aptitude,
        'Abstract Reasoning': Abstract_Reasoning,
        'Verbal Reasoning': Verbal_Reasoning
    })

    input_vector = new_input.values.reshape(1, -1)
    centroid_vectors = temp.values

    similarities = cosine_similarity(input_vector, centroid_vectors)
    cluster = int(np.argmax(similarities))

    careers = knn_data[knn_data['Cluster_4'] == cluster]['Career'].unique()
    #print(f"Predicted Cluster: {cluster}")
    print("Recommended Careers:", careers)
    
    return cluster, careers
# main.py

# import pandas as pd
# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity

# # Load datasets
# knn_data = pd.read_csv('../knn_data.csv')
# temp = pd.read_csv('../temp.csv')
# temp = temp.drop(columns='Cluster_4')

# # Define the prediction function
# def predict_cluster_and_careers(O_score, C_score, E_score, A_score, N_score,
#                                 Numerical_Aptitude, Spatial_Aptitude,
#                                 Perceptual_Aptitude, Abstract_Reasoning,
#                                 Verbal_Reasoning):
#     new_input = pd.Series({
#         'O_score': O_score,
#         'C_score': C_score,
#         'E_score': E_score,
#         'A_score': A_score,
#         'N_score': N_score,
#         'Numerical Aptitude': Numerical_Aptitude,
#         'Spatial Aptitude': Spatial_Aptitude,
#         'Perceptual Aptitude': Perceptual_Aptitude,
#         'Abstract Reasoning': Abstract_Reasoning,
#         'Verbal Reasoning': Verbal_Reasoning
#     })

#     input_vector = new_input.values.reshape(1, -1)
#     centroid_vectors = temp.values

#     similarities = cosine_similarity(input_vector, centroid_vectors)
#     cluster = int(np.argmax(similarities))

#     careers = knn_data[knn_data['Cluster_4'] == cluster]['Career'].unique()
    
#     return cluster, careers

# # Call the function with sample inputs and print results
# if __name__ == "__main__":
#     cluster, careers = predict_cluster_and_careers(
#         O_score=30,
#         C_score=28,
#         E_score=25,
#         A_score=27,
#         N_score=29,
#         Numerical_Aptitude=80,
#         Spatial_Aptitude=75,
#         Perceptual_Aptitude=85,
#         Abstract_Reasoning=78,
#         Verbal_Reasoning=82
#     )

#     print(f"Predicted Cluster: {cluster}")
#     print("Recommended Careers:")
#     for career in careers:
#         print(f"- {career}")

