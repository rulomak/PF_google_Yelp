## Resumen del trabajo realizado

*** 
### Este proyecto consiste en la implementación de dos pipelines en Python que automatizan el procesamiento de datos y su ingestión en un Data Warehouse en Azure. A continuación, se presenta un resumen de cada uno de ellos:

## **Pipeline etl: Procesamiento de archivos en un Data Lake**


Este pipeline se conecta a un Data Lake en Azure y recorre todos los archivos ingresados en él. Cada archivo es procesado individualmente, aplicando transformaciones específicas según su extensión y nombre. Una vez transformado, el archivo es ingestado en un Data Warehouse que utiliza MySQL como motor de base de datos. Para asegurar la seguridad de las conexiones, las credenciales de conexión se almacenan en un archivo de entorno (.env).

## **Pipeline APIs: Obtención de datos de Yahoo Finance y Web Scraping de MarketWatch**

En este segundo pipeline, se establece una conexión con la API de Yahoo Finance para descargar información sobre un índice específico. Los datos descargados se utilizan para crear un dataset que posteriormente es ingresado en el Data Warehouse. Además, se realiza un web scraping en la página web de MarketWatch, accediendo a una URL de descarga y proporcionando parámetros de inicio y fin. Los datos obtenidos a través del web scraping también son ingestados en el Data Warehouse.



En resumen, estos pipelines automatizan la transformación y la ingestión de datos desde un Data Lake y fuentes externas (API y web scraping) hacia un Data Warehouse en Azure. Se implementan medidas de seguridad al almacenar las credenciales de conexión en un archivo de entorno.