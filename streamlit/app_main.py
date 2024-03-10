from app_utils import (display_title_and_instructions, select_assets,
                       choose_prediction_type, model_selection,
                       prediction_horizon)


def main():
    display_title_and_instructions()
    if select_assets():
        choose_prediction_type()
        model_selection()
        prediction_horizon()


if __name__ == "__main__":
    main()
