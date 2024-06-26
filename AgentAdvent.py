from random import shuffle
import os

num_drawing = 1
results = {}


def main():
    directory = get_directory()
    file_data = get_file_data( directory )
    hat = list(file_data.keys())
    shuffle(hat)

    # Will add information into file_data[person]
    # Each person will have appended their draw
    draw_names( file_data, hat )
    create_personal_files( file_data )
    create_next_years_files( file_data, str(int(directory)+1) )


def get_directory() -> str:
    '''Asks the user for the year the drawing is for and returns it as a str'''
    year = 0
    while year < 2000:
        year = int(input("What year do you want to draw names for? "))
    
    return str(year)


def get_file_data( directory: str ) -> dict:
    ''' looks for a local folder titled 'directory' and opens
    a file it contains called 'hat.txt'. This file should 
    contain the following.
    person_drawing/linked_people/recently_drawn_people.
    The sections are separated with slashes and the people in a 
    section are comma separated. This information is parsed and
    returned as a dict of the form
    person_drawing -> [[linked_people], [recently_drawn_people]]
    '''
    os.chdir("./"+directory)

    file_data = {}

    with open('hat.txt', 'r') as hat:
        for line in hat:
            line = line.split('/')
            file_data[line[0]] = [line[1].split(','), line[2].strip().split(',')]
    
    return file_data


def draw_names(file_data: dict, hat: list[str]) -> bool:
    for person in file_data:
        if len(file_data[person]) < 3:
            success = False
            for name in hat:
                if allowed_to_draw(file_data, person, name):
                    hat.remove(name)
                    file_data[person].append(name)
                    success = draw_names(file_data, hat)
                    if success:
                        break
                    hat.append(name)
                    file_data[person].pop()
            return success
    return True


def allowed_to_draw(file_data: dict, person: str, name: str) -> bool:
    return name != person and \
        name not in file_data[person][0] and \
        name not in file_data[person][1]


def create_personal_files(file_data: dict) -> None:
    os.mkdir('Results')
    os.chdir('./Results')
    for person in file_data:
        with open(person+'.txt', 'w') as personal_file:
            personal_file.write(file_data[person][2])


def create_next_years_files(file_data: dict, directory: str) -> None:
    os.chdir('../..')
    os.mkdir( directory )
    os.chdir( './' + directory )
    with open('hat.txt', 'w') as new_hat:
        for person in file_data:
            output_str = person + '/'
            for link in file_data[person][0]:
                output_str += link + ','
            output_str = output_str[:-1] # remove excess comma
            output_str += f'/{file_data[person][1][-1]},{file_data[person][2]}\n'
            new_hat.write(output_str)


if __name__ == '__main__':
    main()
