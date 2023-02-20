import scrypt
from random import choices
from cryptography import fernet
from rich.progress import Progress

class Encryption():
    def __init__(self, passwd=None, key=None):
        self.generate_key = lambda: fernet.Fernet.generate_key()
        self.InvalidToken = fernet.InvalidToken
        self._enc = self.generate_enc(passwd, key)
    
    def generate_enc(self, passwd=None, key=None):
        if passwd != None:
            self.key = self.generate_key_from_passwd(passwd)
        elif key == 'new':
            self.key = self.generate_key()
        else:
            self.key = key
        return fernet.Fernet(self.key)
    
    def generate_key_from_passwd(self, passwd):
        salt = b'aa1f2d3f4d23ac44e9c5a6c3d8f9ee8c'
        key = scrypt.hash(passwd, salt, 2048, 8, 1, 22).hex()
        return f'{key[:43]}='
    
    def rand_name(self):
        characters = 'aa1f2d3f4d23ac44e9c5a6c3d8f9ee8c'
        name = ''.join(choices(characters, k=15))
        return '.' + name
    
    def encrypt(self, data:bytes):
        return self._enc.encrypt(data)
    
    def decrypt(self, data:bytes):
        return self._enc.decrypt(data)
    
    def file_encrypt(self, key:bytes, file, result_file, size):
        enc = self.generate_enc(key=key)
        file.seek(0)
        data = file.read(1000000)
        with Progress() as progress:
            task = progress.add_task('[blue] encrypt...', total=size)
            while data:
                result_file.write(enc.encrypt(data))
                progress.update(task, advance=1000000)
                data = file.read(1000000)
    
    def file_decrypt(self, key:bytes, file, result_file, size):
        enc = self.generate_enc(key=key)
        data = file.read(1333432)
        with Progress() as progress:
            task = progress.add_task('[blue] decrypt...', total=size)
            while data:
                result_file.write(enc.decrypt(data))
                progress.update(task, advance=1333432)
                data = file.read(1333432)