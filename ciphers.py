import random


def reverse(message, method):
    output = message[::-1]
    return output


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


#Missing decrypt method
def horizontal_matrix(message, method, shift):
    x = -1
    actual_list = []
    matrix = []
    output = ''



    for char in message:
        actual_list += char
        if len(actual_list)>=shift:
            matrix += [[i for i in actual_list]]
            actual_list.clear()
    if len(actual_list) != 0:
        matrix += [[i for i in actual_list]]

    if method == 'e':
        while x <= shift:
            x+=1
            for row in matrix:
                try:
                    output += row[x]
                except IndexError:
                    break

    # if method == 'd':
    #     d_matrix = []
    #     for row in matrix:
    #         d_matrix += [[]]

    #     while x <= shift:        
    #         x += 1
    #         for row in matrix:
    #             for d_row in d_matrix:
    #                 d_row += row[x]

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