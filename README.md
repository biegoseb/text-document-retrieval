# Recuperación de Documentos de Texto

![](screenshots/ss.png)

## Integrantes

| Nombre y Apellidos |
|---|
|Diego Enciso Lozano |
|Luis Jauregui Vera	 |
|Jonathan Hoyos      |


## Tabla de contenido
<details>
<summary>"Clic para navegar: "</summary>

- [Introducción](#Introducción)
- [Fundamentos y descripción de las técnicas](#Fundamentos-y-descripción-de-las-técnicas)
- [Resultados experimentales](#Resultados-experimentales)
- [Pruebas de uso y presentación](#Pruebas-de-uso-y-presentación)

</details>

## Introducción

Este proyecto consiste en aplicar algoritmos de búsqueda y recuperación de la información basada en el contenido.
Para esto, se construye un índice invertido óptimo para tareas de búsqueda y recuperación en documentos de texto que se encuentran en memoria secundaria.
Los datos utilizados como contenido son un conjunto de tweets en formato json. Solo se contarán los tweets originales y no retweets.

En el informe se muestra las comparaciones al usar queries con los mejores resultados.

## Implementación del índice invertido
#### Backend
Se ha construido un índice invertido óptimo para recuperación por ranking para consultas de texto libre.

### Preprocesamiento

##### Filtrado de stopwords
Con la ayuda de la librería *nltk* se crean los stopwords en español

    nltk.download('stopwords')
    stoplist = stopwords.words("spanish")
    stoplist += ['?','aqui','.',',','»','«','â','ã','>','<','(',')','º','u']


##### Reducción de palabras (stemming)

Se obtiene la raíz de la palabra con ayuda de la librería *SnowballStemmer* para el idioma español

    stemmer = SnowballStemmer('spanish')
    token = stemmer.stem(word)

##### Tokenización
Se hace uso de una función de limpieza que removerá caracteres especiales, signos de puntuación, emojis y urls para tener un texto limpio.

    def clean_text(self, text):
        text = self.remove_special_character(text)
        text = self.remove_punctuation(text)
        text = self.remove_emoji(text)
        text = self.remove_url(text)
        text = nltk.word_tokenize(text)
    return text

 Finalmente, para obtener los tokens, se recorre toda la lista de tweets en  _tweets_files_ , se guarda el texto en un _text_list_ y se procede a limpiar cada texto con la función mencionada. Con esto, se obtienen todos los tokens.


     for file in self.tweets_files:
          json_file = open(file, encoding = 'utf-8')
          text_list = [(e['text'],e['id']) for e in json.loads(json_file.read()) if not e["retweeted"]]
          json_file.close()
          for text in text_list:
            self.tweets_count += 1
            t = text[0]
            t = self.clean_text(t.lower())
            for word in t:
              if word not in stoplist:
                token = stemmer.stem(word)


### Construcción del índice

Se cargan los archivos de los tweets, y se almacena como tupla el *text* y *id* de cada tweet. Dentro del diccionario _inverted_index_ guardamos para cada indice su tf_idf, con esto se calcula su norma.

    if token not in self.inverted_index.keys():
              self.inverted_index[token] = {"df":0}
            if file not in self.inverted_index[token].keys():
              self.inverted_index[token]["df"] += 1
              self.inverted_index[token][file] = {"tf":0}
              self.inverted_index[token][file]["tweets"] = [ ]
            found = False
            for x in self.inverted_index[token][file]["tweets"]:
              if x["tweet_id"] == text[1]:
                found = True
                x["freq"] += 1
                break
            if not found:
              self.inverted_index[token][file]["tweets"].append({"tweet_id":text[1], "freq":1})
            self.inverted_index[token][file]["tf"] += 1



#### Consulta :
>"El señor Daniel Urresti me bloqueo por cuestionar continuamente su candidatura"

Para obtener los resultados de nuestra consulta seguimos estos pasos:

* Se limpia la query en lenguaje natural
* Se saca el TD e IDF
* Se halla la frecuencia de cada palabra en el query
* Si la palabra esta en un indice invertido, se calcula el indice invertido
* Se obtiene el Tf-idf del query

Al final, ordenamos en una lista de cosenos- que guarda el Id del documento,la similitud y su lista de tweets- de mayor a menor por el que tenga mayor similitud .

## Frontend
### Resultados experimentales
Cuadros para ver el desempeño de los indice invertidos:



**Discusión y Análisis**

Una de las conclusiones que obtuvimos es al momento de hacer una consulta con un nombre **Reggiardo**, como aparece en todos los archivos json, la norma tiende a ser 0.


### Pruebas de uso y presentación
Link del video de funcionalidad.[ Video de funcionalidad](https://drive.google.com/drive/folders/__________)
