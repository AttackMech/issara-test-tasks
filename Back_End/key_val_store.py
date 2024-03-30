from time import time

TTL = 300 # 300 s = 5 minutes

class KeyValStore:
    def __init__(self):
        self.__data_store = {}

    def set_key(self, key, value, ttl=TTL):
        self.__data_store[key] = {
            'value': value,
            'expiration_time': time() + ttl
        }

    def get_keys(self, keys=None):
        if keys is None:
            keys = list(self.__data_store.keys())

        retrieved_keys = {}
        expiration_time = time() + TTL

        for key in keys:
            if key in self.__data_store:
                if time() < self.__data_store[key]['expiration_time']:
                     retrieved_keys[key] = self.__data_store[key]['value']
                     self.__data_store[key]['expiration_time'] = expiration_time
                else:
                    del self.__data_store[key]

        return retrieved_keys
    
    def check_key(self, key):
        return key in self.__data_store.keys()
            
    def reset_keys(self, keys=None, ttl=TTL):
        if keys is None:
            keys = list(self.__data_store.keys())

        expiration_time = time() + ttl
        
        for key in keys:
            if key in self.__data_store:
                self.__data_store[key]['expiration_time'] = expiration_time

    def remove_expired_keys(self):
        expired_keys = [key for key, value in self.__data_store.items() if time() >= value['expiration_time']]
        for key in expired_keys:
            del self.__data_store[key]
