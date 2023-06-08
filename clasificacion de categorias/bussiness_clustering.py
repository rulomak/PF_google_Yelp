import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import re


df = pd.read_parquet('business.parquet')
print(df)
# df = df.sample(frac=0.25, random_state=42) #tomar una muestra de una cuarta parte del dataset para hacer tests

df = df.dropna(subset=['categories'])

df['categories'] = df['categories'].fillna('')
df['categories'] = df['categories'].apply(lambda x: re.sub(r"[\[\]',]", "", x)) #se elimina los caracteres de la lista
categories = df['categories'].unique()

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(categories)

seed = 128  # Establecer una semilla
kmeans = KMeans(n_clusters=8, random_state=seed)
kmeans.fit(X)

cluster_labels = kmeans.predict(vectorizer.transform(df['categories']))
df['cluster'] = cluster_labels

for category, cluster in zip(categories, kmeans.labels_): #visualizar la clasificacion de cada fila
    print(f"Categoría: {category} - Cluster: {cluster}")
    
replacements = {2: 0, 5: 0, 7: 0} #se agregan los cluster faltantes de la columna original cluster
df['cluster'] = df['cluster'].replace(replacements)


diccionario_cluster ={
    0: 'industria de alimentos y bebidas',
    1: 'comercio' ,
    3: 'industria de servicios automotrices' ,
    4: 'industria de la belleza',
    6: 'cuidado de la salud'
}
df['cluster'] = df['cluster'].map(diccionario_cluster)
df.rename(columns={'cluster': 'sector_economico'}, inplace=True)


df.to_csv('business_clustered.csv', index=False)    