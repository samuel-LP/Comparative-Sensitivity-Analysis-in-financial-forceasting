import streamlit as st


def display_title_and_instructions():
    """
    Display title and instructions for the stock market prediction application.
    """
    st.title("Bienvenue stock market prediction !")
    st.write("Cette application a pour objectif de vous permettre d'estimer "
             "l'évolution de votre portefeuille d'actifs. \n"
             "Pour vous permettre de voir vos prédictions, "
             "nous avons besoin des informations suivantes : \n")


def select_assets():
    """
    A function that allows the user to select assets and returns
    True if any assets are selected, otherwise False.
    """
    actif_interne = st.multiselect(
        "Veuillez choisir un ou plusieurs actif(s) \n",
        ["Apple", "Amazon", "Google",
         "Microsoft", "Exxon"])
    actif_externe = st.text_input("Si aucun actif ne vous correspond, "
                                  "veuillez préciser votre actif ici: ")
    if actif_interne or actif_externe:
        selected_assets = ', '.join(actif_interne)
        if actif_externe:
            if selected_assets:
                selected_assets += ', '
            selected_assets += actif_externe

        st.write(
            f"Vous avez sélectionné les actifs suivants : {selected_assets}")
        return True
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
