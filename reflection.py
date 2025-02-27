import asyncio
import json
from autogen_ext.tools.langchain import LangChainToolAdapter
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import MagenticOneGroupChat
from langchain_community.tools.arxiv import ArxivQueryRun
from utils import clear_console, get_logger, get_openai_model_client, print_answer
from datetime import datetime

logger = get_logger("reflection")

clear_console()


async def main() -> None:
    model_client = get_openai_model_client()

    tool = LangChainToolAdapter(ArxivQueryRun())

    assistant = AssistantAgent(
        "Researcher",
        tools=[tool],
        model_client=model_client,
        system_message=f"Act as a research assistant. Find recent research papers on a given topic and prepare a report. Current date: {datetime.now().strftime("%Y-%m-%d")}.",
        description="An agent that finds recent research papers on a given topic and prepares a report.",
    )

    validator = AssistantAgent(
        "Reviewer",
        model_client=model_client,
        system_message=f"Act as a scientific reviewer and editor. Mark any inconsistencies you can find. Current date: {datetime.now().strftime("%Y-%m-%d")}.",
        description="An agent that reviews the articles found by the researcher.",
    )

    team = MagenticOneGroupChat(
        [assistant, validator], model_client=model_client, max_turns=5, max_stalls=2
    )

    result = await team.run(
        task=f"""Prepare a list of three recent articles in the field of psychology that would be interesting for software engineers.
 Ensure that the list meets reviewer's criteria.
 Current date: {datetime.now().strftime("%Y-%m-%d")}.""",
    )

    answer = result.messages[-1].content

    print_answer(answer)

    state = await team.save_state()

    logger.info(answer)
    logger.info(json.dumps(state, indent=2))


asyncio.run(main())
