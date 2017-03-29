import html


def writer(key_string: str) -> object:
    def writer_decorator(func):
        def wrapper(s):
            for item in key_string:
                try:
                    func_name = eval("html_{}".format(item))
                    s = func_name(s)
                except NameError:
                    pass
            return func(s)

        return wrapper

    return writer_decorator


def html_p(s: str) -> str:
    new_s = '<p>{}<p>'.format(s)
    return new_s


def html_b(s: str) -> str:
    new_s = '<b>{}<b>'.format(s)
    return new_s


def html_i(s: str) -> str:
    new_s = '<i>{}<i>'.format(s)
    return new_s


def html_u(s: str) -> str:
    new_s = '<u>{}<u>'.format(s)
    return new_s


@writer('bpx')
def html_printer(s: str) -> str:
    return html.escape(s)


print(html_printer("I'll give you +++ cash for this -> stuff."))
