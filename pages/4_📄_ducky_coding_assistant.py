import os

import streamlit as st
import openai

# Set your OpenAI API key here
openai.api_key = os.getenv('OPENAI_API_KEY')

def review_code(code):
    try:
        # Replace "text-davinci-003" with the appropriate model you want to use
        response = openai.Completion.create(
          engine="text-davinci-003",
          prompt=f"Review the following code:\n\n{code}\n\n",
          temperature=0.7,
          max_tokens=150,
          top_p=1.0,
          frequency_penalty=0.0,
          presence_penalty=0.0
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    st.title("Ducky Coding Assistant")

    # Text area for code input
    code = st.text_area("Enter your code here:", height=300)

    # Button to trigger code review
    if st.button("Review Code"):
        with st.spinner('Reviewing your code...'):
            review_result = review_code(code)
            st.success("Review complete!")
            st.write(review_result)

if __name__ == "__main__":
    main()
