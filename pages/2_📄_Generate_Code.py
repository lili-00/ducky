import asyncio
import os

import openai
import streamlit as st

import helpers.sidebar
import helpers.util
import services.prompts
import services.llm

st.set_page_config(
    page_title="Generate Code",
    page_icon="📄",
    layout="wide"
)

# Add comments to explain the purpose of the code sections

# Show sidebar
helpers.sidebar.show()

#############################################################################

openai.api_key = os.getenv('OPENAI_API_KEY')
openai_model = os.getenv('OPENAI_API_MODEL')

st.write("Welcome to the code generator!")
st.write("This tool is designed to help you generate code for your software projects.")
# st.write("(omitted for the project 5 since students main achievement is to implement this page)")


answer_button_sb = st.sidebar.button("Get Answer&nbsp;&nbsp;➠", type="primary", key="answer_button_sb")

user_review_code = st.text_input("You can enter your code and let me review it:", placeholder="Review your code here")
user_review_code_button = st.button("Review Code", key="user_review_code_button")

if user_review_code_button:
    advice = st.markdown("### Ducky Reviewing...")
    review_prompt = services.prompts.review_prompt(user_review_code)
    messages = services.llm.create_conversation_starter(services.prompts.review_prompt(review_code=user_review_code))
    messages.append({"role": "user",
                     "content": f"{review_prompt}\n"})
    asyncio.run(helpers.util.run_conversation(messages, advice))




debug_code = st.text_input("You can enter your debug code here", placeholder="Debug code")
optional_debug_message = st.text_input("You can enter your optional debug message here:", placeholder="Optional debug message")

debug_button = st.button("Debug Code", key="debug_button")

if debug_button:
    advice = st.markdown("### Ducky Debugging...")
    debug_prompt = services.prompts.debug_prompt(debug_code, optional_debug_message)
    messages = services.llm.create_conversation_starter(services.prompts.system_learning_prompt())
    messages.append({"role": "user",
                     "content": f"{debug_prompt}\n"})
    asyncio.run(helpers.util.run_conversation(messages, advice))




modify_code = st.text_input("You can enter your code that you want to modify here", placeholder="Modify code")

modify_button = st.button("Modify Code", key="modify_code_button")

if modify_button:
    advice = st.markdown("### Ducky Modifying...")
    modify_prompt = services.prompts.modify_code_prompt(modify_code)
    messages = services.llm.create_conversation_starter(services.prompts.system_learning_prompt())
    messages.append({"role": "user",
                     "content": f"{modify_prompt}\n"})
    asyncio.run(helpers.util.run_conversation(messages, advice))



reset_button = st.button("Reset Page", key="reset_page_button")

if reset_button:
    # advice = st.markdown("### Ducky Modifying...")
    modify_prompt = services.prompts.modify_code_prompt(modify_code)
    messages = services.llm.create_conversation_starter(services.prompts.system_learning_prompt())
    messages.append({"role": "user",
                     "content": f"Forget all the previous chatting history. {messages}\n"})
    asyncio.run(helpers.util.run_conversation(messages))
