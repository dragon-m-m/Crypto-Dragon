import pickle, os
from rich.prompt import Prompt
from rich.progress import Progress
from rich import print
from encryption import Encryption
from configs import __version__

class User():
    def __init__(self, password=None):
        password = self.input('Enter Your Password', password, password=True)
        self.enc = Encryption(password)
        login = bool(self.load_database())
        if login is False: exit('The password is wrong.')
        
    def input(self, text, value=None, func=str, **keys):
        while bool(value) is False:
            try:
                value = Prompt.ask(text, **keys)
            except:
                func()
                exit('The app ended!')
        return value.strip()
    
    def load_database(self):
        try:
            with open('database.bin', 'rb') as file:
                data = self.enc.decrypt(file.read())
                data = pickle.loads(data)
        except self.enc.InvalidToken:
            data = False
        except FileNotFoundError:
            data = {'version':__version__, 'keys':{}}
            self.write_database(data)
        return data
    
    def write_database(self, data):
        with open('database.bin', 'wb') as file:
            data = self.enc.encrypt(pickle.dumps(data))
            file.write(data)
    
    def change_password(self, password=None):
        passwd = self.input('Enter your new password', password, password=True)
        data = self.load_database()
        self.enc = Encryption(passwd)
        self.write_database(data)
        return 'The password is changed.'
    
    def load_keys(self):
        keys = self.load_database()['keys']
        return keys
    
    def print_keys(self):
        return 'your keys: ' + ' [green]*[/green] '.join(self.load_keys().keys())
    
    def load_key(self, key_name=None, func=str):
        keys = self.load_keys()
        if key_name not in keys:
            if key_name is not None:
                print(f'The key \'{key_name}\' was not found in your database.')
            key_name = self.input('Enter your key name', func=func, choices=keys.keys())
        key = keys.get(key_name)
        return key_name, key
    
    def create_new_key(self, key_name=None, key=None):
        key_name = self.input('Enter your key name', key_name)
        if type(key) is str:
            key = key.encode()
        elif key is None:
            key = self.enc.generate_key()
        data = self.load_database()
        if (key_name not in data['keys']) and (key not in data['keys'].values()):
            try:
                Encryption(key=key)
                data['keys'][key_name] = key
                self.write_database(data)
                return key
            except:
                return f'Cannot be used \'{key.decode()}\' as key.'
        else:
            return 'error! The key is already available.'
    
    def key_loading_in_file(self, key_name=None, file_name=None):
        key_name, key = self.load_key(key_name)
        if file_name is None: file_name = key_name
        with open(f'{file_name}.key', 'wb') as f:
            f.write(key)
        return 'Operations were performed.'
    
    def add_key_from_file(self, file_name=None, key_name=None):
        file = self.input('Enter Your File Name', file_name)
        if key_name is None:
            key_name = os.path.splitext(os.path.basename(file))[0]
        if os.path.exists(file):
            with open(file, 'rb') as f:
                key = f.readline()
            key = self.create_new_key(key_name, key)
            return key
        else:
            return 'The file is not available.'
    
    def remove_key(self, key_name=None):
        data = self.load_database()
        keys = data['keys'].keys()
        key_name = self.load_key(key_name)[0]
        data['keys'].pop(key_name)
        self.write_database(data)
        return 'Key removed successfully.'
    
    def encryption(self, file=None, key_name=None):
        file = self.input('Enter your file name', file)
        if not os.path.isfile(file):
            return f'The path \'{file}\' is wrong.'
        remove_file = lambda: os.remove(result_file_path)
        file_size = os.stat(file).st_size
        result_file_path = self.enc.rand_name()
        result_file = open(result_file_path, 'ab')
        with open(file, 'rb') as f:
            line = f.readline()
            if 'encrypted' in str(line):
                key_name = line.split()[1].decode()
                key_name, key = self.load_key(key_name, func=remove_file)
                try:
                    self.enc.file_decrypt(key, f, result_file, file_size)
                except self.enc.InvalidToken:
                    result_file.close()
                    remove_file()
                    return 'The key is wrong!'
            else:
                key_name, key = self.load_key(key_name, func=remove_file)
                result_file.write(f'encrypted {key_name} \n'.encode())
                self.enc.file_encrypt(key, f, result_file, file_size)
                result_file.close()
        result_file.close()
        os.rename(result_file_path, file)
        return 'done.'