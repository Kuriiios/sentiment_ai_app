# frontend/pages/0_insérer.py
import streamlit as st
import requests 
import os 
import pandas as pd
from dotenv import load_dotenv 

load_dotenv()

API_ROOT_URL =  f"http://{os.getenv('API_BASE_URL')}:{os.getenv('FAST_API_PORT', '8080')}"
API_AI_ROOT_URL =  f"http://{os.getenv('API_AI_BASE_URL')}:{os.getenv('FAST_API_AI_PORT', '8080')}"
API_URL =  API_ROOT_URL + "/read"

st.title("Read a quote")

mode = st.radio("Choose the search mode: ", ("random", "by id", 'by id mine'))


match mode:
    case "random":
        st.subheader("Random quote")
        API_URL = (API_ROOT_URL+ "/read/random/")
        if st.button('Get random quote'):
            try : 
                response = requests.get(API_URL)

                if response.status_code == 200:
                    st.session_state['api_result'] = response.json()
                    result = response.json()
                    st.success(f"Citation avec ID {result.get('id', 'N/A')}")

                    st.info(result.get('text', 'text non trouvé'))
                    st.balloons()
                else:
                    st.error(f"Erreur de l'API avec le code {response.status_code}")


            except requests.exceptions.ConnectionError:
                st.error(f"ERREUR : Impossible de se connecter à l'API à {API_URL}")
                st.warning("Veuillez vous assurer que le serveur Uvicorn est bien lancé en arrière-plan.")

    case "by id":
        st.subheader("Quote by id")
        with st.form('search id: '):
            quote_id = st.number_input("Enter id of quote", min_value=1, step=1)
            submitted = st.form_submit_button('submit')
            if submitted:
                API_URL = (API_ROOT_URL+ f"/read/{quote_id}")
                try : 
                    response = requests.get(API_URL)

                    if response.status_code == 200:
                        st.session_state['api_result'] = response.json()
                        result = response.json()

                        st.success(f"Citation avec ID {result.get('id', 'N/A')}")
                        st.info(result.get('text', 'text non trouvé'))
                        st.balloons()
                    else:
                        st.error(f"Erreur de l'API avec le code {response.status_code}")


                except requests.exceptions.ConnectionError:
                    st.error(f"ERREUR : Impossible de se connecter à l'API à {API_URL}")
                    st.warning("Veuillez vous assurer que le serveur Uvicorn est bien lancé en arrière-plan.")

    case "by id mine":
        st.subheader("Quote by id")
        API_URL =  API_ROOT_URL + "/read_ids"
        try : 
            response = requests.get(API_URL)

            if response.status_code == 200:
                result = response.json()
                df = pd.DataFrame(result)
                id = st.selectbox('choose id', df)
                API_URL = (API_ROOT_URL+ f"/read/{id}")
                try : 
                    response = requests.get(API_URL)

                    if response.status_code == 200:
                        st.session_state['api_result'] = response.json()
                        result = response.json()

                        st.success(f"Citation avec ID {result.get('id', 'N/A')}")
                        st.info(result.get('text', 'text non trouvé'))
                        st.balloons()
                    else:
                        st.error(f"Erreur de l'API avec le code {response.status_code}")

                except requests.exceptions.ConnectionError:
                    st.error(f"ERREUR : Impossible de se connecter à l'API à {API_URL}")
                    st.warning("Veuillez vous assurer que le serveur Uvicorn est bien lancé en arrière-plan.")
            else:
                st.error(f"Erreur de l'API avec le code {response.status_code}")

        except requests.exceptions.ConnectionError:
            st.error(f"ERREUR : Impossible de se connecter à l'API à {API_URL}")
            st.warning("Veuillez vous assurer que le serveur Uvicorn est bien lancé en arrière-plan.")
            
analyse = st.button('Analyse')

if analyse:
    result_quote = st.session_state['api_result'] 
    API_AI_URL = API_AI_ROOT_URL + '/analyse_sentiment/'

    to_analyse = {'text':result_quote.get('text', 'text non trouvé')}

    response = requests.post(url=API_AI_URL, json=to_analyse)
    if response.status_code == 200:
        result = response.json()
        st.success(f"Quote with ID {result_quote.get('id', 'N/A')} has been analyze and it's sentiment is :")
        st.info(result.get('neg', 'text non trouvé'))
        st.info(result.get('neu', 'text non trouvé'))
        st.info(result.get('pos', 'text non trouvé'))
        st.info(result.get('compound', 'text non trouvé'))