from typing import Optional
from autogen import Agent, ConversableAgent
from aitools_autogen import utils
from aitools_autogen.agents import WebPageScraperAgent
from aitools_autogen.blueprint import Blueprint
from aitools_autogen.config import WORKING_DIR
from aitools_autogen.config import llm_config_openai as llm_config, config_list_openai as config_list, WORKING_DIR


class SoftwareSystemBlueprint(Blueprint):

    def __init__(self, work_dir: Optional[str] = WORKING_DIR):
        super().__init__([], config_list=config_list, llm_config=llm_config)
        self._work_dir = work_dir or "code"
        self._summary_result: Optional[str] = None

    @property
    def summary_result(self) -> str | None:
        """The getter for the 'summary_result' attribute."""
        return self._summary_result

    @property
    def work_dir(self) -> str:
        """The getter for the 'work_dir' attribute."""
        return self._work_dir

    async def initiate_work(self, message: str):
        utils.clear_working_dir(self._work_dir)
        agent0 = ConversableAgent("a0",
                                  max_consecutive_auto_reply=0,
                                  llm_config=False,
                                  human_input_mode="NEVER")

        scraper_agent = WebPageScraperAgent()

        summary_agent = ConversableAgent("summary_agent",
                                         max_consecutive_auto_reply=6,
                                         llm_config=llm_config,
                                         human_input_mode="NEVER",
                                         code_execution_config=False,
                                         function_map=None,
                                         system_message="""You are a helpful AI assistant.
        You can summarize OpenAPI specifications.  When given an OpenAPI specification,
        output a summary in bullet point form for each endpoint.
        Let's make it concise in markdown format.
        It should include short descriptions of parameters,
        and list expected possible response status codes.
        Return `None` if the OpenAPI specification is not valid or cannot be summarized.
            """)

        fastapi_agent = ConversableAgent("fastapi_agent",
                                                max_consecutive_auto_reply=6,
                                                llm_config=llm_config,
                                                human_input_mode="NEVER",
                                                code_execution_config=False,
                                                function_map=None,
                                                system_message="""
        You are a developer expert in Python, using the FastAPI framework.
        You're writing the web, service, data and core layer for a software system.

        When you receive a message, you should expect that message to tell you the type of the software system they want to build,
        and you need to help them build the web, service, data and core layer of that software system.

        All files must be generated in the api/client directory.

        Use multiple classes in separate file names in a directory structure that makes sense.

        You must indicate the script type in the code block.
        Do not suggest incomplete code which requires users to modify.
        Always put `# filename: api/client/<filename>` as the first line of each code block.

        Feel free to include multiple code blocks in one response. Do not ask users to copy and paste the result.
        """)


        # agent0.initiate_chat(scraper_agent, True, True, message=message)
        #
        # message = agent0.last_message(scraper_agent)
        #
        # agent0.initiate_chat(summary_agent, True, True, message=message)

        # api_description_message = agent0.last_message(summary_agent)

        # api_description = api_description_message["content"]
        # print(api_description)

        system_description_message = message

        agent0.initiate_chat(fastapi_agent, True, True, message=system_description_message)
        message = agent0.last_message(fastapi_agent)
        agent0.initiate_chat(summary_agent, True, True, message=message)

        llm_message = agent0.last_message(fastapi_agent)["content"]
        utils.save_code_files(llm_message, self.work_dir)

        self._summary_result = utils.summarize_files(self.work_dir)
