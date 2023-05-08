
from langchain.chat_models import ChatOpenAI
from llama_index import SimpleDirectoryReader, LLMPredictor, PromptHelper, GPTVectorStoreIndex, ServiceContext,\
    StorageContext, load_index_from_storage

# from saybot.config import ConfigClass
from saybot.select_file_config import SelectFileClass
# from langchain import OpenAI
# import os
# from dotenv import load_dotenv
# from pathlib import Path

from saybot import os,logging,Update,retrieve_index_dir,retrieve_index_dir_from_fileid
# Set base directory and load environment variables

# BASE_DIR = Path(__file__).resolve().parent.parent
# dotenv_path = os.path.join(BASE_DIR, ".env")
# load_dotenv(dotenv_path)

openai_api_key = "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"


def process_initializers():  # only initialize variables
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
    return service_context


# Convert uploaded file into index and store in target
async def construct_index(source_dir,index_folder_path) -> None :
    print("inside construct_index")
    service_context = process_initializers() # calling method
    documents = SimpleDirectoryReader(source_dir).load_data()
    # when first building the index
    index = GPTVectorStoreIndex.from_documents(
        documents, service_context = service_context
    )
    # handle index for storage and retrieval
    index.storage_context.persist(persist_dir=index_folder_path) # -> store in db
   

def load_query_engine(update:Update):
   
    logging.info("inside query_engine")
    user_id = update.message.from_user.id
    file_id = SelectFileClass.get_select_file_id()
    # file_id = ConfigClass.get_select_file_id()
 
    if file_id is None:
        target_index_dir,file_name = retrieve_index_dir(user_id) #it returns a tuple
    else:
        target_index_dir,file_name = retrieve_index_dir_from_fileid(file_id = file_id) #it returns a tuple
    
    logging.info(target_index_dir)
    logging.info(file_name)
    service_context = process_initializers()
    storage_context = StorageContext.from_defaults(persist_dir=target_index_dir) # <- load from db

    index = load_index_from_storage(
        service_context = service_context, storage_context = storage_context
    )
    # prompt handling
    query_engine = index.as_query_engine()

    return query_engine,file_name

def generate_response_from_userdoc(prompt,update): 
    logging.info("inside generate_response_from_userdoc")
    query_engine,file_name = load_query_engine(update= update)
    response = query_engine.query(prompt)
    response_text = f"{response.response} : \n\nAnswered from your file 📝 {file_name}" 
    return response_text #its a string : https://gpt-index.readthedocs.io/en/latest/guides/primer/usage_pattern.html

       



   

    
