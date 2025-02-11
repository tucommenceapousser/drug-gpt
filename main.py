import streamlit as st
from agent import generate_stream, generate_response

# Configure l'application Streamlit
st.set_page_config(
    page_title="Trkn-Drug-GPT",
    page_icon="💊",
    menu_items={
        'About': "This app is a prototype made for demo purposes to provide harm reduction advice and drug information. "
                 "It is not intended for real-life use. Please consult a medical professional for advice."
    }
)
st.title("Drug-GPT - Harm Reduction Assistant")

# Introduction avec plus de contexte
st.markdown("""
    ## Contexte de l'application
    Bienvenue sur Drug-GPT, un assistant virtuel conçu pour fournir des informations fiables sur les drogues et aider les consommateurs de drogues à comprendre les risques associés à la consommation de substances comme l'héroïne et le cannabis. 
    Cette application vise à fournir des stratégies de réduction des risques, des informations sur les mécanismes d'action des substances, et des conseils pour aider les utilisateurs à prendre des décisions éclairées concernant leur consommation.
    
    ### Que pouvez-vous attendre de cet assistant ?
    - **Informations détaillées sur les substances :** classes de drogues, mécanisme d'action, efficacité et informations sur les effets secondaires.
    - **Conseils de réduction des risques :** stratégies pour minimiser les risques associés à la consommation de drogues.
    - **Aide pour la gestion de la dépendance :** suggestions sur la gestion des dépendances et conseils sur la manière d'obtenir de l'aide.
    
    **Note importante :** Cette application est une démonstration. Si vous ou quelqu'un que vous connaissez avez besoin d'aide, veuillez consulter un professionnel de la santé.
""")

# Initialisation de l'historique des messages
if "messages" not in st.session_state:
    st.session_state.messages = []
    response = generate_response(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Affichage des messages dans le chat
for message in st.session_state.messages:
    if message["role"] == "assistant":     
        with st.chat_message(name="assistant", avatar="😈"):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Entrée utilisateur pour une nouvelle question
if prompt := st.chat_input("Posez une question à Drug-GPT..."):
    # Ajouter le message de l'utilisateur à l'historique
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Afficher le message de l'utilisateur
    with st.chat_message("user"):
        st.markdown(prompt)

    # Réponse de l'assistant
    with st.chat_message(name="assistant", avatar="😈"):
        stream = generate_stream(st.session_state.messages)
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
