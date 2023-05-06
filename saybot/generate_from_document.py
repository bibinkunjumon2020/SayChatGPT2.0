
from langchain.chat_models import ChatOpenAI
from llama_index import SimpleDirectoryReader, LLMPredictor, PromptHelper, GPTVectorStoreIndex, ServiceContext,\
    StorageContext, load_index_from_storage
import openai
# from langchain import OpenAI

import os
from dotenv import load_dotenv
from pathlib import Path

# Set base directory and load environment variables

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path)

openai_api_key = os.getenv("API_OPENAI")


def construct_index(directory_path,service_context,) -> None :
    print("inside construct_index")
    documents = SimpleDirectoryReader(directory_path).load_data()
    # when first building the index
    index = GPTVectorStoreIndex.from_documents(
        documents, service_context=service_context
    )
    # handle index for storage and retrieval
    index.storage_context.persist(persist_dir="index")
   

def query_index(service_context,storage_context) -> None :
    print("inside query_index")
 
    index = load_index_from_storage(
        service_context=service_context, storage_context=storage_context
    )
    # prompt handling
    query_engine = index.as_query_engine()

    prompt = input("Enter Your Prompt :\n")
    while(prompt):
        response = query_engine.query(prompt)
        print(response)
        prompt = input("Enter Your Prompt :\n")



if __name__ == '__main__':

    max_input_size = 4096
    num_outputs = 512
    max_chunk_overlap = 20
    chunk_size_limit = 600

    prompt_helper = PromptHelper(
        max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    llm_predictor = LLMPredictor(llm=ChatOpenAI(openai_api_key=openai_api_key,
                                                temperature=0, model_name="gpt-3.5-turbo"))
    # llm_predictor = LLMPredictor(llm=OpenAI(openai_api_key=openai_api_key,temperature=0, model_name="text-davinci-003"))


    service_context = ServiceContext.from_defaults(
        llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    storage_context = StorageContext.from_defaults(persist_dir="index")

    construct_index(directory_path="docs",service_context=service_context)
    query_index(service_context=service_context,storage_context= storage_context)
    
