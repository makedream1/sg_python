import re

first_list = ['fu', 'tofu', 'snafu', 'dsds']
second_list = ['futz', 'fusillade', 'functional', 'discombobulated']

regexp = re.compile(r'.*fu\b')


def func(x):
    for i in x:
        res = regexp.findall(i)
        if res:
            print(i)


func(first_list)
func(second_list)
