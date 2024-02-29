import streamlit as st
import helpers.util as util

# Chat with the LLM, and update the messages list with the response.
# Handles the chat UI and partial responses along the way.
async def chat(messages, prompt, language):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        messages, code = await util.run_conversation(messages, message_placeholder,
                                                     f"```{language}", "```")
        st.session_state.code_modify = code
        # Assuming you want to do something with the extracted code here
        # For example, display the code in a code block

    return messages, code


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
