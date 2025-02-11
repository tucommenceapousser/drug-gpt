import streamlit as st
from agent import generate_stream, generate_response
import openai  # Assurez-vous d'installer la bibliothèque OpenAI avec pip install openai

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

# Configuration de l'API OpenAI pour la génération d'images (assurez-vous d'avoir une clé API valide)
openai.api_key = "votre_clé_API_openai"

# Fonction pour générer une image via DALL-E
def generate_drug_image(drug_name):
    try:
        response = openai.Image.create(
            prompt=f"Illustration of {drug_name} drug, its appearance and effects, realistic, medical style",
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        return image_url
    except Exception as e:
        return None

# Menu de navigation
page = st.sidebar.radio("Navigation", ["Accueil", "Informations sur les drogues", "Questions & Réponses"])

# Page d'accueil
if page == "Accueil":
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

# Page "Informations sur les drogues"
elif page == "Informations sur les drogues":
    st.markdown("""
        ## Informations sur les drogues et leurs risques
        
        La consommation de certaines drogues comporte des risques importants pour la santé physique et mentale. Cette section vous fournira des informations de base sur les drogues les plus courantes, les mécanismes d'action et les dangers associés à leur utilisation.

        ### 1. Héroïne (Opioïdes)
        L'héroïne est un opiacé très addictif qui agit sur le système nerveux central. Elle procure un sentiment intense de bien-être, mais entraîne rapidement une dépendance physique et psychologique.
        
        **Risques :**
        - **Surdose :** L'un des risques les plus graves de l'héroïne est la surdose, pouvant entraîner la mort par dépression respiratoire.
        - **Dépendance :** La dépendance à l'héroïne se développe rapidement et nécessite souvent un traitement médical pour être surmontée.
        - **Problèmes respiratoires :** La consommation régulière peut entraîner des problèmes respiratoires graves, y compris des infections pulmonaires.
        
        **Réduction des risques :**
        - Ne jamais consommer seul.
        - Utiliser des seringues propres pour éviter les infections.
        - Accéder à des programmes de substitution avec des opioïdes plus sûrs sous surveillance médicale.

        ### 2. Cannabis
        Le cannabis est une drogue psychoactive couramment utilisée, souvent consommée sous forme de joints ou de concentrés. Bien qu'il soit légal dans certains endroits, il reste illégal dans d'autres et comporte des risques pour la santé.
        
        **Risques :**
        - **Problèmes de mémoire et de concentration :** Une consommation excessive peut nuire à la mémoire à court terme et à la capacité de concentration.
        - **Santé mentale :** L'usage intensif de cannabis peut augmenter le risque de troubles mentaux, y compris la psychose et l'anxiété.
        - **Dépendance :** Bien que moins addictive que d'autres drogues, le cannabis peut conduire à une dépendance psychologique chez certaines personnes.

        **Réduction des risques :**
        - Limiter la consommation, en particulier chez les jeunes et les personnes ayant des antécédents familiaux de troubles mentaux.
        - Éviter de conduire ou d'effectuer des tâches nécessitant de la concentration sous l'influence du cannabis.

        ### 3. Cocaïne
        La cocaïne est un stimulant puissant qui affecte le système nerveux central. Elle procure un sentiment d'euphorie intense, mais comporte des risques considérables.
        
        **Risques :**
        - **Problèmes cardiovasculaires :** La cocaïne peut entraîner une augmentation de la fréquence cardiaque, de la pression artérielle et peut provoquer des crises cardiaques.
        - **Comportements impulsifs :** La consommation de cocaïne peut provoquer des comportements impulsifs et violents.
        - **Dépendance :** Elle entraîne rapidement une dépendance psychologique, avec des symptômes de sevrage sévères.

        **Réduction des risques :**
        - Ne jamais mélanger la cocaïne avec de l'alcool ou d'autres substances.
        - Utiliser un soutien professionnel pour sevrer et traiter la dépendance.

    """)

    # Générer une image pour l'héroïne (par exemple)
    if st.button("Afficher l'image de l'héroïne"):
        image_url = generate_drug_image("heroin")
        if image_url:
            st.image(image_url, caption="Illustration de l'héroïne", use_column_width=True)
        else:
            st.error("Erreur lors de la génération de l'image.")

    # Ajouter un autre bouton pour générer l'image du cannabis ou d'autres drogues
    if st.button("Afficher l'image du cannabis"):
        image_url = generate_drug_image("cannabis")
        if image_url:
            st.image(image_url, caption="Illustration du cannabis", use_column_width=True)
        else:
            st.error("Erreur lors de la génération de l'image.")

# Page "Questions & Réponses" (Q&A)
elif page == "Questions & Réponses":
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
