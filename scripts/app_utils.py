import pandas as pd
import streamlit as st
import yfinance as yf
import os
import requests
import plotly.graph_objects as go

import json

def display_title_and_instructions():
    """
    Display title and instructions for the stock market prediction application.
    """
    st.title("Bienvenue sur Stock Prediction !")
    st.markdown("#### Cette application a pour objectif de vous permettre d'estimer "
             "l'évolution de votre portefeuille d'actifs."
             "Pour vous permettre de voir vos prédictions, "
             "nous avons besoin des informations suivantes : \n")


def select_assets():
    """
    Function to select assets and download their data if necessary.

    Returns:
    bool: True if assets are selected, False otherwise.
    """
    st.markdown("\n \n")
    st.markdown("##### Choix des Actifs :")
    actif_interne = st.multiselect("Veuillez choisir un ou plusieurs actif(s)",
                                   ["AMZN", "GOOG",
                                    "MSFT", "XOM"])
    actif_externe = st.text_input("Si vous voulez rajouter un actif, "
                                  "veuillez préciser son ticker : ")

    if actif_interne or actif_externe:
        selected_assets = ', '.join(actif_interne)
        if actif_externe:
            if selected_assets:
                selected_assets += ', '
            selected_assets += actif_externe
            if not os.path.exists('data'):
                os.makedirs('data')

            data = yf.download(actif_externe,
                               start="2020-01-02",
                               end="2023-12-29")
            data.reset_index(inplace=True)
            if data.shape[0] > 0:
                data.to_csv(f"data/{actif_externe}.csv")
                st.write(f"Données téléchargées pour {actif_externe} :")
                st.dataframe(data.tail())
            else:
                st.write("Données non disponibles pour"
                         "cet actif, avez vous fait une faute?")

        st.write(
            f"Vous avez sélectionné les actifs suivants : {selected_assets}")
        print(list(selected_assets.split(",")))
        st.session_state['actifs'] = list(selected_assets.split(","))
        return selected_assets
    return False


def choose_prediction_type():
    """
    Function for choosing the type of prediction. It displays a message asking
    the user to choose between predicting volatility or price.
    It then creates buttons for each choice and updates the session state
    based on the user's selection.
    """
    st.markdown("\n \n")
    st.markdown("##### Choix de la Cible :")

    prediction_choice = st.radio("Voulez-vous prédire la volatilité ou le prix ?",
                                 ('Prix', 'Volatilité'))

    # Mettre à jour st.session_state basé sur le choix
    if prediction_choice == 'Prix':
        st.session_state['prediction'] = 'Value'
    elif prediction_choice == 'Volatilité':
        st.session_state['prediction'] = 'Volatility'


def model_selection():
    """
    Function for model selection in the application. It handles the user's
    selection of prediction type and model type using Streamlit buttons.
    """
    if 'prediction' in st.session_state:
        if st.session_state['prediction'] == 'Value':
            st.write("Vous avez sélectionné le prix")
        if  st.session_state['prediction'] == 'Volatility':
            st.write("Vous avez sélectionné la volatilité")

        st.markdown("\n \n")
        st.markdown("##### Choix du Modèle :")

        model_choice = st.radio("Quel modèle voulez vous utiliser ?",
                                     ('XGBoost', 'LSTM'))

        # Mettre à jour st.session_state basé sur le choix
        if model_choice == 'XGBoost':
            st.session_state['modele'] = 'XGB'
        else :
            st.session_state['modele'] = 'LSTM'


def prediction_horizon():
    """
    This function checks if a model is present in the session state, and if so,
    it writes a message about the selected model and prompts the user
    to select a prediction horizon.
    """

    if 'modele' in st.session_state:
        modele = st.session_state['modele']
        st.write(f"Vous avez sélectionné un modèle {modele}, excellent choix!")

        st.markdown("\n \n")
        st.markdown("##### Choix de l'Horizon de Prédiction :")


        option = st.select_slider("Veuillez maintenant sélectionner un horizon de prédiction",
                                  options=['1 jour', '7 jours',
                                           '14 jours', "28 jours"],
                                  key=f'horizon_{modele}')

        if option == '1 jour':
            st.session_state['horizon'] = 1
        elif option == '7 jours':
            st.session_state['horizon'] = 7
        elif option == '14 jours':
            st.session_state['horizon'] = 14
        elif option == '28 jours':
            st.session_state['horizon'] = 28

def plot_predictions(container, predictions, selected_value):
    if st.session_state["prediction"] == "Value" :
        value = pd.DataFrame(json.loads(predictions[selected_value]))
        value['Date'] = pd.to_datetime(value['Date'], unit='ms')

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=value['Date'], y=value['Close'], mode='lines', name='réel'))
        fig.add_trace(go.Scatter(x=value['Date'], y=value['Prediction'], mode='lines', name='prédit'))
        fig.update_layout(title=f"Évolution de la valeur de {selected_value}",
                          xaxis_title='Date',
                          yaxis_title='Valeur')

        container.plotly_chart(fig)
    else :
        value = pd.DataFrame(json.loads(predictions[selected_value]))
        value['Date'] = pd.to_datetime(value['Date'], unit='ms')

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=value['Date'], y=value['Volatility'], mode='lines', name='réel'))
        fig.add_trace(go.Scatter(x=value['Date'], y=value['Prediction'], mode='lines', name='prédit'))
        fig.update_layout(title=f"Évolution de la valeur de {selected_value}",
                          xaxis_title='Date',
                          yaxis_title='Valeur')

        container.plotly_chart(fig)


def plot_ptf(container, ptf):
    if st.session_state["prediction"] == "Value" :
        ptf_avg = pd.DataFrame(json.loads(ptf))
        ptf_avg['Date'] = pd.to_datetime(ptf_avg['Date'], unit='ms')

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=ptf_avg['Date'], y=ptf_avg['Predicted_Portfolio_Value'], mode='lines', name='Predicted'))
        fig.add_trace(go.Scatter(x=ptf_avg['Date'],
                                 y=ptf_avg['Predicted_Portfolio_Value'],
                                 mode='lines',
                                 fill='tozeroy',
                                 opacity=0.3,
                                 showlegend=False))

        fig.add_trace(go.Scatter(x=ptf_avg['Date'], y=ptf_avg['Real_Portfolio_Value'], mode='lines', name='Real'))
        fig.add_trace(go.Scatter(x=ptf_avg['Date'],
                                 y=ptf_avg['Real_Portfolio_Value'],
                                 mode='lines',
                                 fill='tozeroy',
                                 opacity=0.3,
                                 showlegend=False))

        fig.update_layout(title=f"Évolution de la valeur du portefeuille",
                          xaxis_title='Date',
                          yaxis_title='Valeur')

        container.plotly_chart(fig)
    else :
        ptf_avg = pd.DataFrame(json.loads(ptf))
        ptf_avg['Date'] = pd.to_datetime(ptf_avg['Date'], unit='ms')

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=ptf_avg['Date'], y=ptf_avg['Prediction'], mode='lines', name='Predicted'))
        fig.add_trace(go.Scatter(x=ptf_avg['Date'],
                                 y=ptf_avg['Prediction'],
                                 mode='lines',
                                 fill='tozeroy',
                                 opacity=0.3,
                                 showlegend=False))

        fig.add_trace(go.Scatter(x=ptf_avg['Date'], y=ptf_avg['Volatility'], mode='lines', name='Real'))
        fig.add_trace(go.Scatter(x=ptf_avg['Date'],
                                 y=ptf_avg['Volatility'],
                                 mode='lines',
                                 fill='tozeroy',
                                 opacity=0.3,
                                 showlegend=False))

        fig.update_layout(title=f"Évolution de la valeur du portefeuille",
                          xaxis_title='Date',
                          yaxis_title='Valeur')

        container.plotly_chart(fig)


def send_request_to_api():
        data = {
            "tickers": st.session_state['actifs'],
            "model": st.session_state['modele'],
            "target": st.session_state['prediction'],
            "horizon": st.session_state['horizon']
        }

        response = None
        try:
            response = requests.post(
                url="http://127.0.0.1:8000/prediction/",
                json=data
            )
            if response.status_code == 200:
                response_data = response.json()

                predictions = response_data["predictions"]
                portfolio = response_data["portfolio"]
                error = response_data["error"]

                return(predictions, portfolio, error)



        except Exception as e:
            st.error(f"Erreur lors de l'envoi de la requête : {e}")
            if response is not None:
                st.error(f"Détails de l'erreur : Statut HTTP: {response.status_code}, Réponse: {response.text}")


