import configs
from rich import print
from database import User
from argument import value, switch

print(configs.__welcome__)
print('version:', configs.__version__)

if switch in configs.__help__('switches'):
    user = User('')
    commends = {
    '-e': user.encryption,
    '-p': user.change_password,
    '-k': user.print_keys,
    '-c': user.create_new_key,
    '-r': user.remove_key,
    '-l': user.key_loading_in_file,
    '-a': user.add_key_from_file,
    }
    try:
        print(commends.get(switch)(*value))
    except TypeError:
        print(configs.__help__(switch))
else:
    print(configs.__help__(*value))