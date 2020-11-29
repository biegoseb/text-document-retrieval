# Recuperación de Documentos de Texto

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

Este proyecto consiste en entender y aplicar algoritmos de busqueda y recuperación de la información basada en el contenido.
Para esto, se construye un indice invertido óptimo para tareas de busqueda y recuperación en documentos de texto que se encuentran en memoria secundaria.
Los datos se han utilizando son de un conjunto de tweets en formato json. Solo se contarán los tweets originales y no retweets.

En el informe se muestra las comparaciones al usar queries con los mejores resultados.

## Fundamentos y descripción de las técnicas



### Backend

Se ha construido un indice invertido optimo para recuperación por ranking para consultas de texto libre.


Para esto, primero se lee todos los tweets almacenados que esten en formato json y sean del 2018:

    def read_files(self):
    for base, dirs, files in os.walk(./):
      for file in files:
        f = join(base, file)
        if f.endswith(.json) and "tweets_2018-" in f:
          self.tweets_files.append(f)


#### Filtrar stopwords
Con la ayuda de la libreria *nltk* creamos una lista de stopwords en español y añadimos más elementos

    nltk.download('stopwords')
    stoplist = stopwords.words("spanish")
    stoplist += ['?','aqui','.',',','»','«','â','ã','>','<','(',')','º','u']


#### Reduccion de palabras(stemming)

Vamos a obtener la raiz de la palabra con ayuda de la libreria *SnowballStemmer* para el idioma español

    stemmer = SnowballStemmer('spanish')
    token = stemmer.stem(word)

#### Tokenización

 _Como se hacen se guardan los stopwords_


 _Como se almacena y limpia cada tweet?_

## Resultados experimentales


### Consultas

### Nuestra consulta en lenguaje natural:
>El señor Daniel Urresti me bloqueo por cuestionar continuamente su candidatura


Cuadros para ver el desempeño de los indice invertidos:




 ##### Tiempos de ejecución

- Tiempos de cada test

    | Test   | Input  	 |  Tiempo (ms) |
    |------  |--------   |--------------|
    |  1     | 100       |              |
    |  2     | 500 	 |       	|
    |  3     | 1000 	 |        	|





**Discusión y Análisis**

Una de las conclusiones que obtuvimos es al momento de hacer una consulta con un nombre **Reggiardo**, como aparece en todos los archivos json, la norma tiende a ser 0.


## Pruebas de uso y presentación
Link del video de funcionalidad.[ Video de funcionalidad](https://drive.google.com/drive/folders/__________)
