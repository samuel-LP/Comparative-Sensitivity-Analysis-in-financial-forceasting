def display_return(ptf, name, ax):
    # Tracer les prédictions et les retours réels
    ax.plot(ptf.Date, ptf['Prediction'], label='Prediction', fillstyle='bottom')
    ax.plot(ptf.Date, ptf['Returns'], label='Return', fillstyle='bottom')

    # Mise à jour des titres et des légendes
    ax.set_title(f"Évolution des returns de {name}")
    ax.set_xlabel('Date')
    ax.set_ylabel('Valeur')
    ax.legend()


def display_evolution(ptf, name, ax):
    # Calculs pour les valeurs de portefeuille
    ptf['Real_Portfolio_Value'] = 1000 * (1 + ptf['Returns']).cumprod()
    ptf['Predicted_Portfolio_Value'] = 1000 * (1 + ptf['Prediction']).cumprod()

    # Tracer les valeurs réelles et prédites du portefeuille
    ax.plot(ptf.Date, ptf['Real_Portfolio_Value'], label='Valeur Réelle', fillstyle='bottom')
    ax.plot(ptf.Date, ptf['Predicted_Portfolio_Value'], label='Valeur Prédite', fillstyle='bottom')

    # Mise à jour des titres et des légendes
    ax.set_title(f"Évolution de la valeur de {name}")
    ax.set_xlabel('Date')
    ax.set_ylabel('Valeur')
    ax.legend()