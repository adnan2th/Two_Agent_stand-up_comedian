from groq import Groq
from autogen import ConversableAgent
import os
from dotenv import load_dotenv
import streamlit as st

#load_dotenv()

st.title("🎭 Simple AI Comedy Show")
st.write("A simple stand-up comedy conversation between Adnan & Hassan.") 

#api_key = Groq()



# 1. Safely retrieve the API key from Streamlit's environment/secrets


api_key= os.environ.get("groq_api")


llm_config = {
    "config_list": [
        {
            "model": "openai/gpt-oss-20b", # Using a supported Groq model
            "api_key": api_key,
            "base_url": "https://api.groq.com/openai/v1", # Point explicitly to Groq's endpoint
        }
    ]
}

Adnan = ConversableAgent(
    name="Adnan",
    system_message="Your name is Adnan and you are a stand-up comedian short joke.also mention your name like this (Adnan Speaking): in start"
    "When you're ready to end the conversation, say 'I gotta go'.",

    llm_config=llm_config,
    is_termination_msg=lambda msg: "I gotta go" in msg["content"] or "Goodbye" in msg["content"],
    human_input_mode="NEVER",

)

Hassan = ConversableAgent(
    name="Hassan",
    system_message="Your name is Hassan and you are a stand-up comedian short joke.(Hassan Speaking):"
    "Start the next joke from the punchline of the previous joke."
    "When you're ready to end the conversation, say 'I gotta go'.",

    llm_config=llm_config,
    is_termination_msg=lambda msg: "I gotta go" in msg["content"] or "Goodbye" in msg["content"],
    human_input_mode="NEVER",


)

if st.button("Start Show"):
        with st.spinner("Generating jokes..."):
            chat_result = Adnan.initiate_chat(
                recipient=Hassan,
                message="I'm Adnan. Hassan, let's keep the jokes rolling.",
                
            
            )

            # Simple way to display dialogs
            for message in chat_result.chat_history:
                role = message["sender"] if "sender" in message else "Agent"

                st.chat_message(role).write(message["content"])
