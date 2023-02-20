
def __help__(switch=None):
    help = {
    'switches': {'-e', '-p', '-c', '-r', '-l', '-a', '-k'},
    None:'''
    How to use: python main.py --help 'name switch'
    
    -e : File encryption 'default'
    -p : change password.
    -c : create new key.
    -r : remove key.
    -l : key loading in file.
    -a : add key from file.
    -k : Display existing keys.
    ''',
    '-e':'''
  With this switch, you can encrypt or decrypt your files.
  How to use: python main.py -e 'file path' 'key name'
  Note this is the default switch.
    ''',
    '-p':'''
  With this switch, you can change your password.
  How to use: python main.py -p 'new password'
    ''',
    '-c':'''
  With this switch, you can create a new key to encrypt.
  How to use: python main.py -c 'new key name'
    ''',
    '-r':'''
  With this switch, you can delete a key from your keys list.
  How to use: python main.py -r 'key name'
    ''',
    '-l':'''
  With this switch, you can save a key in the file.
  How to use: python main.py -l 'key name' 'file name'
    ''',
    '-a':'''
  With this switch, you can add a key from the file to your keys list.
  How to use: python main.py -a 'path file' 'key  name'
    ''',
    '-k':'''
  With this key you can see your keys.
  How to use: python main.py -k
    '''}
    return help.get(switch, help[None])

__welcome__ = 'Welcome to Crypto Dragon.'
__version__ = '1.0.0'
