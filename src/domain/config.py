import configparser

class Config:
    def __init__(self, path_to_config):
        self.path_to_config = path_to_config
        self.config = configparser.ConfigParser()
        self.config.read(self.path_to_config)            

    @property
    def db_connection(self):
        try:
            return self.config["Database"]["ASYNC_DATABASE_URL"]
        except Exception as ex:
            raise ex    
        
    @property
    def tg_api_key(self):
        try:
            return self.config["Telegram"]["API_KEY"]
        except Exception as ex:
            raise ex    
 
    @property
    def node_url(self):
        try:
            return self.config["Blockchain"]["NODE_URL"]
        except Exception as ex:
            raise ex    
        
    @property
    def target_contract(self):
        try:
            return self.config["Blockchain"]["TARGET_CONTRACT"]
        except Exception as ex:
            raise ex    
        
    @property
    def erc_20_abi(self):
        try:
            return self.config["Blockchain"]["ERC_20_TRANSFER_ABI"]
        except Exception as ex:
            raise ex       