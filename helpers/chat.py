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

async def code_chat(messages, prompt, util):
    """

    :param messages:  Current messages in the chat
    :param prompt:  User prompt
    :param util:  Utility functions to run the conversation
    :return:  Current chat messages with response, modified source code
    """
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        messages = await util.run_conversation(messages, message_placeholder)
        st.session_state.messages = messages

    code = ""

    return messages, code
