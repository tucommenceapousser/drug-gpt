import streamlit as st
from agent import generate_stream, generate_response

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Trkn-Drug-GPT",
    page_icon="💊",
    menu_items={
        'About': "This app is a prototype made for demo purposes to provide harm reduction advice and drug information. "
                 "It is not intended for real-life use. Please consult a medical professional for advice."
    }
)

# 🎨 Injection de CSS pour un design "hacker" fluo
st.markdown("""
    <style>
    /* Fond général */
    .stApp {
        background-color: #0E0E0E;
        color: white;
    }

    /* Titres */
    h1, h2, h3 {
        color: #00FFAA;
        text-shadow: 2px 2px 8px #00FFAA;
        text-align: center;
    }

    /* Texte standard */
    p, ul, li {
        color: #D3D3D3;
        font-size: 16px;
    }

    /* Sidebar (navigation) */
    .css-1d391kg {
        background-color: #161616 !important;
        border-right: 3px solid #00FFAA;
    }

    /* Boutons */
    .stButton>button {
        background-color: #00FFAA;
        color: black;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #FF0044;
        color: white;
        border: 2px solid white;
    }

    /* Chat Messages */
    .stChatMessage {
        background-color: #1A1A1A;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 0px 10px #00FFAA;
    }

    /* Images */
    img {
        border: 3px solid #00FFAA;
        border-radius: 5px;
    }

    /* Input Chat */
    .stChatInput {
        background-color: #1E1E1E;
        color: white;
        border: 2px solid #00FFAA;
    }

    </style>
""", unsafe_allow_html=True)

st.title("💊 Drug-GPT - Harm Reduction Assistant")

# Menu de navigation stylisé
page = st.sidebar.radio("📜 Navigation", ["🏠 Accueil", "💊 Informations sur les drogues", "❓ Questions & Réponses"])

# Page d'accueil
if page == "🏠 Accueil":
    st.markdown("""
        ## 🏠 Contexte de l'application
        Bienvenue sur **Drug-GPT**, un assistant virtuel conçu pour fournir des **informations fiables** sur les drogues et aider à **réduire les risques** liés à leur consommation.  
        
        🚀 **Ce que vous trouverez ici** :
        - 🔬 **Détails sur les substances** : Effets, mécanismes d'action, dangers.
        - 🛡️ **Stratégies de réduction des risques** : Conseils pratiques.
        - 🏥 **Aide pour la dépendance** : Ressources et accompagnement.

        ⚠️ **Note :** Cette application est une **démonstration**. Pour toute question de santé, consultez un **professionnel**.
    """)

# Page "Informations sur les drogues"
elif page == "💊 Informations sur les drogues":
    st.markdown("## 💊 Informations sur les drogues et leurs risques")

    ### **Héroïne**
    st.markdown("### 1️⃣ Héroïne (Opioïdes)")
    st.image("images/heroine.jpg", caption="💉 Poudre d'héroïne", width=300)
    st.markdown("""
        **Description :**  
        Un puissant opiacé provoquant une sensation d'euphorie intense, mais extrêmement addictif.  

        🛑 **Risques :**  
        - Surdose fatale (dépression respiratoire).  
        - Forte dépendance.  
        - Transmission de maladies (injections contaminées).  

        ✅ **Réduction des risques :**  
        - Toujours avoir du **Naloxone** à disposition.  
        - **Ne jamais consommer seul**.  
    """)

    ### **Cannabis**
    st.markdown("### 2️⃣ Cannabis")
    st.image("images/cannabis.jpeg", caption="🌿 Fleurs de cannabis", width=300)
    st.markdown("""
        **Description :**  
        Psychoactif naturel souvent fumé sous forme de joints ou vaporisé.  

        🛑 **Risques :**  
        - Dépendance psychologique.  
        - Troubles de la mémoire.  
        - Psychose chez certains consommateurs.  

        ✅ **Réduction des risques :**  
        - **Espacer les prises** pour éviter l'accoutumance.  
        - **Éviter les mélanges avec alcool**.  
    """)

    ### **Cocaïne**
    st.markdown("### 3️⃣ Cocaïne")
    st.image("images/cocaine.jpg", caption="❄️ Poudre de cocaïne", width=300)
    st.markdown("""
        **Description :**  
        Stimulant rapide et euphorisant, mais très addictif.  

        🛑 **Risques :**  
        - Crises cardiaques.  
        - Paranoïa et troubles du comportement.  
        - Forte dépendance.  

        ✅ **Réduction des risques :**  
        - **Ne jamais mélanger avec de l'alcool**.  
        - **Tester avant consommation** (fentanyl, contaminants).  
    """)

# Page "Questions & Réponses" (Q&A)
elif page == "❓ Questions & Réponses":
    if "messages" not in st.session_state:
        st.session_state.messages = []
        response = generate_response(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": response})

    for message in st.session_state.messages:
        if message["role"] == "assistant":
            with st.chat_message(name="assistant", avatar="😈"):
                st.markdown(message["content"])
        else:
            with st.chat_message(message["role"]):
                st.write(message["content"])

    if prompt := st.chat_input("Posez une question à Drug-GPT..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message(name="assistant", avatar="😈"):
            stream = generate_stream(st.session_state.messages)
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
