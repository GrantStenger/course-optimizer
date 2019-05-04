import json

def get_prefixes():
    r_file = open('prefixes.txt', 'r')
    prefixes = []
    line = r_file.readline()
    while line:
        to_write = (line.split('">'))[1].split('</')[0]
        prefixes.append(to_write)
        line = r_file.readline()
    r_file.close()
    return prefixes

def get_full_titles():
    r_file = open('full_titles.txt', 'r')
    titles = []
    line = r_file.readline()
    while line:
        to_write = (line.split('">'))[1].split('</')[0]
        titles.append(to_write)
        line = r_file.readline()
    r_file.close()
    return titles

def add_comma():
    r_file = open('departments.txt', 'r')
    w_file = open('new_departments.txt', 'w')
    line = r_file.readline()
    while line:
        to_write = line.split(' ')[0] + ', ' + str(' '.join(line.split(' ')[1:]))
        w_file.write(to_write)
        line = r_file.readline()
    r_file.close()
    w_file.close()

def depts_to_json():
    r_file = open('departments.txt', 'r')
    data = []
    line = r_file.readline()
    while line:
        course = {}
        course['prefix'] = line.split(' ')[0]
        course['title'] = str(' '.join(line.split(' ')[1:]))[:-1]
        data.append(course)
        line = r_file.readline()
    r_file.close()

    with open('departments.json', 'w') as w_file:
        json.dump(data, w_file)

if __name__ == "__main__":
    with open("../data/depts_pretty.json", "r") as read_file:
        data = json.load(read_file)
    data_str = json.dumps(data, indent=2)
    print(data_str)
    for course in data:
        print(course['title'])
