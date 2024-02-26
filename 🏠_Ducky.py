import streamlit as st

import helpers.sidebar

st.set_page_config(
	page_title="Ducky",
	page_icon="🦆",
	layout="wide"
)

helpers.sidebar.show()

st.toast("Welcome to Ducky!", icon="🦆")

st.markdown("Welcome to Ducky, your AI-powered personal software development assistant!")
st.write("Ducky is designed to help you deliver software better and faster.")

