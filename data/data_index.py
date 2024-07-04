import os
import glob
import requests
from loguru import logger
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from typing import List, Dict, Any
from config import Config
from langchain_community.document_loaders import PyPDFLoader

DATA_SOURCE_FILE = 'handbook.pdf'
CHUNK_SZIE = 300
CHUNK_OVERLAP = 0
TEXT_SEPARATORS = ["\n\n", "\n", " ", ""]
EMBEDDING_MODEL_NAME = "BAAI/bge-base-en-v1.5"
COLLECTION_NAME="zania",

# SCORE_THRESOLD = 0.5

# os.environ["MISTRAL_API_KEY"] = Config.MISTRAL_API_KEY
os.environ["OPENAI_API_KEY"] = Config.OPENAI_API_KEY
os.environ["TOKENIZERS_PARALLELISM"] = "false"

LLM_MDOEL_NAME = "mistral-large-latest"

class DataIndexer():
    def __init__(self, source_file_path=None):    
        try:
            self.embedding_model = FastEmbedEmbeddings(model_name=EMBEDDING_MODEL_NAME)
            
            # if self._are_embeddings_already_loaded():
            #     logger.info(f"Embeddings already exists at {Config.VECTOR_DB_PATH}")
            #     return

            logger.info(f"Reading raw documents from {source_file_path}")
            raw_documents = PyPDFLoader(source_file_path).load_and_split()

            # logger.debug(f"Raw documents len {len(raw_documents)}")

            text_splitter = RecursiveCharacterTextSplitter(
                separators= TEXT_SEPARATORS,
                chunk_size = CHUNK_SZIE,
                chunk_overlap  = CHUNK_OVERLAP,
                length_function = len,
            )

            self.documents = text_splitter.split_documents(raw_documents)
            logger.debug(f"Documents post split len {len(self.documents)}")

            Chroma.from_documents(self.documents, 
                                embedding=self.embedding_model, 
                                collection_name="zania-vectorstore",
                                persist_directory=Config.VECTOR_DB_PATH)
        
            logger.info(f"Loading of embeddings from file {DATA_SOURCE_FILE} \
                        at {Config.VECTOR_DB_PATH} completed successfully")
        except Exception as e:
            logger.error(f"Error - Indexing of the data from {source_file_path} failed {e}")   


    def _are_embeddings_already_loaded(self):
        return any(os.path.isdir(item) for item in glob.glob(f'{Config.VECTOR_DB_PATH}/*'))


    def _get_vectorstore(self):
        self.vectorstore =  Chroma(persist_directory=Config.VECTOR_DB_PATH, 
                embedding_function=self.embedding_model, 
                collection_name="zania-vectorstore")
        return self.vectorstore


    def get_retriever(self):
        db = self._get_vectorstore()
        # TODO configure different types of retriever here, depedning upon the type semantic search to perform
        return  db.as_retriever(search_kwargs={"k":2}) #search_type="mmr"



# def format_docs(docs):
#         return "\n\n".join(doc.page_content for doc in docs)



# def parse(output):
#     # If no function was invoked, return to user
#     if "function_call" not in output.additional_kwargs:
#         return AgentFinish(return_values={"output": output.content}, log=output.content)

#     # Parse out the function call
#     function_call = output.additional_kwargs["function_call"]
#     name = function_call["name"]
#     inputs = json.loads(function_call["arguments"])

#     # If the Response function was invoked, return to the user with the function inputs
#     if name == "Response":
#         return AgentFinish(return_values=inputs, log=str(function_call))
#     # Otherwise, return an agent action
#     else:
#         return AgentActionMessageLog(
#             tool=name, tool_input=inputs, log="", message_log=[output]
#         )


# class Response(BaseModel):
#     """Final response to the question being asked"""

#     answer: str = Field(description="The final answer to respond to the user")
#     sources: List[int] = Field(
#         description="List of page chunks that contain answer to the question. Only include a page chunk if it contains relevant information"
#     )


