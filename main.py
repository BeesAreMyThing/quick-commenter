from tkinter import Tk


def get_text():
    with open('comments.txt', 'r') as a_file:
        raw_text = a_file.readlines()
    return raw_text


def remove_n(text_list):
    new_list = []
    for line in text_list:
        new_list.append(line.strip())
    return new_list


def keyed_dict(text_list, keyword):
    a_dict = {}
    for line in text_list:
        if line.startswith(keyword):
            next_key = line.replace(keyword,'')
            a_dict[next_key] = []
        else:
            a_dict[next_key].append(line)
    return a_dict


def sub_dict(big_dict, keyword):
    result_dict = {}
    for key, value in big_dict.items():
        try:
            result_dict[key] = keyed_dict(value, keyword)
        except UnboundLocalError:
            result_dict[key] = value
    return result_dict


def get_data():
    main_text = remove_n(get_text())
    main_dict = keyed_dict(main_text, "Main - ")
    main_dict = sub_dict(main_dict, "Sub - ")
    return main_dict


def to_clipboard(text):
    comp = Tk()
    comp.withdraw()
    comp.clipboard_clear()
    comp.clipboard_append(text)


def print_list(a_list):
    for index, line in enumerate(a_list):
        print('\t{}: {}'.format(index, line))


def main():
    done = False
    main_dict = get_data()

    memory = main_dict
    lowest_level = False
    print('Welcome to the auto-commenter!\n')
    print("To access headings and subheadings input its first letter.")
    print("To copy a comment to the clipboard, enter its number.")
    print('Input "clear" to return to the main menu.')
    print('Input "refresh" to update the menus if you change the '
          '"comments.txt" source file.\n')

    while not done:
        if memory == main_dict:
            print('\nMain Headings:')
            print('\t',[key for key in memory.keys()])
        user_input = input('\n>>> ').lower()

        if not lowest_level:
            for char in user_input:
                for heading in memory.keys():
                    if heading[0].lower() == char:
                        memory = memory[heading]
                        try:
                            memory.keys()
                            current_heading = heading
                            print('{} Subheadings:'.format(current_heading))
                            print('\t',[key for key in memory.keys()])
                        except AttributeError:
                            print('Comments:')
                            print_list(memory)
                            lowest_level = True
        else:
            try:
                new_message=''
                for char in user_input:
                    if char == " ":
                        new_message += '\n'
                    else:
                        num = int(char)
                        new_message += memory[num] + ' ' 
                print('Copied: ', new_message, '\n')
                to_clipboard(new_message)
                try:
                    memory = main_dict[current_heading]
                    print('{} Subheadings:'.format(current_heading))
                    print('\t',[key for key in memory.keys()])
                except (UnboundLocalError, KeyError):
                    memory = main_dict
                
                lowest_level = False
            except ValueError:
                print('Invalid input.')
                num = None

        if user_input in ['quit']:  
            done = True
        if user_input == 'refresh':
            print('Data refreshed')
            main_dict = get_data()
            memory = main_dict
        if user_input in ['clear', 'del','','main']:
            print('Memory cleared')
            current_heading = None
            lowest_level = False
            memory = main_dict
main()





