# Diccionario de datos
## Fuente de datos GOOGLE
### Negocios (metadata):
- *name* - nombre del negocio
- *address* - dirección del negocio
- *gmap_id* - ID del negocio en Google Maps
- *description* - descripción del negocio
- *latitude* - latitud del negocio
- *longitude* - longitud del negocio
- *category* - categoría del negocio
- *avg_rating* - calificación promedio del negocio
- *num_of_reviews* - número de reseñas
- *price* - precio del negocio
- *hours* - horario de apertura
- *MISC* - información miscelánea
- *state* - estado actual del negocio (por ejemplo, cerrado permanentemente)
- *relative_results* - negocios relativos recomendados por Google
- *url* - URL del negocio

### Reseñas (states):

- *user_id* - ID del usuario
- *name* - nombre del usuario
- *time* - tiempo de la reseña (tiempo Unix)
- *rating* - calificación del negocio
- *text* - texto de la reseña
- *pics* - imágenes de la reseña
- *resp* - respuesta del negocio a la reseña, incluyendo tiempo Unix y texto de la respuesta
- *gmap_id* - ID del negocio en Google Maps

## Fuente de datos YELP

### Negocios (business):
- *business_id* - ID del negocio, que se refiere al negocio en cuestión
- *name* - nombre del negocio
- *address* - dirección completa del negocio
- *city* - ciudad
- *state* - código de dos letras del estado donde se ubica el negocio
- *postal code* - código postal
- *latitude* - latitud
- *longitude* - longitud
- *stars* - calificación en estrellas, redondeada a 0 o 0.5
- *review_count*- número entero de reseñas
- *attributes* - atributos del negocio como valores. Algunos valores de atributos también pueden ser objetos
- *categories* - lista de categorías de los negocios
- *hours* - horario de apertura y cierre, las horas están en formato de 24 horas

## Reseñas (review):

- *review_id* - ID de la reseña (cadena de 22 caracteres)
- *user_id* - ID único del usuario (cadena de 22 caracteres), hace referencia al usuario en user.json
- *business_id* - ID del negocio (cadena de 22 caracteres), hace referencia al negocio en business.json
- *stars* - puntaje en estrellas de 1 al 5 (entero)
- *date* - fecha en formato YYYY-MM-DD (cadena de texto)
- *text* - la reseña en inglés (cadena de texto)
- *useful* - número de votos como reseña útil (entero)
- *funny* - número de votos como reseña graciosa (entero)
- *cool* - número de votos como reseña cool (entero)