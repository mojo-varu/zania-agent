import json
import requests
from config import Config
from loguru import logger
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import tool


def get_retriver_tool(retriever):
    return create_retriever_tool(
        retriever,
        "search_indexed_pdf_data",
        """ Search and return contexts from the data to help in preparing better answers for the questions asked."""
    )


@tool
def send_slack_message(payload: str) -> str:
    """
    Helps in send any message provided as param to a slack channel using slack webhook.
    """
    try:
        response = requests.post(Config.SLACK_WEBHOOK_URL, 
                                 data=json.dumps({"text": payload}), 
                                 headers={"Content-type": "application/json"})
        response.raise_for_status()
        return "Slack message delivered."
    except requests.exceptions.RequestException as e:
        return f"Failed to deliver slack mesasge - {e}"
