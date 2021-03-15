import argparse, unidecode, random, subprocess
from sys import platform
import ciphers as cipher


def get_arguments():
    parser = argparse.ArgumentParser(prog="Liandr4's Crypt")
    parser.add_argument('message', help='Mandatory, a message to be encrypted or decrypted, please use quotes if has any special character or spaces.')
    parser.add_argument('cipher', nargs=1, choices=['e','d'], help='Choose wether to (e)ncrypt or (d)ecrypt given message.')
    parser.add_argument('method', nargs ='*', choices =['a','r','c', 'n', 'h', 'v', 'ra'], help='Method to be used, can choose many, separating them with spaces. Order of choosing is respected.')
    parser.add_argument('-s', '--shift', nargs=1, help="Can be used with Caesar's Cipher to define how long to jump.", default=3)
    parser.add_argument('-hs', '--horizontal_shift', nargs=1, help="Same as shift, but to define when to break words in horizontal matrix", default=4)
    parser.add_argument('-pw', '--preserve_whitespaces', action='store_true', help="Use it to preserve whitespaces. Keep in mind that this may alter the result with a few methods like alternate and colunar transposition, thus being need to passed as argument when decrypting.")
    parser.add_argument('-k', '--key', nargs='*', help="Specify a key to decrypt messages in key-based decryption")
    parser.add_argument('-o', '--output', nargs=2, help="Saves it to a external file. The first argument is for location, the other one to the method (w)rite or (a)ppend.")
    parser.add_argument('-i', '--input', action='store_true', help="Open an external file and use it as message, type the location as an argument for message")
    parser.add_argument('--clear', action='store_true')

    arguments = parser.parse_args()
    return arguments

args = get_arguments()
final_message = ''

if args.input:
    try:
        message = open(args.message, 'r')
        for i in message:
            final_message += str(i)
    except:
        print("Couldn't open the given file! Make sure you have permissions, and typed the path and name correctly!")
        exit()
else:
    final_message = args.message

final_message = unidecode.unidecode(final_message)

if args.preserve_whitespaces == False:
    final_message = final_message.replace(' ','')

code = ''.join(args.cipher)

if args.shift!=3:
    shift = int(''.join(args.shift))
else:
    shift = args.shift

if args.horizontal_shift != 4:
    h_shift = int(''.join(args.horizontal_shift))
else:
    h_shift = args.horizontal_shift

print(args)
key = None

for m in args.method:
    if m == 'r':
        final_message = cipher.reverse(final_message, code)
    elif m == 'c':
        final_message = cipher.caesar(final_message, code, shift)
    elif m == 'n':
        final_message = cipher.char_num(final_message, code)
    elif m == 'h':
        final_message = cipher.horizontal_matrix(final_message, code, h_shift)
    elif m == 'a':
        final_message = cipher.alternate(final_message, code)
    elif m == 'ra':
        final_message, key = cipher.random_key(final_message, code, args.key)

if args.clear == True:
    try:

        if platform.startswith('win32'):
            subprocess.run("cls", shell=True, check=True)
        else:
            subprocess.run("clear", shell=True, check=True)
    except subprocess.CalledProcessError as error:
        print(f"\n> Not possible to clear screen! \n> Error: {error} ")
    except:
        print("For some reason, it wasn't possible to clear screen!")
    
print(f'\n{final_message}\n')

if key != None:
    print(key)

if args.output:
    try:
        file = open(args.output[0], args.output[1])
        file.write(f'{final_message}\n')
    except IsADirectoryError:
        print("\n> Couldn't save the file! Make sure you provided the right location. Ex.:'/home/john/test.txt'")
    except ValueError:
        print("\nCouldn't save the file! Wrong value set for operation mode, choose (w)rite or (a)ppend.")
    except PermissionError:
        print("\n> Couldn't save the file! It seems you don't have permission to do so.")
    except:
        print("\n> Something went wrong, but I'm not sure what!")
    finally:
        file.close()

