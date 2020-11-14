from bs4 import BeautifulSoup
from urllib.parse import urlsplit
from re import compile, findall
from itertools import chain

with open("sample.html") as fp:
    soup = BeautifulSoup(fp, 'lxml')


def inline_style(soup):
    intag_style = {
        'attrs': {
            'style': True
        }
    }
    inline_style = {
        'name': 'style'
    }

    summ = 0

    intag = soup.body.find_all(**intag_style)
    for tag in intag:
        summ += len(tag["style"])

    inline = soup(**inline_style)
    for i in inline:
        for s in i.children:
            summ += len(s)

    return summ


def len_text(soup):
    inline_text = {
        'string': True
    }
    inline = soup(**inline_text)
    return sum([len(i) for i in inline])


def number_external_src(soup):
    ext = [
        {
            'name': 'link',
            'attrs': {
                    'href': True}
        },
        {
            'attrs': {
                'src': True
            }
        }
    ]
    src = list(chain.from_iterable([soup(**i) for i in ext]))
    return len(src)
    """return {
        'length': len(src),
        'list': src
    }"""


def number_int_ext_links(soup, base=None):
    baseq = {
        'name': 'base',
        'attrs': {
            'href': True
        }
    }
    baseqr = soup.find(**baseq)
    if not base and baseqr:
        base = baseqr['href']

    extreg = compile('^(?!#).*$')
    intreg = compile('^#.*')
    linkq = [
        {
            'name': 'a',
            'attrs': {
                    'href': extreg
            }
        },
        {
            'name': 'area',
            'attrs': {
                    'href': extreg
            }
        },
        {
            'name': 'a',
            'attrs': {
                    'href': intreg
            }
        },
        {
            'name': 'area',
            'attrs': {
                    'href': intreg
            }
        }
    ]
    links = [soup(**i) for i in linkq]
    internal = []
    external = []
    if base:
        base = urlsplit(base).netloc

    for lin in links[0:2]:
        for li in lin:
            if base and base == urlsplit(li['href']).netloc:
                internal.append(li)
            else:
                external.append(li)

    for lin in links[2:]:
        for li in lin:
            internal.append(li)

    return [len(internal), len(external)]
    """return {
        'internal': {
            'lenght': len(internal),
            'list': internal,
        },
        'external': {
            'lenght': len(external),
            'list': external,
        },
    }"""

def number_of_tokens(soup, token, i=0):
    file_text = soup.prettify()
    return file_text.count(token)
    

print(number_int_ext_links(soup))

print(number_external_src(soup))

print(len_text(soup))

print(inline_style(soup))

print(number_of_tokens(soup, " "))
