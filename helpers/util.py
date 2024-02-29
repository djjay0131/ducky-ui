import io
from typing import List, Dict

import pandas
from streamlit.delta_generator import DeltaGenerator

import services.llm


async def run_conversation(messages: List[Dict[str, str]], message_placeholder: DeltaGenerator,
                           start_code_marker: str = "", end_code_marker: str = "") -> (List[Dict[str, str]], str):
    full_response = ""
    extracted_code = ""
    message_placeholder.markdown("Thinking...")
    chunks = services.llm.converse(messages)
    chunk = await anext(chunks, "END OF CHAT")
    while chunk != "END OF CHAT":
        print(f"Received chunk from LLM service: {chunk}")
        if chunk.startswith("EXCEPTION"):
            full_response = ":red[We are having trouble generating advice. Please wait a minute and try again.]"
            break
        full_response = full_response + chunk
        message_placeholder.markdown(full_response + "▌")
        chunk = await anext(chunks, "END OF CHAT")
    message_placeholder.markdown(full_response)

    # Extract code if markers are provided
    if start_code_marker and end_code_marker:
        start_index = full_response.find(start_code_marker)
        end_index = full_response.find(end_code_marker, start_index + 1)
        if start_index != -1 and end_index != -1:
            extracted_code = full_response[start_index + len(start_code_marker):end_index].strip()

    messages.append({"role": "assistant", "content": full_response})
    return messages, extracted_code


async def run_prompt(prompt: str, message_placeholder: DeltaGenerator) -> Dict[str, object]:
    messages = services.llm.create_conversation_starter(prompt)
    result = await run_conversation(messages, message_placeholder, "```code_start", "```code_end")
    return result


def copy_as_csv_string(data_frame: pandas.DataFrame) -> str:
    # Convert DataFrame to CSV-like string
    csv_string_io = io.StringIO()
    data_frame.to_csv(csv_string_io, index=False, sep=',')

    # Get the CSV data from the StringIO object
    return csv_string_io.getvalue()
