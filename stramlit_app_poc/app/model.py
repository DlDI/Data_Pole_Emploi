import numpy as np
import scipy
from sklearn.metrics.pairwise import cosine_similarity


def calculate_average_word2vec_optimized(token_lists, model):
    num_features = model.vector_size
    feature_vecs = np.zeros((len(token_lists), num_features), dtype="float32")
    for idx, tokens in enumerate(token_lists):
        valid_tokens = [token for token in tokens if token in model.wv.key_to_index]
        if valid_tokens:
            model_vocabs = np.array([model.wv[token] for token in valid_tokens])
            feature_vecs[idx] = np.mean(model_vocabs, axis=0)
    return feature_vecs


def debug_vector_sizes(vec1, vec2):
    if len(vec1) != len(vec2):
        # Adjust size if necessary
        if len(vec1) < len(vec2):
            vec1 = np.append(vec1, np.zeros(len(vec2) - len(vec1)))
        else:
            vec2 = np.append(vec2, np.zeros(len(vec1) - len(vec2)))
    return vec1, vec2


def calculate_cosine_similarity(vec1, vec2):
    vec1, vec2 = debug_vector_sizes(vec1, vec2)
    if np.linalg.norm(vec1) != 0 and np.linalg.norm(vec2) != 0:
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    return 0


def apply_tfidf_vectorizer(text_list, vectorizer):
    # Transform list of texts into TF-IDF vectors
    tfidf_matrix = vectorizer.transform([" ".join(text_list)])
    return tfidf_matrix.mean(
        axis=0
    )  # You might want to average here if your logic requires, but typically you just return the matrix


def calculate_cosine_similarity_tfidf(vec1, vec2):
    # Convert vec1 and vec2 to dense arrays if they are in sparse format
    if scipy.sparse.issparse(vec1):
        vec1 = vec1.toarray()
    if scipy.sparse.issparse(vec2):
        vec2 = vec2.toarray()

    # Convert vec1 and vec2 to NumPy arrays if they are np.matrix instances
    vec1 = np.asarray(vec1)
    vec2 = np.asarray(vec2)

    # Now you can safely compute cosine similarity
    return cosine_similarity(vec1, vec2)
