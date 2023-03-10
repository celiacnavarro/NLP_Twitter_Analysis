# Monitorización de redes sociales: The Bridge

En este proyecto se realiza una obtención de datos de Twitter de las menciones que nombran a la escuela The Bridge con el objetivo de medir el impacto de su marca en redes sociales y tomar decisiones basadas en los datos.
La base de datos generada se encuentra desplegada en Cloud mediante el servicio RDS de Amazon Web Services (AWS).
Se ha realizado un primer análisis exploratorio de los datos y posteriormente, se ha utilizado un modelo pre-entrenado de Natural Lenguage Processing (NLP) para realizar un análisis del sentimiento de los tweets que mencionan a The Bridge.

### Directory tree
```
twitter_analysis
│   README.md
│   requirements.txt
│   database.py
|   eda.py
|   nlp.py
|   Presentacion.ppt
│
└───data
│   │   tweets.csv
|   |   users.csv
|   |   tweets_cleaned.csv
|   |   predictions.csv
│
└───models
│   │   model.pkl
|
└───notebooks
│   │   Notebook_data_analysis.ipynb
│   │   Notebook_database.ipynb
│   │   Notebook_machine_learning.ipynb
|
└───utils
│   │   functions.py
└───img
    │   correlations.png
    │   ...
 ```

### Modo de uso
Para utilizar este proyecto, siga los siguientes pasos:

- Clone este repositorio en su máquina local.

 ```git clone url_repositorio```

- Instale las librerías necesarias contenidas en el archivo requirements.txt utilizando el siguiente comando en la terminal:

```pip install -r requirements.txt```

- Cree una base de datos en AWS RDS y asegúrese de tener las credenciales de acceso.

- Añada las credenciales de acceso a la base de datos en el archivo database.py y ejecútelo.

```python database.py```

- Ejecute el los archivos eda.py y nlp.py en la terminal utilizando el siguiente comando:


```python eda.py```


```python nlp.py```


