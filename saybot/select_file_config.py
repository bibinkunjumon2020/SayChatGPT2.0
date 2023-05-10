from saybot import logging

class SelectFileClass:
    
    select_file_id = None
    
    def __init__(self):
        pass


    def set_select_file_id(new_file_id):
        logging.info("Inside set_select_file_id")
        SelectFileClass.select_file_id = new_file_id
    
    def get_select_file_id():
        logging.info("Inside get_select_file_id")
        return SelectFileClass.select_file_id
