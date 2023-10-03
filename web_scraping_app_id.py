from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import re
import streamlit as st
import plotly.express as px
import analise_aplicativo
import transformers_nlp

def get_id(provider = 'Google', company = None):
    """
    Function that receive a provider ('google' or 'apple') and a company name. After this, does a search for collect
    the id (and/or other arguments that be necessary to get data from scraper code)
    """
    if company == None:
        raise ValueError(f"Please, insert a value different of None as company value")
    
    if provider == 'Google':
        url = f'https://play.google.com/store/search?q={company}&c=apps'
        class_name = 'Qfxief'
        attribute = 'href'
    elif provider == 'Apple':
        url = f'https://www.apple.com/br/search/{company}?src=serp'
        class_name = 'rf-serp-productname-link'
        attribute = 'href'
    else:
        raise ValueError(f"Not a valid provider. Only 'google' or 'apple' are currently enableded")
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)
    url_id = driver.find_element(By.CLASS_NAME,class_name).get_attribute(attribute)
    if provider == "Google":
        for match in re.finditer('id', url_id):
            pos = match.span()[1]
            break

        id = url_id[pos + 1:]

    if provider == "Apple":
        for match in re.finditer('/id', url_id):
            pos = match.span()
            break
        for match in re.finditer('app/', url_id):
            pos_name = match.span()[1]
            break
        app_name = url_id[pos_name:pos[0]]

        id = url_id[pos[1]:]
    if provider == "Google":
        return id
    else:
        return (id,app_name)

def convert_df(df):
   """
   Function that transform a dataframe (pandas) into csv file
   """
   return df.to_csv(index=False).encode('utf-8')

__name__ = "main"
if __name__ == "main":
    # Store the initial value of widgets in session state
    st.title('Ferramenta de análise de aplicativos')
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    col1, col2 = st.columns(2)

    with col1:
        st.image("brain_logo.jpg")
        st.checkbox("Desabilitar seleção", key="disabled")
        st.radio(
            "Selecione a visibilidade do título da caixa de seleção 👉",
            key="visibility",
            options=["visible", "hidden", "collapsed"],
        )

    with col2:
        st.image("ia_foto.jpg")
        option = st.selectbox(
            "Selecione a fonte da qual deseja coletar informações",
            options=("Google", "Apple", "Ambos"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )
        count = int(st.number_input('Entre com o número de dados a serem coletados pela fonte Google (Apple = 50): ', value = 50))
        company = st.text_input('Entre com o nome da empresa a ser consultada: ')

    if option == "Ambos":
        fontes = ["Google", "Apple"]
    if option == "Google":
        fontes = ["Google"]
    if option == "Apple":
        fontes = ["Apple"]

    if company != "":
        company = company.lower()
        # Generating the dataframe with results collected
        for fonte in fontes:
            st.markdown(f"Inicializando o processo para a opção de fonte **{fonte}** e empresa **{company}**")
            if fonte == "Google":
                id = get_id(provider=fonte, company=company)
                print(f"Id Google: {id}")
                df_google = analise_aplicativo.coordena_processo(name_google=id, qtd = count)

            elif fonte == "Apple":
                results = get_id(provider=fonte, company=company)
                id = results[0]
                app_name = results[1]
                df_apple = analise_aplicativo.coordena_processo(name_apple=app_name, apple_id=id)
        
        if option == "Ambos":
            scraper = analise_aplicativo.Scraper()
            df_results = scraper.return_results(df_google, df_apple)
        if option == "Google":
            df_results = df_google
        if option == "Apple":
            df_results = df_apple

        # Creating a Dashboard with some initial insights about performance
        count_negative = int(
            df_results[(df_results["sentimento"] == "Negativo")]["sentimento"].count()
        )
        count_positive = int(
            df_results[(df_results["sentimento"] == "Positivo")]["sentimento"].count()
        )
        total_comment = int(
            len(df_results)
        )
        placeholder = st.empty()
        with placeholder.container():

            # create three columns
            kpi1, kpi2, kpi3 = st.columns(3)

            # fill in those three columns with respective metrics or KPIs
            kpi1.metric(
                label="Total de impressões",
                value=round(total_comment)
            )
            
            kpi2.metric(
                label="Impressões positivas",
                value=int(count_positive)
            )
            
            kpi3.metric(
                label="Impressões Negativas",
                value=count_negative
            )

            st.markdown("### Mapa de calor entre score e sentimento")
            fig = px.density_heatmap(
                data_frame=df_results, y="score", x="sentimento", color_continuous_scale="Agsunset"
            )
            st.write(fig)

            data = df_results.copy()
            data['at'] = data['at'].dt.date
            data = data.groupby(['at', 'sentimento']).size().rename("Count").reset_index()
            st.markdown("### Sentimento do usuário ao longo do tempo")
            fig2 = px.bar(data_frame=data, x="at",y="Count", color = "sentimento",barmode='group',
                          labels = {'at': 'Data', 'Count': 'Contagem'}, 
                          color_discrete_map = {"Negativo": "red", "Positivo": "green", "Neutro": "yellow"})
            st.write(fig2)

        # Creating a view with the raw data and download button
        csv = convert_df(df_results)

        st.download_button(
        "Download dos Resultados",
        csv,
        "file.csv",
        "text/csv",
        key='download-csv'
        )

        st.dataframe(df_results, hide_index=True)
    
        nlp = transformers_nlp.NLP(df_results)
        
        question = st.text_input('Realize uma pergunta sobre os dados observados: ')
        if question != "":
            answer = nlp.question_answering(question = question)
            st.text_area(label="Resposta:", value=answer, height=350)


        


