
from saybot import generate_chat,generate_response,generate_image
from saybot.generate_from_document import generate_response_from_userdoc

class ConfigClass:
    model_selection_command = "gpt-3.5-turbo"  # default model
    model_list_dictionary={
        'gpt-3.5-turbo':generate_chat,
        'text-davinci-003':generate_response,
        'dall.e2':generate_image,
        'askyourbook':generate_response_from_userdoc,
        }
    # select_file_id = None
    def __init__(self):
        pass


    # def set_select_file_id(new_file_id):
    #     ConfigClass.select_file_id = new_file_id
    
    # def get_select_file_id():
    #     return ConfigClass.select_file_id

    def set_model_selection_command(new_model):
        ConfigClass.model_selection_command = new_model

    def get_model_selection_command():
        return ConfigClass.model_selection_command
    
    def set_model_list_dictionary(key,value):
        ConfigClass.model_list_dictionary.update({key:value})
        
    def get_model_list_dictionary(key):
        return ConfigClass.model_list_dictionary.get(key)
    
    def current_model_function(self):
        func = ConfigClass.get_model_list_dictionary(ConfigClass.get_model_selection_command())
        return func
    