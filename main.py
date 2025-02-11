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
st.title("Drug-GPT - Harm Reduction Assistant")

# Menu de navigation (ajout de "Plan d'Arrêt")
page = st.sidebar.radio("Navigation", ["Accueil", "Informations sur les drogues", "Questions & Réponses", "Plan d'Arrêt"])

# Page d'accueil
if page == "Accueil":
    st.markdown("""
        ## Contexte de l'application
        Bienvenue sur Drug-GPT, un assistant virtuel conçu pour fournir des informations fiables sur les drogues et aider les consommateurs à comprendre les risques associés à la consommation de substances comme l'héroïne, le cannabis et la cocaïne.  
        
        Cette application vise à fournir des stratégies de réduction des risques, des informations sur les mécanismes d'action des substances et des conseils pour aider les utilisateurs à prendre des décisions éclairées.  

        ### Que pouvez-vous attendre de cet assistant ?
        - **Informations détaillées sur les substances** : mécanismes d'action, effets et risques.
        - **Conseils de réduction des risques** : stratégies pour minimiser les dangers liés à la consommation.
        - **Aide pour la gestion de la dépendance** : ressources et conseils pour obtenir de l'aide.  

        **Note importante :** Cette application est une démonstration. Pour toute question de santé, consultez un professionnel.
    """)

# Page "Informations sur les drogues"
elif page == "Informations sur les drogues":
    st.markdown("## Informations sur les drogues et leurs risques")

    ### **Héroïne**
    st.markdown("### 1. Héroïne (Opioïdes)")
    st.image("images/heroine.jpg", caption="Poudre d'héroïne", width=300)  # Image locale ou URL
    st.markdown("""
        L'héroïne est un opiacé très addictif qui agit sur le système nerveux central.  

        **Risques :**  
        - Surdose pouvant entraîner une dépression respiratoire fatale.  
        - Forte dépendance physique et psychologique.  
        - Infections et maladies transmissibles (si injection avec du matériel contaminé).  

        **Réduction des risques :**  
        - Ne jamais consommer seul.  
        - Utiliser des seringues propres pour éviter les infections.  
        - Accéder à des programmes de substitution (méthadone, buprénorphine).  
    """)

    ### **Cannabis**
    st.markdown("### 2. Cannabis")
    st.image("images/cannabis.jpeg", caption="Fleurs de cannabis", width=300)  # Image locale ou URL
    st.markdown("""
        Le cannabis est une drogue psychoactive couramment utilisée, souvent sous forme de joints ou d'huiles.  

        **Risques :**  
        - Troubles de la mémoire et de la concentration.  
        - Risque accru de psychose chez certaines personnes sensibles.  
        - Dépendance psychologique chez certains consommateurs réguliers.  

        **Réduction des risques :**  
        - Éviter de fumer avant d'effectuer des tâches nécessitant de la concentration (conduite, travail).  
        - Limiter la fréquence d'utilisation, surtout chez les jeunes.  
    """)

    ### **Cocaïne**
    st.markdown("### 3. Cocaïne")
    st.image("images/cocaine.jpg", caption="Poudre de cocaïne", width=300)  # Image locale ou URL
    st.markdown("""
        La cocaïne est un stimulant qui procure une euphorie intense, mais présente de nombreux risques.  

        **Risques :**  
        - Problèmes cardiovasculaires (hypertension, crises cardiaques).  
        - Forte dépendance psychologique.  
        - Comportements impulsifs et agressifs.  

        **Réduction des risques :**  
        - Ne jamais mélanger la cocaïne avec de l'alcool ou d'autres drogues.  
        - S'informer sur la composition pour éviter des produits coupés avec des substances dangereuses.  
    """)

# Page "Questions & Réponses" (Q&A)
elif page == "Questions & Réponses":
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

# Ajout de la page "Plan d'Arrêt"
elif page == "Plan d'Arrêt":
    import plan  # Importer plan.py pour l'afficher
