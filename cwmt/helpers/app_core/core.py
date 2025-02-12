from cwmt.helpers.app_core.logger import Logger

class AppCore:
    
    def __init__(self):
        self.logger = Logger()

    def show_attributes(self):
        print("*"*80)
        print(self.__dict__)
    