from azure.storage.blob import BlobServiceClient
import pandas as pd
import os
from dotenv import load_dotenv
import pymysql
# Importa las funciones de clusterización 
from clustering import clustering_google, clustering_yelp


# Cargar las variables de entorno desde el archivo .env
load_dotenv()


# Variables de conexión
account_name = os.getenv('DB_NAME')
account_key = os.getenv('DB_PASSWORD')
container_name = os.getenv('DB_CONTAINER_NAME')
local_folder = ""

# Crea la cadena de conexión
conn_str = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"

# Crea el cliente del servicio de blob
blob_service_client = BlobServiceClient.from_connection_string(conn_str)

# Obtén una referencia al contenedor
container_client = blob_service_client.get_container_client(container_name)

# Lista los archivos en el contenedor
blob_list = container_client.list_blobs()
print("conexion DataLake establecida")


## ___ base de datos MySql_ Azure__##
# se intenta conexion con la base de datos 
try:
    conector = pymysql.connect(
        host= os.getenv('HOST'),
        port= 3306,
        user= os.getenv('USER'),
        password= os.getenv('PASSWORD'),
        db= os.getenv('DB'),
        ssl={'ssl': {'sslmode': 'require'}}
    )

    print("Conexión exitosa a la base de datos.")
    # cursor se utiliza para ejecutar consultas SQL 
    cursor = conector.cursor()

except pymysql.Error as e:
    print("Error al conectar a la base de datos:", e)



# ** Descarga los archivos y realiza transformaciones con pandas
for blob in blob_list:
    # Descarga el archivo localmente
    local_file_path = f"{local_folder}{blob.name}"
    with open(local_file_path, "wb") as file:
        blob_client = container_client.get_blob_client(blob)
        file.write(blob_client.download_blob().readall())
        print(f"procesando {blob.name}")

    # Obténer la extensión del archivo
    file_extension = os.path.splitext(blob.name)[1]

    # Realiza las transformaciones según la extensión y el nombre de archivo
    if file_extension == '.csv':
        if 'metadata' in blob.name.lower():
        # Realiza las operaciones de transformación para archivos CSV con "metadata" en su nombre
            df_meta = pd.read_csv(local_file_path)
            # se llama a la funcionde crustering 
            df_meta = clustering_google(df_meta)  
            print(f"{blob.name} Transformacion Finalizada")

            # se inserta la data  en la tabla
            print("Insertando infomarcion en la tabla sitios_google")
            consulta = "INSERT INTO sitios_google (gmap_id, name, address, description, latitude, longitude, category, avg_rating, num_of_reviews, sector_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            valores = [
                (
                    fila['gmap_id'],
                    fila['name'],
                    fila['address'],
                    fila['description'],
                    fila['latitude'],
                    fila['longitude'],
                    fila['category'],
                    fila['avg_rating'],
                    fila['num_of_reviews'],
                    fila['sector_id']
                )
                for _, fila in df_meta.iterrows()
            ]
            cursor.executemany(consulta, valores)
            print("data insertada en la tabla sitios_google")
        else:
            # Realiza las operaciones de transformación para archivos CSV sin "metadata" en su nombre
            df_rev = pd.read_csv(local_file_path)
            # se borran columnas de mas 
            # df = df.drop(columns=['pics', 'resp'])
            # Se crea una nueva columna con el nombre del estado  extraido del nombre de dataframe  
            df_rev['state'] = os.path.splitext(blob.name)[0]
        
            print(f"{blob.name} Transformacion Finalizada")

        
            # se inserta la informacion en la tabla  
            print("Insertando infomarcion en la tabla opiniones_google")
            consulta = """
            INSERT INTO opiniones_google (user_id, name, time, rating, text, pics, resp, gmap_id, state)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            valores = [
            (
                fila['user_id'],
                fila['name'],
                fila['time'],
                fila['rating'],
                fila['text'],
                fila['pics'],
                fila['resp'],
                fila['gmap_id'],
                fila['state']
            )
            for _, fila in df_rev.iterrows()
            ]

            cursor.executemany(consulta, valores)
            print("data insertada en la tabla opiniones_google")

    elif file_extension == '.parquet':
        if 'business' in blob.name.lower():
            # Realiza las operaciones de transformación para archivos .parquet
            df_business = pd.read_parquet(local_file_path)
            # se llama a la funcionde crustering 
            df_business = clustering_yelp(df_business)

            # se inserta la data en la tabla  
            print("Insertando infomarcion en la tabla negocios_yelp")
            consulta = """
                    INSERT INTO negocios_yelp (business_id, name, address, city, state, postal_code, latitude, longitude, stars, review_count, is_open, attributes, categories, hours, sector_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """

            valores = [
                (
                    fila['business_id'],
                    fila['name'],
                    fila['address'],
                    fila['city'],
                    fila['state'],
                    fila['postal_code'],
                    fila['latitude'],
                    fila['longitude'],
                    fila['stars'],
                    fila['review_count'],
                    fila['is_open'],
                    fila['attributes'],
                    fila['categories'],
                    fila['hours'],
                    fila['sector_id']
                )
                for _, fila in df_business.iterrows()
            ]

            cursor.executemany(consulta, valores)
            print("data insertada en la tabla negocios_yelp")
        
        elif 'reviews' in blob.name.lower():
            # Realiza las operaciones de transformación para archivos .parquet
            df_reviews = pd.read_parquet(local_file_path)

            #  se inserta la data en la tabla  
            print("Insertando infomarcion en la tabla opiniones yelp ")

            consulta = """
                INSERT INTO opiniones_yelp (review_id, user_id, business_id, stars, useful, funny, cool, text, date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

            valores = [
                (
                    fila['review_id'],
                    fila['user_id'],
                    fila['business_id'],
                    fila['stars'],
                    fila['useful'],
                    fila['funny'],
                    fila['cool'],
                    fila['text'],
                    fila['date']
                )
                for _, fila in df_reviews.iterrows()
            ]

            cursor.executemany(consulta, valores)
            
            print("data insertada en la tabla opiniones yelp")

        elif 'tips' in blob.name.lower():
            # Realiza las operaciones de transformación para archivos .parquet
            df_tips = pd.read_parquet(local_file_path)

            #  se inserta la data en la tabla  
            print("Insertando infomarcion en la tabla recomendacion yelp ")

            
            consulta = """
                INSERT INTO recomendacion_yelp  (user_id, business_id, text, date)
                VALUES (%s, %s, %s, %s)
                """

            valores = [
                (
                    fila['user_id'],
                    fila['business_id'],
                    fila['text'],
                    fila['date']
                )
                for _, fila in df_tips.iterrows()
            ]

            cursor.executemany(consulta, valores)
            print("data insertada en la tabla recomendaciones yelp")

        elif 'user' in blob.name.lower():
            # Realiza las operaciones de transformación para archivos .parquet
            df_user = pd.read_parquet(local_file_path)

            #  se inserta la data en la tabla  
            print("Insertando infomarcion en la tabla usuario yelp ")

            consulta = """
            INSERT INTO usuarios_yelp (user_id, name, review_count, yelping_since, useful, funny, cool, elite, friends, fans, average_stars)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            valores = [
                (
                    fila['user_id'],
                    fila['name'],
                    fila['review_count'],
                    fila['yelping_since'],
                    fila['useful'],
                    fila['funny'],
                    fila['cool'],
                    fila['elite'],
                    fila['friends'],
                    fila['fans'],
                    fila['average_stars']
                )
                for _, fila in df_user.iterrows()
            ]

            cursor.executemany(consulta, valores)

            print("data insertada en la tabla usuario yelp")
        else: 
            print(f"No se puede procesar el archivo {blob.name}, la tabla no existe en la base de datos")

    else:
        print(f"No se puede procesar el archivo {blob.name}")



print('ETL finalizado')


