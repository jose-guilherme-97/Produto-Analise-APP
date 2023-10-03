import pandas as pd
import numpy as np
import logging
from genderbr.genderbr import get_gender

# Scraper
from google_play_scraper import Sort, reviews
from app_store_scraper import AppStore


logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level="INFO")

class Scraper(object):
    def __init__(self):
        logging.info("Iniciando Scraper")
        super(Scraper,self).__init__()    

    def return_results(self, df_google, df_apple):
        return pd.concat([df_google,df_apple])
    
    def get_genero(self,nome):
        return  get_gender(nome)


    def google_scraper(self, name = None, language = None, country = None, filtro_data_min = None, filtro_data_max = None, qtd = 50):
        if name ==  None:
            raise ValueError("O argumento app_name deve ser informado")
        if language ==  None:
            raise ValueError("O argumento language deve ser informado")
        if country ==  None:
            raise ValueError("O argumento country deve ser informado")

        reviews_results,_ = reviews(
        name,
        #sleep_milliseconds=0, # defaults to 0
        lang=language, # defaults to 'en'
        country=country, # defaults to 'us'
        sort=Sort.NEWEST, # defaults to Sort.MOST_RELEVANT
        count = qtd
        )

        df = pd.DataFrame(np.array(reviews_results), columns=['reviews'])
        #print(df)
        df = df.join(pd.DataFrame(df.pop('reviews').tolist()))

        if filtro_data_min is not None:
            df = df.loc[df['at'] >= filtro_data_min]
        
        if filtro_data_max is not None:
            df = df.loc[df['at'] <= filtro_data_min]

        df = df.drop(['reviewId', 'userImage',
        'thumbsUpCount', 'reviewCreatedVersion', 'replyContent',
        'repliedAt'], axis=1)

        df['aplicativo'] = 'Play Store'
        return df

    def apple_scraper(self, app_name = None, app_id = None, country = None, filtro_data_min = None, filtro_data_max = None):
        if app_name ==  None:
            raise ValueError("O argumento app_name deve ser informado")
        if app_id ==  None:
            raise ValueError("O argumento app_id deve ser informado")
        if country ==  None:
            raise ValueError("O argumento country deve ser informado")

        scaper_app = AppStore(country=country, app_name=app_name, app_id = app_id)
        scaper_app.review(how_many=50)

        df = pd.DataFrame(np.array(scaper_app.reviews), columns=['review'])
        df = df.join(pd.DataFrame(df.pop('review').tolist()))
        df.rename(columns = {'review': 'content', 'date': 'at', 'rating': 'score'}, inplace = True)

        if filtro_data_min is not None:
            df = df.loc[df['at'] >= filtro_data_min]
        
        if filtro_data_max is not None:
            df = df.loc[df['at'] <= filtro_data_min]

        df = df.drop(['isEdited', 'title', 'developerResponse'], axis=1)

        df['aplicativo'] = 'App Store'

        return df

def categoriza_score(score):
    if score < 3:
        return "Negativo"
    elif score > 3:
        return "Positivo"
    else:
        return "Neutro"

def coordena_processo(name_google = None, name_apple = None, apple_id = None, qtd = 50):
    scraper = Scraper()
    if name_google is not None and name_apple is None and apple_id is None:
        logging.info("Iniciando a construção dos DataFrames para Google Play")
        df_results = scraper.google_scraper(name = name_google, language = 'pt-br', country = 'br', qtd=qtd)
        logging.info("Finalizou a construção dos DataFrames para Google Play")

    if name_apple is not None and apple_id is not None and name_google is None:
        logging.info("Iniciando a construção dos DataFrames para App Store")
        df_results = scraper.apple_scraper(app_name = name_apple, app_id = apple_id, country = 'br')
        logging.info("Finalizou a construção dos DataFrames para App Store")

    df_results['sentimento'] = df_results['score'].apply(categoriza_score)
    return df_results