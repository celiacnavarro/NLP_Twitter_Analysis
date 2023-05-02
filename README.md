# Social media monitoring: The Bridge

This project involves obtaining Twitter data from mentions that reference The Bridge school in order to measure the impact of its brand on social media and make data-driven decisions.
The generated database is deployed on the cloud using Amazon Web Services' (AWS) RDS service.
An initial exploratory data analysis has been conducted, followed by the use of a pre-trained Natural Language Processing (NLP) model to perform a sentiment analysis of the tweets mentioning The Bridge.

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

### Instructions for use

To use this project, follow these steps:

- Clone this repository on your local machine.

 ```git clone url_repository```

- Install the necessary libraries contained in the requirements.txt file using the following command in the terminal:

```pip install -r requirements.txt```

- Create a database in AWS RDS and ensure you have the access credentials.

- Add the access credentials for the database in the database.py file and execute it.

```python database.py```

- Run the eda.py and nlp.py files in the terminal using the following commands:


```python eda.py```


```python nlp.py```


