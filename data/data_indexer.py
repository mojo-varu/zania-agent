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
from langchain_openai import OpenAIEmbeddings

DATA_SOURCE_FILE = 'handbook.pdf'
CHUNK_SZIE = 300
CHUNK_OVERLAP = 0
TEXT_SEPARATORS = ["\n\n", "\n", " ", ""]
EMBEDDING_MODEL_NAME = "BAAI/bge-base-en-v1.5"
# SCORE_THRESOLD = 0.5


class DataIndexer():
    """
        Responsible for the followings around indexing of PDF data-
        1. Reading data from text data from a PDF file and generating chunks
        2. Generate vector embeddings of chuncks and index them into a vector store
        3. Provide a retriver to fetch docs based on semantic seach condition used
    """
    def __init__(self, source_file_path=None):    
        try:
            self.embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")
            # self.embedding_model = FastEmbedEmbeddings(model_name=EMBEDDING_MODEL_NAME)
            
            # if self._are_embeddings_already_loaded():
            #     logger.info(f"Embeddings already exists at {Config.VECTOR_DB_PATH}")
            #     return

            logger.info(f"Reading raw documents from {source_file_path}")
            raw_documents = PyPDFLoader(source_file_path).load_and_split()
            text_splitter = RecursiveCharacterTextSplitter(
                separators= TEXT_SEPARATORS,
                chunk_size = CHUNK_SZIE,
                chunk_overlap  = CHUNK_OVERLAP,
                length_function = len,
            )

            self.documents = text_splitter.split_documents(raw_documents)
            logger.info(f"{len(self.documents)} documents post spliting")
            logger.info(f"Now loading embeddings to {Config.VECTOR_DB_PATH}")
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
        """
            Responsible to provide a retriver with specific search method like similarity search, MMR, score thresold
        """
        db = self._get_vectorstore()
        # TODO configure different types of retriever here based ot type of search method
        # return  db.as_retriever(search_type="mmr")
        # return  db.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.5})
        return  db.as_retriever(search_kwargs={"k":3})
    
