from app_utils import (display_title_and_instructions, select_assets,
                       choose_prediction_type, model_selection,
                       prediction_horizon, send_request_to_api)
import streamlit as st

if 'actifs' not in st.session_state:
    st.session_state['actifs'] = ["Apple"]
if "modele" not in st.session_state:
    st.session_state['modele'] = "LSTM"
if "prediction" not in st.session_state:
    st.session_state['prediction'] = "volatilité"
if "horizon" not in st.session_state:
    st.session_state['horizon'] = 1


def main():
    display_title_and_instructions()
    if select_assets():
        choose_prediction_type()
        model_selection()
        prediction_horizon()
        send_request_to_api()


if __name__ == "__main__":
    main()
