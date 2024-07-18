import Doc, Embedding as emb
import numpy as np

from sklearn.cluster import KMeans
from dotenv import load_dotenv

def get_indices(num_clusters):
    closest_indices = []

    for i in range(num_clusters):
        distances = np.linalg.norm(vectors - kmeans.cluster_centers_[i], axis=1)
        closest_index = np.argmin(distances)
        closest_indices.append(closest_index)
        selected_indices = sorted(closest_indices)
    
    return selected_indices

load_dotenv()
doc = Doc.Document()
doc.load_from_pdf('./Books/Cover Letter.pdf')

cleaned_text = doc.data
docs, vectors = emb.generate_embedding(open_source=False, text=cleaned_text)

num_clusters = 5
kmeans = KMeans(n_clusters=num_clusters, random_state=42).fit(vectors)

selected_indices = get_indices(num_clusters)
