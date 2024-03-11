import streamlit as st
import yfinance as yf
import os
import requests
import json


def display_title_and_instructions():
    """
    Display title and instructions for the stock market prediction application.
    """
    st.title("Bienvenue sur stock market prediction !")
    st.write("Cette application a pour objectif de vous permettre d'estimer "
             "l'évolution de votre portefeuille d'actifs. \n"
             "Pour vous permettre de voir vos prédictions, "
             "nous avons besoin des informations suivantes : \n")


def select_assets():
    """
    Function to select assets and download their data if necessary.

    Returns:
    bool: True if assets are selected, False otherwise.
    """
    actif_interne = st.multiselect("Veuillez choisir un ou plusieurs actif(s)",
                                   ["Apple", "Amazon", "Google",
                                    "Microsoft", "Exxon"])
    actif_externe = st.text_input("Si vous voulez rajouter un actif, "
                                  "veuillez préciser son symbole boursier : ")

    if actif_interne or actif_externe:
        selected_assets = ', '.join(actif_interne)
        if actif_externe:
            if selected_assets:
                selected_assets += ', '
            selected_assets += actif_externe
            if not os.path.exists('data'):
                os.makedirs('data')

            data = yf.download(actif_externe,
                               start="2013-01-02",
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
        return selected_assets
    return False


def choose_prediction_type():
    """
    Function for choosing the type of prediction. It displays a message asking
    the user to choose between predicting volatility or price.
    It then creates buttons for each choice and updates the session state
    based on the user's selection.
    """

    st.write("Voulez-vous prédire la volatilité ou le prix ?")
    prix_col, volatilite_col = st.columns(2)
    with prix_col:
        prix_btn = st.button('Prix', key='prix')
    with volatilite_col:
        vol_btn = st.button('Volatilité', key='volatilite')
    if prix_btn:
        st.session_state['prediction'] = 'prix'
    if vol_btn:
        st.session_state['prediction'] = 'volatilité'


def model_selection():
    """
    Function for model selection in the application. It handles the user's
    selection of prediction type and model type using Streamlit buttons.
    """
    if 'prediction' in st.session_state:
        if st.session_state['prediction'] == 'prix':
            st.write("Vous avez sélectionné le prix")
        else:
            st.write("Vous avez sélectionné la volatilité")
        st.write("Quel modèle de prédiction voulez-vous utiliser?")
        xgb_col, lstm_col = st.columns(2)
        with xgb_col:
            xgb_btn = st.button('XGBoost', key='xgb')
        with lstm_col:
            lstm_btn = st.button('LSTM', key='lstm')
        if xgb_btn:
            st.session_state['modele'] = 'XGBoost'
        elif lstm_btn:
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
        st.write("Veuillez maintenant sélectionner un horizon de prédiction")
        option = st.select_slider("",
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


def send_request_to_api():
    # Bouton pour lancer la prédiction
    if st.button("Voir les prévisions"):
        data = {
            "tickers": st.session_state['actifs'],
            "model": st.session_state['modele'],
            "target": st.session_state['prediction'],
            "horizon": st.session_state['horizon']
        }

        response = None  # Initialiser la variable de réponse
        try:
            response = requests.post(
                url="http://127.0.0.1:8000/predict/",
                json=data
            )
            if response.status_code == 200:
                predictions = response.json()
                st.write(predictions)  # Simple affichage des prédictions
            else:
                # Affichage d'une erreur avec plus de détails si la réponse n'est pas 200 OK
                st.error(f"Erreur lors de la récupération des prévisions. Statut HTTP: {response.status_code}, Réponse: {response.text}")
        except Exception as e:
            st.error(f"Erreur lors de l'envoi de la requête : {e}")
            # Affichez des détails sur la réponse si disponible
            if response is not None:
                st.error(f"Détails de l'erreur : Statut HTTP: {response.status_code}, Réponse: {response.text}")
