def pretty_func(obj):
    print('Some useful message')


def do_things(obj, self):
    print(self)


class PublicMeta(type):
    def __new__(cls, classname, supers, classdict):
        newdict = {}
        for k, v in classdict.items():
            if k.startswith('_' + classname):
                newattr = k.replace('_' + classname + '__', '')
                newdict[newattr] = classdict.get(k)
        classdict.update(newdict)
        classdict['pretty_func'] = pretty_func
        classdict['do_things'] = do_things
        return type.__new__(cls, classname, supers, classdict)


class A(metaclass=PublicMeta):
    __var = 10

    def __init__(self, x):
        self.x = x


a = A(10)
print(a.var)
a.pretty_func()
a.do_things(10)
