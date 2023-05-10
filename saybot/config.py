
from saybot import generate_chat,generate_response,generate_image
from saybot.generate_from_document import generate_response_from_userdoc

class ConfigClass:
    model_selection_command = "chatgpt"  # default model
    model_list_dictionary={ # these all prompt responding methods
        'chatgpt':generate_chat,
        'davincigpt':generate_response,
        'dall.e2':generate_image,
        'askyourbook':generate_response_from_userdoc,
        }
    def __init__(self):
        pass

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
    