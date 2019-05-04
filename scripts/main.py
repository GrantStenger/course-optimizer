
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

if __name__ == "__main__":
    # prefixes = get_prefixes()
    # titles = get_full_titles()
    #
    # for i in range(len(prefixes)):
    #     print(prefixes[i], titles[i])
    add_comma()
