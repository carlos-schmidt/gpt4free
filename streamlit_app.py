import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

import streamlit as st
from streamlit_toggle import toggle

from gpt4free import phind


def get_answer(question: str, context: str, shrink_context: bool = True, cutoff=True) -> str:
    # Set cloudflare clearance cookie and get answer from GPT-4 model
    try:
        result = phind.Completion.create(
            model='gpt-4',
            prompt=question,
            results=phind.Search.create(question, actualSearch=False),
            # create search (set actualSearch to False to disable internet)
            creative=False,
            detailed=False,
            code_context=context,
            shrink_context=shrink_context,
            cutoff=cutoff)  # up to 3000 chars of code

        return result.completion.choices[0].text

    except Exception as e:
        # Return error message if an exception occurs
        return (
            f'An error occurred: {e}. Please make sure you are using a valid cloudflare clearance token and user agent.'
        )


# Set page configuration and add header
st.set_page_config(
    page_title="gpt4freeGUI",
    initial_sidebar_state="expanded",
    page_icon="🧠",
    menu_items={
        'Get Help': 'https://github.com/xtekky/gpt4free/blob/main/README.md',
        'Report a bug': "https://github.com/xtekky/gpt4free/issues",
        'About': "### gptfree GUI",
    },
)
st.header('GPT4free GUI')

# Add text area for user input and button to get answer
question_text_area = st.text_area('🤖 Ask Any Question :', placeholder='Explain quantum computing in 50 words')
context = st.text_area('Context:', placeholder='{"con":"text"}')

shrink_context_switch = toggle(widget='checkbox', value=True,
                               label="Auto-shrink context? (Remove newlines, whitespaces and tabs)")
cutoff_switch = toggle(widget='checkbox', value=True,
                       label="Auto-cut-off context? (Upper limit is 5999 characters of question + context)")

if st.button('🧠 Think'):
    answer = get_answer(question_text_area, context, shrink_context=shrink_context_switch, cutoff=cutoff_switch)
    escaped = answer.encode('utf-8').decode('unicode-escape')
    # Display answer
    st.caption("Answer :")
    st.markdown(escaped)

# Hide Streamlit footer
hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
