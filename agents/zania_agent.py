from config import Config
from typing import Any
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_mistralai import ChatMistralAI
from loguru import logger
import os

# os.environ["MISTRAL_API_KEY"] = Config.MISTRAL_API_KEY
os.environ["OPENAI_API_KEY"] = Config.OPENAI_API_KEY
os.environ["TOKENIZERS_PARALLELISM"] = "false"

class ZaniaAgent():
    """
       Responsible for defining the what the agent is, what LLM it depends upon and what it can do via tools
    """
    prompt = ChatPromptTemplate.from_messages(
    [
        # (
        #     "system",
        #     """
        #         You are a useful assistant, named agent Zania, for answering question provided in the input. 
        #         Please use the retriever_tool tool to get the information needed.
        #         If the answer is not found or is low confidence, then reply with Data Not Available. 
        #         Always provide your answer as JSON object, with question key as the input string and answer key as response generated.
        #         then use send_slack_message tool to send this JSON object as payload to a slack channel.
        #     """
        # ),
        (
            "system",
            """
                You are a useful assistant, named agent Zania. You are capable of doing the followings -
                --- Provide short friendly instruction, don't use retriever_tool for this neither send_slack_message to send any message. 
                --- Answering specific question provided in the input. Use the retriever_tool tool to get the information needed.
                    If the answer is not found or is low confidence, then reply with Data Not Available. 
                    Always provide your answer as JSON object, with question key as the input string and answer key as response generated then use send_slack_message tool to send this JSON object as payload to a slack channel.
            """
        ),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])


    def __init__(self, tools):
        try:
            # self.llm = ChatMistralAI(model=Config.MISTRAL_MDOEL_NAME)
            self.llm = ChatOpenAI(model=Config.OPENAI_MODEL_NAME)
            self.tools = tools
            self.agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)
            self.agent_executor = AgentExecutor(agent=self.agent, tools=tools, verbose=True)
        except Exception as e:
            logger.error(f"Error - failed to initialize ZaniaAgent instance - {e}")


    def __call__(self, questions: str, callback=None) -> Any:
        try:
            questions_list = questions.split(',') if questions else []
            agent_inputs = [{"input": question.strip()} for question in questions_list] 
            logger.debug(f"Zania agent __call__ {agent_inputs}")

            # output = self.agent_executor.batch(agent_inputs)
            # output = self.agent_executor.invoke(agent_inputs[0], {"callbacks": [callback]})
            if agent_inputs:
                output = list(map(lambda item: self.agent_executor.invoke(item, {"callbacks": [callback]}), agent_inputs))
                logger.debug(f"agent_executor.batch output {output}")
        except Exception as e:
            logger.error(f"Error - agent failed to execute the actions - {e}")


    def provide_instrcution(self, query) -> str:
        # return self.agent_executor.stream(query)
        return self.agent_executor.invoke(query).get('output')
