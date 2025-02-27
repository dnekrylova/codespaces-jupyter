# Workshop Instructions

## Disclaimer
*Magentic-One* is a research project, not a production-ready product. We selected it for this workshop to quickly showcase how agents and human feedback can work together. Note that the code is optimized for demonstration purposes, not for performance or security. In production, consider exploring [Semantic Kernel](https://aka.ms/semantic-kernel).

## Introduction
This workshop guides you through the exciting world of agents in AI systems and highlights the value of human supervision. The content is structured to help you set up your environment, execute your first run, and dive into multi-agent systems, self-reflection, feedback loops, and human collaboration.

## Step 1: Environment Setup

1. **Install the Essentials:**
   - Ensure you have **Python 3.10 or higher** installed.
   - Use **pip** for managing your packages.

2. **Configure Your OpenAI API Key:**
   Set your OpenAI API key as an environment variable:
   ```bash
   export OPENAI_API_KEY="your_openai_api_key"
   ```
   **Tip:** For production scenarios, consider using Azure OpenAI.

3. **(Optional) Create a Virtual Environment:**
   ```bash
   python -m venv workshop_env
   source workshop_env/bin/activate  # On Windows: workshop_env\Scripts\activate
   ```

4. **Install the Required Dependencies:**
   - **Using a requirements file:**
     ```bash
     pip install -r requirements.txt
     ```
   - **Manual Installation:**
     ```bash
     pip install autogen-agentchat autogen-ext[magentic-one,openai,langchain]
     pip install langchain-community arxiv
     ```

## Step 2: First Run

1. **Set Up Your Imports:**
   Begin by importing the necessary modules:
   ```python
   import asyncio
   import json
   from autogen_agentchat.agents import AssistantAgent
   from autogen_agentchat.teams import MagenticOneGroupChat
   from autogen_agentchat.ui import Console
   from colorama import Fore, Style
   import os
   ```

2. **Define the Main Function and Initialize the Model:**
   Create an asynchronous main function that initializes the model client:
   ```python
   async def main() -> None:
       model_client = OpenAIChatCompletionClient(
           model="gpt-4o",
           api_key=os.getenv("OPENAI_API_KEY"),
           temperature=0
       )
   ```

3. **Set Up Your Assistant Agent:**
   Initialize the assistant agent with a clear role and system message:
   ```python
   assistant = AssistantAgent(
       "<descriptive name>",
       model_client=model_client,
       system_message="<instructions for the agent>",
       description="<this will be visible to the orchestrator>",
   )
   ```

4. **Define the Task:**
   Clearly state the task for your assistant:
   ```python
   task = "<your task here>"
   ```

5. **Create and Run the Multi-Agent Team:**
   Set up a multi-agent chat team and run your task:
   ```python
   team = MagenticOneGroupChat(
       [assistant],
       model_client=model_client,
       max_turns=5,
       max_stalls=2
   )
   result = await Console(team.run_stream(task=task), output_stats=True)
   ```

6. **Display the Final Answer:**
   Extract the final response from the session and print it:
   ```python
   answer = result.messages[-1].content
   print_answer(answer)
   ```

7. **Save Your Session State:**
   Save the current session state as a JSON file for future reference:
   ```python
   state = await team.save_state()
   with open("state.json", "w") as f:
       json.dump(state, f)
   ```

8. **Run the Main Function:**
   Execute your asynchronous workflow:
   ```python
   asyncio.run(main())
   ```

9. **Review Your Results:**
   - Execute the code in your Python environment.
   - Check the console for the final answer.
   - Open `state.json` to explore detailed process insights.

## Step 3: Multi-Agent Systems, Self-Reflection, and Feedback Loops

## Step 4: Human-in-the-Loop

## Step 5: LLM-as-a-Judge

## Appendix
The complete code for this workshop is available in the `samples` directory.
