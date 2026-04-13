import bs4, re
import functools


def pipe(data, funcs):
    return functools.reduce(lambda i, f: f(i), funcs, data)

def clear_string(s: str) -> str:
    return s.strip().replace("\n", "").replace("\t", "").replace("  ", "")

def is_header(element: bs4.BeautifulSoup) -> bool:
    if element.name == "h1":
        return True
    elif element.name == "div":
        classes = element.get("class", [])
        return re.match("(title|heading|header)", "".join(classes))
    return False