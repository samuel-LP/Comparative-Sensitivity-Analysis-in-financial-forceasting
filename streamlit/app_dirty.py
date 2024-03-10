import streamlit as st

st.title("Bienvenue stock market prediction !")

st.write("Cette application a pour objectif de vous permettre d'estimer "
         "l'évolution de votre portefeuille d'actifs. \n"
         "Pour vous permettre de voir vos prédictions, "
         "nous avons besoin des informations suivantes : \n")

actif_interne = st.multiselect("Veuillez choisir un ou plusieurs actif(s) \n",
                               ["Apple", "Amazon", "Google", "Microsoft", "Exxon"])

actif_externe = st.text_input("Si aucun actif ne vous correspond, "
                              "veuillez préciser votre actif ici: ")

if actif_externe or actif_interne:
    st.write("Vous avez sélectionné les actifs suivants :")
    for actif in actif_interne + [actif_externe]:
        st.write(actif)

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

    if 'prediction' in st.session_state:
        if st.session_state['prediction'] == 'prix':
            st.write("Vous avez sélectionné le prix")

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

        elif st.session_state['prediction'] == 'volatilité':
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

        if 'modele' in st.session_state:
            if st.session_state['modele'] == 'XGBoost':

                st.write("Vous avez sélectionné un modèle XGBoost, excellent choix!")
                st.write("Veuillez maintenant sélectionner un horizon de prédiction")

                option = st.radio("",
                                  ('1 jour', '7 jours', '14 jours', "28 jours"),
                                  key='horizon_xgboost')
                
                j1_col, j7_col, j14_col, j28_col = st.columns(4)

            with j1_col:
                j1_btn = st.radio('1 jour', key='1j')

            with j7_col:
                j7_btn = st.button('7 jours', key='7j')

            with j14_col:
                j14_btn = st.button('14 jours', key='14j')
            
            with j28_col:
                j28_btn = st.button('28 jours', key='28j')

        elif st.session_state['modele'] == 'LSTM':

            st.write("Vous avez sélectionné un modèle LSTM, excellent choix!")
            st.write("Veuillez maintenant sélectionner un horizon de prédiction")

            option = st.radio("",
                                ('1 jour', '7 jours', '14 jours', "28 jours"),
                                key='horizon_lstm')
