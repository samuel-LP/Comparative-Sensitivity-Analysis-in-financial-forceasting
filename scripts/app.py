import time

from app_utils import *

import streamlit as st

if "horizon" not in st.session_state:
   st.session_state['horizon'] = None

with open('./static/style.css') as f:
   st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    display_title_and_instructions()
    select_assets()
    choose_prediction_type()
    model_selection()
    prediction_horizon()


    if st.session_state['horizon'] is not None:
        if st.button("Voir les prévisions") or 'predictions' in st.session_state:

            with st.spinner('Prédiction en cours ...'):
                if 'predictions' not in st.session_state:
                    preds, ptf, errors = send_request_to_api()
                    st.session_state['predictions'] = preds
                    st.session_state["ptf"] = ptf
                    st.session_state['errors'] = errors
                else:
                    preds = st.session_state['predictions']
                    ptf = st.session_state["ptf"]
                    errors = st.session_state['errors']

            st.success("Prédiction réussie !")
            st.markdown("\n")
            st.markdown("#### Visualisations des Résultats : ")
            st.markdown("##### Prédiction de la valeur de votre Portefeuille : ")
            plot_container_ptf = st.empty()
            plot_ptf(plot_container_ptf, ptf)

            st.markdown("\n")
            st.markdown("##### Prédiction des titres de votre Portefeuille : ")
            selected_value = st.selectbox("Sélectionner une valeur", list(preds.keys()))
            plot_container = st.empty()
            plot_predictions(plot_container, preds, selected_value)

            st.markdown("\n")
            st.markdown("##### Métriques d'erreurs de prédiction : ")
            table_container = st.empty()
            errors = pd.DataFrame(json.loads(errors))
            table_container.dataframe(errors)


if __name__ == "__main__":
    main()