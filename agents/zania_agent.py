from typing import Any
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from loguru import logger


class ZaniaAgent():
    prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
                You are a useful assistant capable of answering question as provided in the input, use the retriever_tool tool to get the information needed.
                If the answer is not found or is low confidence, then reply with “Data Not Available”. 
                Always provide your answer as JSON object, with question as the input string and answer as response generated.
                then use send_slack_message tool to send this JSON object as payload to a slack channel.
            """
        ),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])


    def __init__(self, llm, tools):
        try:
            self.llm = llm
            self.tools = tools
            self.agent = create_tool_calling_agent(llm, tools, self.prompt)
            self.agent_executor = AgentExecutor(agent=self.agent, tools=tools, verbose=True)
        except Exception as e:
            logger.error(f"Error - failed to initialize {self.cls} - {e}")


    def __call__(self, questions: str, callback=None) -> Any:
        questions_list = questions.split(',') if questions else []
        agent_inputs = [{"input": question.strip()} for question in questions_list] 
        logger.debug(f"Zania agent __call__ {agent_inputs}")
        
        # output = self.agent_executor.batch(agent_inputs)
        if agent_inputs:
            output = self.agent_executor.invoke(
                agent_inputs[0], {"callbacks": [callback]}
            )
            logger.debug(f"agent_executor.batch output {output}")
        