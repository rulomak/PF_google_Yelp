from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import re


def clustering_google(df):
    df = df.dropna(subset=['category'])
    df['category'] = df['category'].fillna('')
    df['category'] = df['category'].apply(lambda x: re.sub(r"[\[\]',]", "", x)) #se elimina los caracteres de la lista
    categories = df['category'].unique()

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(categories)

    seed = 128  # Establecer una semilla
    kmeans = KMeans(n_clusters=6, random_state=seed)
    kmeans.fit(X)

    cluster_labels = kmeans.predict(vectorizer.transform(df['category']))
    df['cluster'] = cluster_labels

    # for category, cluster in zip(categories, kmeans.labels_): #visualizar la clasificacion de cada fila
    #     print(f"Categoría: {category} - Cluster: {cluster}")

    df_cluster_3 = df[df['cluster'] == 3].copy()
    df_cluster_3 = df_cluster_3.dropna(subset=['category'])
    df_cluster_3['category'] = df_cluster_3['category'].fillna('')

    categories_cluster_3 = df_cluster_3['category'].unique()

    vectorizer = TfidfVectorizer()
    X_cluster_3 = vectorizer.fit_transform(categories_cluster_3)

    kmeans_cluster_3 = KMeans(n_clusters=3, random_state=42) #volver a clasificar los datos del cluster numero 3 por que ese queda con muchos datos agrupados 
    kmeans_cluster_3.fit(X_cluster_3)

    cluster_labels_cluster_3 = kmeans_cluster_3.predict(vectorizer.transform(df_cluster_3['category']))
    df_cluster_3['cluster2'] = cluster_labels_cluster_3

    replacements = {2: 3, 1: 6, 0: 7} #se agregan los cluster faltantes de la columna original cluster
    df_cluster_3['cluster2'] = df_cluster_3['cluster2'].replace(replacements)
    df_cluster_3['cluster'] = df_cluster_3['cluster2']
    df_cluster_3 = df_cluster_3.drop('cluster2', axis=1)

    df.update(df_cluster_3[['cluster']])# Actualizar el DataFrame original con los nuevos datos
    df['cluster'] = df['cluster'].astype(int)



    diccionario_cluster ={
        0: 'industria de servicios automotrices',
        1: 'industria de la belleza',
        2: 'industria de ventas y servicios',
        3: 'industria minorista',
        4: 'restaurantes',
        5: 'hoteles',
        6: 'cuidado de la salud'
    }
    df['cluster'] = df['cluster'].map(diccionario_cluster)
    df.rename(columns={'cluster': 'sector_economico'}, inplace=True)

    
    return df



def clustering_yelp(df):

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


    return df