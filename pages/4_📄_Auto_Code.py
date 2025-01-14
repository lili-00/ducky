import asyncio
import streamlit as st
from asyncio import sleep

import helpers.sidebar
import helpers.util
from aitools_autogen.blueprint_generate_core_client import CoreClientTestBlueprint
from aitools_autogen.blueprint_project8 import SoftwareSystemBlueprint
from aitools_autogen.config import llm_config_openai as llm_config
from aitools_autogen.utils import clear_working_dir

st.set_page_config(
    page_title="Auto Code",
    page_icon="📄",
    layout="wide"
)

# Add comments to explain the purpose of the code sections

# Show sidebar
helpers.sidebar.show()

if st.session_state.get("blueprint", None) is None:
    # st.session_state.blueprint = CoreClientTestBlueprintBedrock()
    st.session_state.blueprint = SoftwareSystemBlueprint()

async def run_blueprint(ctr, seed: int = 42) -> str:
    await sleep(3)
    llm_config["seed"] = seed
    await st.session_state.blueprint.initiate_work(message=task)
    return st.session_state.blueprint.summary_result

blueprint_ctr, parameter_ctr = st.columns(2, gap="large")
with blueprint_ctr:
    st.markdown("# Run Blueprint")
    software_system = st.text_input("Enter a software system that you would like to build:", value="A house rental system")
    agents = st.button("Start the Agents!", type="primary")

with parameter_ctr:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### Other Options")
    clear = st.button("Clear the autogen cache...&nbsp; ⚠️", type="secondary")
    seed = st.number_input("Enter a seed for the random number generator:", value=42)

dynamic_ctr = st.empty()
results_ctr = st.empty()

if clear:
    with results_ctr:
        st.status("Clearing the agent cache...")
    clear_working_dir("../aitools_autogen/.cache", "*")

if agents:
    with results_ctr:
        st.status("Running the Blueprint...")

    task = f"""
            I want to build a software system that is a {software_system}
            """

    text = asyncio.run(run_blueprint(ctr=dynamic_ctr, seed=seed))
    st.balloons()

    with results_ctr:
        st.markdown(text)


