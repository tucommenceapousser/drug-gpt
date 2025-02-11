import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_response(message_history):
    messages = [{"role": m["role"], "content": m["content"]} for m in message_history]
    messages.insert(0, {
        "role": "system", 
        "content": """You are a helpful assistant named Drug-GPT. Your purpose is to provide information related to drugs, especially for consumers seeking help with their heroin and cannabis consumption. 
        Your goal is to educate users about harm reduction strategies, the dangers of various drugs, and help them make informed decisions. 
        Always prioritize safety and never promote harmful practices. Make sure to introduce yourself in your initial message."""
    })
    response = client.chat.completions.create(
                model="gpt-4",
                messages=messages
            )
    return response.choices[0].message.content

def generate_stream(message_history):
    messages = [{"role": m["role"], "content": m["content"]} for m in message_history]
    messages.insert(0, {
        "role": "system", 
        "content": """You are a helpful assistant named Drug-GPT. Your purpose is to provide harm reduction information and educate users about the risks of substances like heroin and cannabis. 
        If a user asks for drug information, give a brief description, list the drug class, the mechanism of action, and efficacy. 
        Provide harm reduction tips and main competitors (if any) in point form, along with a brief description of each. 
        Focus on harm reduction and never provide any advice that could encourage unsafe behavior."""
    })
    stream = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.1,
                stream=True,
            )
    return stream
