import streamlit as st
from openai import OpenAI
import pandas as pd

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("📋 Plan personnalisé pour arrêter ou réduire la consommation")

st.write("Répondez aux questions ci-dessous pour que l'IA vous propose un plan d'accompagnement personnalisé.")

# Collecte des informations de l'utilisateur
substance = st.text_input("Quelle(s) substance(s) consommez-vous ?")
frequency = st.selectbox("À quelle fréquence consommez-vous ?", ["Tous les jours", "Plusieurs fois par semaine", "Occasionnellement"])
motivation = st.text_area("Pourquoi voulez-vous arrêter ou réduire ? (Ex: santé, famille, travail...)")
difficulties = st.text_area("Quelles sont vos principales difficultés pour arrêter ou réduire ? (Ex: manque, stress, entourage...)")

if st.button("Générer mon plan personnalisé"):
    with st.spinner("Analyse de votre situation..."):
        user_input = f"""L'utilisateur consomme {substance} à une fréquence de {frequency}. 
        Il souhaite arrêter ou réduire parce que : {motivation}. 
        Les principales difficultés qu'il rencontre sont : {difficulties}. 
        Établis un plan progressif, avec des objectifs à court, moyen et long terme, des actions concrètes et des conseils pour gérer le manque et éviter les rechutes.
        Affiche le plan sous forme de tableau avec les colonnes : 'Objectif', 'Action', 'Conseils'."""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "Tu es un assistant spécialisé dans l'accompagnement des toxicomanes pour réduire ou arrêter leur consommation de drogue. Crée un plan progressif sous forme de tableau en fonction de la situation de l'utilisateur."},
                      {"role": "user", "content": user_input}]
        )

        # Extraction du tableau généré par l'IA
        plan_text = response.choices[0].message.content
        lines = plan_text.split("\n")
        table_data = [line.split("|")[1:-1] for line in lines if "|" in line]

        if len(table_data) > 1:
            df = pd.DataFrame(table_data[1:], columns=table_data[0])
            st.write("### 🛠️ Plan personnalisé d'arrêt ou de réduction")
            st.dataframe(df)
        else:
            st.warning("L'IA n'a pas pu générer un tableau structuré. Essayez de reformuler votre réponse.")

st.markdown("💡 **Conseil** : Vous pouvez imprimer ce plan ou l'enregistrer pour suivre vos progrès.")
