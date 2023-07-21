import signal
import time

import dotenv
import rich
from rich.box import Box
from gentopia.tools.arxiv_search import ArxivSearch
from gentopia.tools.google_search import GoogleSearch
from gentopia.tools.web_page import WebPage
from gentopia.tools.shell import RunShell
from gentopia.assembler.agent_assembler import AgentAssembler
from gentopia.tools.code_interpreter import *
from gentopia.output import enable_log
from gentopia import chat
from gentopia.tools.gradio import TextToImage

from gentopia.tools.calculator import Calculator



if __name__ == '__main__':

    enable_log(log_level='debug')
    dotenv.load_dotenv(".env")

    tool = GoogleSearch()
    print(tool.description)
    print(tool.run("a cute dog"))

    # assembler = AgentAssembler(file='configs/react.yaml')
    #
    # # # assembler.manager = LocalLLMManager()
    # agent = assembler.get_agent()
    #
    # chat(agent)