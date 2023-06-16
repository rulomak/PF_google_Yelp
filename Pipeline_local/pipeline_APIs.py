import pymysql
from azure.storage.blob import BlobServiceClient
import pandas as pd
import os
from dotenv import load_dotenv
import datetime as dt
import yfinance as yf


# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Variables de conexión
account_name = os.getenv('DB_NAME')
account_key = os.getenv('DB_PASSWORD')
container_name = os.getenv('DB_CONTAINER_NAME')
folder_name = 'indices'  # Nombre de la carpeta dentro del Data Lake
local_file_path = ''


# Crea la cadena de conexión
conn_str = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"

# Crea el cliente del servicio de blob
blob_service_client = BlobServiceClient.from_connection_string(conn_str)

# Obtén una referencia al contenedor
container_client = blob_service_client.get_container_client(container_name)

# Lista los archivos en el contenedor
blob_list = container_client.list_blobs()
print("conexion con azure establecida")



##__WEB_Scraping __##
# se declaran las variables de comienzo y final en lo formatos adecuados 

start = dt.datetime(2022, 6, 1).strftime('%m-%d-%Y')
end = dt.datetime.now().date().strftime('%m-%d-%Y')

# ruta para descargar el .csv 
url = f"https://www.marketwatch.com/investing/index/sp500.253010/downloaddatapartial?startdate={start}%2000:00:00&enddate={end}%2000:00:00&daterange=d30&frequency=p1d&csvdownload=true&downloadpartial=false&newdates=false&countrycode=xx"

# se lee el dataset directamente desde la url 
df_sp500HRL = pd.read_csv(url)

# selecionan columnas de interes
df_sp500HRL = df_sp500HRL[['Date','Close']]

print("dataset sp_HRL Creado")



##___API____##
# se define  fecha de comienzo y fecha de final  (Actual)   
start = dt.datetime(2022,6,1)
end = dt.datetime.now().date()
company = '^GSPC'   # sp500  

# se carga la data 
data = yf.download(company, start , end)


# se crea el dataset con los precios de cierre 
df = pd.DataFrame(data['Close'])

# Reiniciar el índice del DataFrame
df.reset_index(inplace=True)

# Convertir el índice en una columna de fecha
df['fecha'] = pd.to_datetime(df['Date']).dt.date

# Eliminar la columna 'Date' si ya no es necesaria
df.drop('Date', axis=1, inplace=True)

print("dataset sp500 Creado")


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


# se crea la tabla si no existe  sp_HRL
consulta = """
CREATE TABLE IF NOT EXISTS sp_HRL (
    id INT AUTO_INCREMENT,
    fecha DATE,
    close FLOAT,
    PRIMARY KEY (id)
)
"""
cursor.execute(consulta)


# se crea la tabla si no existe  sp500
consulta = """
CREATE TABLE IF NOT EXISTS sp500 (
    id INT AUTO_INCREMENT,
    fecha DATE,
    close FLOAT,
    PRIMARY KEY (id)
)
"""
cursor.execute(consulta)

print("Insertando infomarcion en la tabla sp_HRL")
# se ingresa nueva info a la tabla
for _, fila in df_sp500HRL.reset_index().iterrows():
    fecha = pd.to_datetime(fila['Date']).strftime('%Y-%m-%d') # se normaliza fecha  
    close = float(fila['Close'].replace(',', ''))
    consulta = "INSERT INTO sp_HRL (fecha, close) VALUES (%s, %s)"
    cursor.execute(consulta, (fecha, close))

conector.commit()
print("data insertada en la tabla sp_HRL ")



print("Insertando infomarcion en la tabla sp500")
# se ingresa nueva info a la tabla sp500
for _, fila in df.iterrows():
    fecha = fila['fecha']
    close = float(fila['Close'])
    consulta = "INSERT INTO sp500 (fecha, close) VALUES (%s, %s)"
    cursor.execute(consulta, (fecha, close))

conector.commit()

print("data insertada en la tabla sp500 ")

print('pipeline finalizado')


conector.close()


