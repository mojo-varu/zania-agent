from agents.zania_agent import ZaniaAgent
from data.data_indexer import DataIndexer
from loguru import logger
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
import tempfile
from tools.zania_agent_tools import get_retriver_tool, send_slack_message
import streamlit as st


st.header(f"Zania Agent", divider='violet')
st.info(f"An AI agent that leverages the capabilities of a large language model and is capable to extracting answers based on the content of a large PDF document and post the results on Slack.")

with st.container(border=True):
    if 'data_retriever' not in st.session_state:
        st.session_state.data_retriever = None
    # This is the step A for loading PDF file for chunking and indexing
    uploaded_file = st.file_uploader("1. Please upload your PDF file here", 
                                    type=['pdf'], 
                                    accept_multiple_files=False, 
                                    key='input_zania')
        
    if uploaded_file and 'pdf_uploaded' not in st.session_state:
        with st.spinner("Processing the PDF file, this may take some. Please wait..."):
                try:
                    with tempfile.NamedTemporaryFile() as temp_file:
                        temp_file.write(uploaded_file.read())
                        st.session_state.data_retriever = DataIndexer(temp_file.name).get_retriever()
                        st.success(f"The file {uploaded_file.name} has been loaded and indexed sucessfully, Next type your questions, you want to ask from this PDF.")
                        st.session_state.pdf_uploaded = True
                except Exception as e:
                    logger.error(f"Error - failed to load the PDF file for indexing {e}")


    # Now we initalize our agent as we have created the data_retriever 
    # to pass as dependecy for the agent creation
 
    zania_agent = ZaniaAgent(tools=[get_retriver_tool(st.session_state.data_retriever), send_slack_message])

    st.divider()
    # TODO Take questions as a text span and let LLM do the formating and turn into a list of questions
    input_questions =  st.text_area("2. Please provide your questions here, use comma(,) to seperate each question.", 
                                    value="", 
                                    height=None, 
                                    max_chars=500)

    # This is container to show the steps perfomred by agent
    st_callback = StreamlitCallbackHandler(st.container())
    
    
    # TODO this is a basic chat window, it can be enhaced to be more dynammic to user inputs
    with st.sidebar:
        messages = st.container(height=500)
        query = {'input':'Introduce yourself in few words, and instruct user to upload pdf first and \
                                            provide questions to be asked from the PDF.'}
        messages.chat_message("assistant").write(
            zania_agent.provide_instrcution(query=query))
        if user_input := st.chat_input("Ask me something"):
            messages.chat_message("user").write(user_input)
            if input_questions:
                messages.chat_message("assistant").write(f"Proccessing...")
                # trigger the agent to perfrom the task
                zania_agent(input_questions, st_callback)
                messages.chat_message("assistant").write(f"Questions answered")
            else:
                 messages.chat_message("assistant").write(zania_agent.provide_instrcution(query=query))
           