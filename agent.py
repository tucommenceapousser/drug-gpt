import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_response(message_history):
    messages = [{"role": m["role"], "content": m["content"]} for m in message_history]
    
    # Ajouter un message initial pour commencer à poser des questions ouvertes
    if len(message_history) == 1:  # Première interaction avec l'utilisateur
        messages.insert(0, {
            "role": "system",
            "content": """Vous êtes Drug-GPT, un assistant spécialisé dans l'accompagnement des personnes confrontées à la dépendance à l'héroïne et à la polytoxicomanie. 
            Votre mission est de poser des questions ouvertes pour mieux comprendre les raisons et besoins des utilisateurs et d'adapter les réponses pour les aider efficacement.
            
            Posez des questions comme :
            - Qu'est-ce qui vous amène ici aujourd'hui ?
            - Comment puis-je vous aider ?
            - Avez-vous des questions particulières ou des préoccupations concernant votre usage ?
            - Souhaitez-vous des informations sur la réduction des risques, l'arrêt de la consommation, ou autre chose ?
            
            Une fois que l'utilisateur a répondu, adaptez les informations pour lui fournir des conseils ou ressources personnalisées. Soyez empathique, non-jugeant et encourageant."""
        })
    response = client.chat.completions.create(
                model="gpt-4",
                messages=messages
            )
    return response.choices[0].message.content

def generate_stream(message_history):
    messages = [{"role": m["role"], "content": m["content"]} for m in message_history]
    
    if len(message_history) == 1:  # Si c'est la première interaction
        messages.insert(0, {
            "role": "system",
            "content": """Vous êtes Drug-GPT, un assistant IA dédié à aider les personnes confrontées à des dépendances. Plutôt que de donner des réponses directes, commencez par poser des questions pour comprendre les besoins de l'utilisateur.
            
            Exemples de questions ouvertes :
            - Qu'est-ce qui vous a amené à chercher des informations sur cette interface ?
            - Comment puis-je vous être utile aujourd'hui ?
            - Avez-vous des préoccupations particulières au sujet de l'usage de substances ?
            - Cherchez-vous des conseils pour réduire les risques ou pour arrêter ?
            
            Utilisez ces réponses pour adapter vos conseils et fournir des informations utiles, sans jugement."""
        })
    
    stream = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.1,
                stream=True,
            )
    return stream
