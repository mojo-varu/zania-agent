from agents.zania_agent import ZaniaAgent
from config import Config
from data.data_index import DataIndexer
from loguru import logger
from langchain_openai import ChatOpenAI
from langchain_mistralai import ChatMistralAI
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
import tempfile
from tools.zania_agent_tools import get_retriver_tool, send_slack_message
import streamlit as st
import os


# os.environ["MISTRAL_API_KEY"] = Config.MISTRAL_API_KEY
os.environ["OPENAI_API_KEY"] = Config.OPENAI_API_KEY
os.environ["TOKENIZERS_PARALLELISM"] = "false"

if __name__ == '__main__':
    st.header(f"Zania Agent", divider='violet')
    st.info(f"An AI agent that leverages the capabilities of a large language model and is capable to extracting answers based on the content of a large PDF document and post the results on Slack.")

    with st.container(border=True):
        # This is the step A for loading PDF file for chunking and indexing
        uploaded_file = st.file_uploader("1. Please upload your PDF file here", 
                                        type=['pdf'], 
                                        accept_multiple_files=False, 
                                        key='input_zania')
            
        data_retriever = None
        if uploaded_file and 'pdf_uploaded' not in st.session_state:
            with st.spinner("Processing the PDF file, this may take some. Please wait..."):
                    try:
                        with tempfile.NamedTemporaryFile() as temp_file:
                            temp_file.write(uploaded_file.read())
                            data_retriever = DataIndexer(temp_file.name).get_retriever()
                            st.success(f"The file {uploaded_file.name} has been loaded and indexed sucessfully, Next type your questions, you want to ask from this PDF.")
                            st.session_state['pdf_loaded'] = True
                    except Exception as e:
                        logger.error(f"Error - failed to load the PDF file for indexing {e}")


        # Here we initalize our agent since we have created the data_retriever 
        retriever_tool = get_retriver_tool(data_retriever)
        tools = [retriever_tool, send_slack_message]
        
        # llm = ChatMistralAI(model=LLM_MDOEL_NAME)
        llm = ChatOpenAI(model=Config.OPENAI_MODEL_NAME)
        
        zania_agent = ZaniaAgent(llm, tools=tools)

        st.divider()
        # TODO Take questions as a text span and let LLM do the formating and turn into a list of questions
        input_questions =  st.text_area("2. Please provide your questions here, use comma(,) to seperate each question.", 
                                        value="", 
                                        height=None, 
                                        max_chars=500)

        # This is container to show the steps perfomred by agent
        st_callback = StreamlitCallbackHandler(st.container())
        with st.sidebar:
            messages = st.container(height=500)
            temp = [
                (
                    "system",
                    "You are a helpful conversation agent named Zania. Your job is provide short but relatable answer to user for there input",
                ),
                ("human", "introduce yourself and suggest to upload a PDF and type related questions in the text input box"),
            ]
            # llm.invoke(messages)
            messages.chat_message("assistant").write_stream(llm.stream(temp))

            if prompt := st.chat_input("Ask me something"):
                messages.chat_message("user").write(prompt)
                messages.chat_message("assistant").write(f"Echo: {input_questions}")

            zania_agent(input_questions, st_callback)
