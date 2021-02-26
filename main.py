import argparse, unidecode, random, subprocess
from sys import platform

'''
r = reverse
c = caesar
n = numbers
h = horizontal matrix
v = vertical matrix
ra = random
'''

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


#Nesse caso o argumento método é puramente para padronização, pois se revertendo a palavra já revertida, se chega a original.
def reverse(message, method):
    output = message[::-1]
    return output


#O shift nn é obrigatório aqui, já que se omitido no parser, o default é 3, porém, também definindo no parser, é possível brincar com outras transições.
def caesar(message, method, shift):
    output = ''
    if method == 'e':
        for char in message:
            if char.isupper():
                new_char = chr((ord(char) + shift - 65) % 26 + 65)
                output += new_char
            elif char.islower():
                new_char = chr((ord(char) + shift - 97) % 26 + 97)
                output += new_char
            elif char.isdigit():
                new_char = chr((ord(char) + shift - 48) % 10 + 48)
                output += new_char
            else:
                output += char
    
    elif method == 'd':
        for char in message:
            if ord(char) in range (65, 122):
                if char.isupper():
                    new_char = chr((ord(char) - shift - 65) % 26 + 65)
                    output += new_char
                elif char.islower():
                    new_char = chr((ord(char) - shift - 97) % 26 + 97)
                    output += new_char
                elif char.isdigit():
                    new_char = chr((ord(char) - shift - 48) % 10 + 48)
                    output += new_char
            else:
                output += char

    return output


def alternate(message, method):
    output = ''
    list_message = message.split(' ')
    list_final_message = []
    x = 0
    y = 1
    for i in list_message:
        while len(output) < len(i):
            try:
                output += str(i[y])
                output += str(i[x])
                x += 2
                y += 2
            except IndexError:
                output += str(i[x])
                break
        x = 0
        y = 1
        list_final_message.append(output)
        output = ''
    
    return ' '.join(list_final_message)



def char_num(message, method):
    char_to_num = {'a':'1', 'b':'2', 'c':'3', 'd':'4', 'e':'5', 'f':'6', 'g':'7', 'h':'8', 'i':'9', 'j':'10', 'k':'11', 'l':'12', 'm':'13', 'n':'14', 'o':'15', 'p':'16', 'q':'17', 'r':'18', 's':'19', 't':'20', 'u':'21', 'v':'22', 'w':'23', 'x':'24', 'y':'25', 'z':'26'}
    num_to_char = {'1':'a', '2':'b', '3':'c', '4':'d', '5':'e', '6':'f', '7':'g', '8':'h', '9':'i', '10':'j', '11':'k', '12':'l', '13':'m', '14':'n', '15':'o', '16':'p', '17':'q', '18':'r', '19':'s', '20':'t', '21':'u', '22':'v', '23':'w', '24':'x', '25':'y', '26':'z'}
    message = message.lower()
    output = ''

    if method == 'e':
        for char in message:
            new_char = char_to_num.get(char, char)
            output += new_char + ' '

    elif method == 'd':
        split_message = message.split(' ')
        for char in split_message:
            if char == '' and output[-1]!= ' ':
                output += ' '
            else:
                new_char = num_to_char.get(char, char)
                output += new_char

    return output


#Falta fazer decriptação
def horizontal_matrix(message, method, shift):
    shift = shift - 1
    x = -1
    actual_list = []
    matrix = []
    output = ''



    for char in message:
        actual_list += char
        if len(actual_list)>shift:
            matrix += [[i for i in actual_list]]
            actual_list.clear()
    if len(actual_list) != 0:
        matrix += [[i for i in actual_list]]

    if method == 'e':
        while x < shift:
            x+=1
            for row in matrix:
                try:
                    output += row[x]
                except IndexError:
                    break

            
    return output


def random_key(message, code, key):
    message_list = [i for i in message]
    possible_key_numbers = [i for i in range(0, len(message_list))]
    output = ''
    x = 0

    if code == 'e':
        key = ''
        for i in range(0,len(possible_key_numbers)):
            x = random.choice(possible_key_numbers)
            possible_key_numbers.remove(x)
            output += message_list[x]
            key += f' {str(x)}'
            key = key.strip()

    elif code == 'd':
        try:
            position = -1
            key = [int(i) for i in key]
            while x < max(key):
                for i in key:
                    if i == x:
                        position = key.index(i)
                        output += message_list[position]
                        x+=1
        except IndexError:
            return("\n> Please make sure you entered the right message, key and space preservation. IndexError: out of range")
        except:
            return("\n> Something went wrong, but I'm not sure what! Please review your command line.")

    output = output.strip()
    return output, key

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
#Segue, na ordem exata, os métodos requisitados pelo usuário distinguindo se deve ser feita encriptação ou decriptação
for m in args.method:
    if m == 'r':
        final_message = reverse(final_message, code)
    elif m == 'c':
        final_message = caesar(final_message, code, shift)
    elif m == 'n':
        final_message = char_num(final_message, code)
    elif m == 'h':
        final_message = horizontal_matrix(final_message, code, h_shift)
    elif m == 'a':
        final_message = alternate(final_message, code)
    elif m == 'ra':
        final_message, key = random_key(final_message, code, args.key)


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

#I know that argparse have it's way to file handling, but I'd think it was best if I did from scratch
if args.output:
    try:
        file = open(args.output[0], args.output[1])
        file.write(f'{final_message}\n')
        file.close()
    except IsADirectoryError:
        print("\n> Couldn't save the file! Make sure you provided the right location. Ex.:'/home/john/test.txt'")
    except ValueError:
        print("\nCouldn't save the file! Wrong value set for operation mode, choose (w)rite or (a)ppend.")
    except PermissionError:
        print("\n> Couldn't save the file! It seems you don't have permission to do so.")
    except:
        print("\n> Something went wrong, but I'm not sure what!")

