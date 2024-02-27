import streamlit as st
from streamlit_ace import st_ace, KEYBINDINGS, LANGUAGES, THEMES
import services.prompts
import services.llm
import asyncio

from services import prompts
from helpers import util, chat as chat_service

st.set_page_config(
    page_title="Generate Code",
    page_icon="📄",
    layout="wide"
)

import helpers.sidebar
import helpers.util

helpers.sidebar.show()

st.header("Generate Code")
st.write("Generate code reviews and code suggestions based on example code provided.")


# Function to mimic the resetting of the page
def reset_page():
    st.session_state.editor_id_code_review = st.session_state.editor_id_code_review + 1
    st.session_state.code_review = ""  # Reset the code in the editor
    st.session_state.editor_id_code_debug = st.session_state.editor_id_code_debug + 1
    st.session_state.code_debug = ""  # Reset the code in debug editor


# Add a sidebar option to select a learner level
st.sidebar.write("### Chat Response Settings")
learner_level = st.sidebar.selectbox("I'd like my answer as if I were a:",
                                     ["5 year old", "high school student", "college student", "expert coder"],
                                     index=3)
# Sidebar with a reset button
st.sidebar.button("Reset Page", on_click=reset_page)

st.sidebar.divider()

st.sidebar.write("### Code Editor Settings")
sidebar_language = st.sidebar.selectbox("Language mode", options=LANGUAGES, index=121)
sidebar_theme = st.sidebar.selectbox("Theme", options=THEMES, index=5)
sidebar_font_size = st.sidebar.slider("Font size", 5, 24, 14)
sidebar_tab_size = st.sidebar.slider("Tab size", 1, 8, 4)
sidebar_wrap = st.sidebar.checkbox("Wrap lines", value=False)
sidebar_gutter = st.sidebar.checkbox("Show gutter", value=True)
sidebar_print_margin = st.sidebar.checkbox("Show print margin", value=True)
sidebar_auto_update = st.sidebar.checkbox("Auto update", value=True)
sidebar_readonly = st.sidebar.checkbox("Read only", value=False)

# Using tabs for different features
tab1, tab2, tab3 = st.tabs(["Review Code", "Debug Code", "Modify Code"])

with tab1:
    st.subheader("Review Code")

    st.write("Enter your code to be reviewed here:")

    # Every time we reload the page, make a new editor with a new id
    CODE_REVIEW_EDITOR_KEY_PREFIX = "ace-editor-code_review"
    if 'editor_id_code_review' not in st.session_state:
        st.session_state.editor_id_code_review = 0

    # Empty code on first run
    if "code_review" not in st.session_state:
        st.session_state.code_review = ""

    # This is how we update code in the editor - saving it in a session variable "code".
    INITIAL_CODE_TO_REVIEW = st.session_state.code_review

    code_review = st_ace(
        value=INITIAL_CODE_TO_REVIEW,
        language=sidebar_language,
        placeholder="Enter your code to be reviewed here...",
        theme=sidebar_theme,
        font_size=sidebar_font_size,
        tab_size=sidebar_tab_size,
        wrap=sidebar_wrap,
        show_gutter=sidebar_gutter,
        show_print_margin=sidebar_print_margin,
        auto_update=sidebar_auto_update,
        readonly=sidebar_readonly,
        key=f"{CODE_REVIEW_EDITOR_KEY_PREFIX}-{st.session_state.editor_id_code_review}",
        height=500,
        min_lines=12,
        max_lines=20
    )

    code_review_button = st.button("Get Review", key='get_review')

    if code_review_button:
        advice = st.markdown("### Ducky Teaching...")
        learning_prompt = services.prompts.code_review_prompt(learner_level, code_review)
        messages = services.llm.create_conversation_starter(services.prompts.system_learning_prompt())
        messages.append({"role": "user", "content": learning_prompt})
        asyncio.run(helpers.util.run_conversation(messages, advice))
    else:
        st.write("Review response will appear here")

with tab2:
    st.subheader("Debug Code")

    # Every time we reload the page, make a new editor with a new id
    CODE_DEBUG_EDITOR_KEY_PREFIX = "ace-editor-code_debug"
    if 'editor_id_code_debug' not in st.session_state:
        st.session_state.editor_id_code_debug = 0

    # Empty code on first run
    if "code_debug" not in st.session_state:
        st.session_state.code_debug = ""

    # This is how we update code in the editor - saving it in a session variable "code".
    INITIAL_CODE_TO_DEBUG = st.session_state.code_debug

    code_debug = st_ace(
        value=INITIAL_CODE_TO_DEBUG,
        language=sidebar_language,
        placeholder="Enter your code to be debugged here...",
        theme=sidebar_theme,
        font_size=sidebar_font_size,
        tab_size=sidebar_tab_size,
        wrap=sidebar_wrap,
        show_gutter=sidebar_gutter,
        show_print_margin=sidebar_print_margin,
        auto_update=sidebar_auto_update,
        readonly=sidebar_readonly,
        key=f"{CODE_DEBUG_EDITOR_KEY_PREFIX}-{st.session_state.editor_id_code_debug}",
        height=500,
        min_lines=12,
        max_lines=20
    )

    error_string = st.text_area("Optional: Enter error string", key='error_string', height=150)

    code_debug_button = st.button("Debug Code", key='debug_code')

    if code_debug_button:
        debug_advice = st.markdown("### Ducky Debugging...")
        learning_prompt = services.prompts.code_debug_prompt(learner_level, code_debug, error_string)
        messages = services.llm.create_conversation_starter(services.prompts.system_learning_prompt())
        messages.append({"role": "user", "content": learning_prompt})
        asyncio.run(helpers.util.run_conversation(messages, debug_advice))
    else:
        st.write("Debug response will appear here")

with tab3:
    st.subheader("Modify Code")

    column_chat, column_code = st.columns([1, 1])

    with column_code:
        # Every time we reload the page, make a new editor with a new id
        CODE_MODIFY_EDITOR_KEY_PREFIX = "ace-editor-code_modify"
        if 'editor_id_code_modify' not in st.session_state:
            st.session_state.editor_id_code_modify = 0

        # Empty code on first run
        if "code_modify" not in st.session_state:
            st.session_state.code_modify = ""

        # This is how we update code in the editor - saving it in a session variable "code".
        INITIAL_CODE_TO_MODIFY = st.session_state.code_modify

        code_modify = st_ace(
            value=INITIAL_CODE_TO_MODIFY,
            language=sidebar_language,
            placeholder="Enter your code to be modifyged here...",
            theme=sidebar_theme,
            font_size=sidebar_font_size,
            tab_size=sidebar_tab_size,
            wrap=sidebar_wrap,
            show_gutter=sidebar_gutter,
            show_print_margin=sidebar_print_margin,
            auto_update=sidebar_auto_update,
            readonly=sidebar_readonly,
            key=f"{CODE_MODIFY_EDITOR_KEY_PREFIX}-{st.session_state.editor_id_code_modify}",
            height=1000,
            min_lines=12,
            max_lines=20
        )

    # Ensure the session state is initialized
    if "messages" not in st.session_state:
        initial_messages = [{"role": "system",
                             "content": prompts.modify_code_chat_system_prompt()}]
        st.session_state.messages = initial_messages

    with column_chat:

        # Print all messages in the session state
        for message in [m for m in st.session_state.messages if m["role"] != "system"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # React to the user prompt
        if prompt := st.chat_input("Ask me what to modify in the code..."):
            chat_prompt = services.prompts.modify_code_chat_prompt(code_modify, prompt)

            st.session_state.messages.append({"role": "user", "content": chat_prompt})

            asyncio.run(chat_service.chat(st.session_state.messages, prompt, util))

