import streamlit as st
from streamlit_ace import st_ace, KEYBINDINGS, LANGUAGES, THEMES
import services.prompts
import services.llm
import asyncio

from services import prompts
from helpers import util, chat as chat_service

import helpers.sidebar
import helpers.util

st.set_page_config(
    page_title="Generate Code",
    page_icon="📄",
    layout="wide"
)


helpers.sidebar.show()

st.header("Generate Code")
st.write("Generate code reviews and code suggestions based on example code provided.")


# Function to mimic the resetting of the page
def reset_page():
    st.session_state.editor_id_code_review = st.session_state.editor_id_code_review + 1
    st.session_state.code_review = ""  # Reset the code in the editor
    st.session_state.editor_id_code_debug = st.session_state.editor_id_code_debug + 1
    st.session_state.code_debug = ""  # Reset the code in debug editor
    st.session_state.editor_id_code_modify = st.session_state.editor_id_code_modify + 1
    st.session_state.code_modify = ""  # Reset the code in debug editor
    st.session_state.messages = []  # Reset the chat messages
    st.session_state.review_messages = []  # Reset the review messages
    st.session_state.debug_messages = []  # Reset the debug messages
    st.session_state.error_string = ""  # Reset the error string
    review_container.empty()
    debug_container.empty()

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

    st.subheader("Ducky Review")

    if "review_messages" not in st.session_state:
        st.session_state.review_messages = [] # Initialize the messages list

    review_container = st.container(height=500)

    with review_container:
        advice = st.empty()
        # Print th assistant messages session state
        for message in [m for m in st.session_state.review_messages if m["role"] == "assistant"]:
            advice = st.markdown(message["content"])

        if code_review_button:
            learning_prompt = services.prompts.code_review_prompt(learner_level, code_review)
            review_messages = services.llm.create_conversation_starter(services.prompts.system_learning_prompt())
            review_messages.append({"role": "user", "content": learning_prompt})
            st.session_state.review_messages, review_code = asyncio.run(helpers.util.run_conversation(review_messages, advice))

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

    st.subheader("Ducky Debugging")

    if "debug_messages" not in st.session_state:
        st.session_state.debug_messages = [] # Initialize the messages list

    debug_container = st.container(height=500)
    with debug_container:
        debug_advice = st.empty()
        # Print th assistant messages session state
        for message in [m for m in st.session_state.debug_messages if m["role"] == "assistant"]:
            debug_advice = st.markdown(message["content"])

        if code_debug_button:

            debug_advice = st.markdown("### Ducky Debugging...")
            learning_prompt = services.prompts.code_debug_prompt(learner_level, code_debug, error_string)
            messages = services.llm.create_conversation_starter(services.prompts.system_learning_prompt())
            messages.append({"role": "user", "content": learning_prompt})
            st.session_state.debug_messages, debug_code = asyncio.run(helpers.util.run_conversation(messages, debug_advice))

with tab3:

    code_column, chat_column = st.columns([3, 2])

    with code_column:
        st.subheader("Code")
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
            placeholder="Enter your code to be modified here...",
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

    with chat_column:

        st.subheader("Chat with Ducky")

        # Ensure the session state is initialized
        if "messages" not in st.session_state:
            initial_messages = [{"role": "system",
                                 "content": prompts.modify_code_chat_system_prompt()}]
            st.session_state.messages = initial_messages
        prompt = st.chat_input("Ask me what to modify in the code...")

    st.subheader("Ducky Response")

    with st.container(height=500):

        # Print all messages in the session state
        for message in [m for m in st.session_state.messages if m["role"] != "system"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # React to the user prompt
        if prompt:
            chat_prompt = services.prompts.modify_code_chat_prompt(prompt, code_modify, sidebar_language)

            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "system", "content": chat_prompt})

            st.session_state.messages, new_code = asyncio.run(
                chat_service.chat(st.session_state.messages, prompt, sidebar_language))

            st.session_state.code_modify = new_code
            st.session_state.editor_id_code_modify = st.session_state.editor_id_code_modify + 1
            st.rerun()
