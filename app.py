import streamlit as st
from streamlit_chat import message
from openai import OpenAI
from google import generativeai as genai
import anthropic
from dotenv import load_dotenv
import os

load_dotenv()

# Open AI Client
Open_AI_Client = OpenAI(api_key= os.getenv("OPENAI_API_KEY"))

# Gemini Client
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
Gemini_Client = genai.GenerativeModel(
    model_name="gemini-pro"
)

# Claude Client
Claude_Client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))



def gemini_response(prompt):
    st.session_state.gemini_chat_history.append({"role":"user", "text":prompt})
    chat = Gemini_Client.start_chat(history = [])
    
    AI_Response = chat.send_message(
        content=prompt,
        generation_config=genai.GenerationConfig(
            temperature=0.5,
        )
    )
    return AI_Response.text


def chat_gpt_response(prompt):
    st.session_state.gpt_chat_history.append({"role":"user", "content":prompt})
    AI_Response = Open_AI_Client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.gpt_chat_history,
        temperature=0.5,
    )
    return AI_Response.choices[0].message.content


def claude_response(prompt):

    st.session_state.claude_chat_history.append({"role":"user", "content":prompt})
    AI_Response = Claude_Client.messages.create(
        model="claude-2.1",
        temperature=0.5,
        max_tokens=256,
        messages=st.session_state.claude_chat_history
    )
    return AI_Response.content[0].text

def main():

    st.header("Conversations with AI : ChatGPT, Gemini, Claude 🚀")
    st.divider()
    chat_gpt, gemini, claude = st.tabs(["Chat with GPT", "Chat with Gemini","Chat with Claude"])

    with chat_gpt:
        prompt_gpt = st.text_input("Prompt:", placeholder="Ask me anything...",key="prompt_gpt")

        if "gpt_chat_history" not in st.session_state:
            st.session_state["gpt_chat_history"] = []

        if prompt_gpt:
            with st.spinner("Thinking..."):
                generated_response = chat_gpt_response(prompt_gpt)
                st.session_state.gpt_chat_history.append({"role":"assistant", "content":generated_response})

            for msg in st.session_state.gpt_chat_history:
                if msg["role"] == "user":
                    message(msg["content"], is_user=True, avatar_style="personas")
                elif msg["role"] == "assistant":
                    message(msg["content"], is_user=False, avatar_style="bottts")

    with gemini:
        prompt_gemini = st.text_input("Prompt:", placeholder="Ask me anything...",key="prompt_gemini")

        if "gemini_chat_history" not in st.session_state:
            st.session_state["gemini_chat_history"] = []

        if prompt_gemini:

            with st.spinner("Thinking..."):
                generated_response = gemini_response(prompt_gemini)
                st.session_state.gemini_chat_history.append({"role":"model", "text":generated_response})

            for msg in st.session_state.gemini_chat_history:
                if msg["role"] == "user":
                    message(msg["text"], is_user=True, avatar_style="personas")
                elif msg["role"] == "model":
                    message(msg["text"], is_user=False, avatar_style="bottts")

    with claude:

        prompt_claude = st.text_input("Prompt:", placeholder="Ask me anything... ",key="prompt_claude")
        
        if "claude_chat_history" not in st.session_state:
            st.session_state["claude_chat_history"] = []
        
        if prompt_claude:
            
            with st.spinner("Thinking..."):
                generated_response = claude_response(prompt_claude)
                st.session_state.claude_chat_history.append({"role":"assistant", "content":generated_response})

            for msg in st.session_state.claude_chat_history:
                if msg["role"] == "user":
                    message(msg["content"], is_user=True, avatar_style="personas")
                elif msg["role"] == "assistant":
                    message(msg["content"], is_user=False, avatar_style="bottts")


if __name__ == '__main__':
    main()
