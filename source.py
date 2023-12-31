from abc import ABC, abstractmethod
import pickle
import shutil
import os

class ErrorPermission(Exception):
    pass

class Data_storage(ABC):
    @abstractmethod
    def save(self, data):
        pass
    
    @abstractmethod
    def load(self, identifier):
        pass
    
    @abstractmethod
    def delete(self, identifier):
        pass

#ays obektnery karox enq stexcel miayn mek angam ete erkrord angam stexcenq Database_storage kam File_storage type-i obektner apa nranq bolory khxven hishoxutyan nuyn hascei vra

#ays class-ov stexcum enq obektner vorpes parametr poxancelov ayn pickle file-i anuny vory gtnvum e 'current directory'-um ev linelu e himnakan database-y
class Database_storage(Data_storage):
    __instance = None
    __countData = 0

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self, file_path):
        if not hasattr(self, "_" + self.__class__.__name__ + "__file_path"):
            self.__file_path = file_path
            try:
                with open(self.__file_path, "rb") as file:
                    existing_data = pickle.load(file)
                    if existing_data:
                        self.__countData = len(existing_data)
            except (FileNotFoundError, EOFError):
                print("There are problems opening the file!!")
    
    def save(self, data):
        existing_data = []
        try:
            with open(self.__file_path, "rb") as file:
                existing_data = pickle.load(file)
        except EOFError as err:
            print(str(err))
        except FileNotFoundError:
            print("There are problems opening the file!!")
            return None
        existing_data.append(data)
        
        with open(self.__file_path, "wb") as file:
            pickle.dump(existing_data, file)

        self.__countData += 1
        
         
    def load(self, index):
        try:
            with open(self.__file_path, "rb") as file:
                return pickle.load(file)[index]
        except (FileNotFoundError, EOFError):
            print("There are problem__getattribute__s opening the file!!")
    
    def delete(self, index):
        existing_data = []
        try:
            with open(self.__file_path, "rb") as file:
                existing_data = pickle.load(file)
        except (FileNotFoundError, EOFError):
            print("There are problems opening the file!!")
        if existing_data:
            del existing_data[self.__countData - 1]
            self.__countData -= 1
            with open(self.__file_path, "wb") as file:
                pickle.dump(existing_data, file)

    @property
    def count(self):
        return self.__countData

#ays class-ov stexcum enq obekt nran vorpes parametr poxancelov ayn dir-y vortex pahelu enq file-ery kam folder-nery

class File_storage(Data_storage):
    __instance = None
    __countFiles = 0#aystex pahvum e __destination-um exac file-eri kam folder-neri yndhanur qanaky

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    def __init__(self, destination):
        if not hasattr(self, "_" + self.__class__.__name__ + "__destination"):
            self.__destination = destination
            try:
                self.__countFiles = len(os.listdir(self.__destination))
            except:
                print("There are problems opening the folder!!")

            
    def save(self, data_link):#poxancum enq ayn file-i kam folder-i link-y vory anhrajesht e pahpanel __destination-um
        try:
            shutil.move(data_link, self.__destination)
            self.__countFiles += 1
        except:
            print("There are problems opening the folder!!")
    
    def load(self, index):#stanum enq yst __destination-um dasavorutyan index-rd file-y kam folder-y(anuny miayn)
        try:
            return os.listdir(self.__destination)[index] 
        except:
            print("There are problems opening the folder!!")
    def delete(self, index):#jnjum enq index-rdy __destination-ic
        try:
            path = self.__destination + "/" + self.load(index)
            if os.path.isdir(path):
                shutil.rmtree(path)
            elif os.path.isfile(path):
                os.remove(path)
            self.__countFiles -= 1
        except:
            print("There are problems opening the folder!!")

    @property
    def count(self):
        return self.__countFiles



