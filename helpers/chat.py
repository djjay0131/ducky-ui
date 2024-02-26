import streamlit as st

# Chat with the LLM, and update the messages list with the response.
# Handles the chat UI and partial responses along the way.
async def chat(messages, prompt, util):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        messages = await util.run_conversation(messages, message_placeholder)
        st.session_state.messages = messages
    return messages
