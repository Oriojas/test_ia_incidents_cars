# test_ia_incidents_cars
Para este análisis el entorno el gestor de dependencia es poetry y la versión general de python la 3.10, el demo se encontrará temporalmente en: http://ec2-44-210-144-99.compute-1.amazonaws.com:8501/ 

## Instalación del repositorio
Para instalar el presente repositorio clonar en una carpeta en local con el siguiente comando ne una terminal o con su IDE favorito:

`git clone https://github.com/Oriojas/test_ia_incidents_cars.git`

## Instalación de entorno
### poetry
Este código se desarrollo con el gestor de dependencias poetry https://python-poetry.org/ si se tiene instalado este gestor de dependencias en la carpeta raíz del repositorio ejecutar el siguiente comando:

`poetry update`

Este paso se demorará unos minutos dependiendo del computador y la conexión a internet. posteriormente para ingresar al entorno virtual:

`poetry shell`

En este momento ya se pueden ejecutar los comandos que se sujeridos mas adelante para ejecutar las funcionalidades

## pip
Para este caso se creo un archivo de requierements.txt y con esto se sugiere crear un entorno virtual .env ingresar y ejecutar el comando:

`pip3 install - r requierements.txt`

## Ejecución de notebooks
Una vez dentro del entorno virtual bien sea poetry o pip simplemente abrir jupyter-notebook y ejecutar los archivos con la extensión *.ipynb
* [eda_clean_data.ipynb](eda_clean_data.ipynb) en este archivo se encuentra en análisis exploratorio inicial
* [model_v1.ipynb](model_v1.ipynb) en este archivo se encuentra las primera iteración del modelo 
* [model_final.ipynb](model_final.ipynb) en este archivo se encuentra la optimización de los hiperparametros del modelo sugerido
Dentro de todos los notebooks se encuentran las notas y comentarios de las acciones tomadas en cada caso

## Ejecución del front
Para este caso ejecutar dentro de la carpeta raíz el siguiente comando y seguir las instrucciones:

`streamlit run front_app.py`

Este se ejecutara en el localhost en el puerto 8090

## Ejecución de la API
Para este caso dentro del entorno virtual ejecutar el comando

`python3 main_api.py `

Este se ejecutara en el localhost en el puerto 8501

## Archivo EDA
En la carpeta **eda_files** esta el resultado del análisis exploratorio de los datos

## Consideraciones generales
* Es importante contar con las carpetas **data** y **model** aunque el contenido se genra al ejecutar los notebooks con los datos enviados, para no esperar le ejecuaicón se enviaran comprimidos por correo electrónico
* Para poder acceder a los demos es primordial revisar la estructura de datos sugerida


