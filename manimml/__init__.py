from telnetlib import EL
from manimlib import *
# from manimml.mock import *
from xml.etree.ElementTree import ElementTree, Element
from functools import reduce


# Manim Markup Language
class ManimML:
    def __init__(self, *args, scene: Scene, file: str, data: dict = {}):
        self.objs = []
        self.ids = dict()
        self.classes = dict()
        self.data = data

        dom = ElementTree(file=file).getroot()
        for child in dom:
            self.parse_node(child)

    def parse_kwargs(self, expr: str) -> tuple:
        """
        Examples:
            "5" -> [5], {}
            "1, 2, num=3" -> [1, 2], {'num': 3}
        """
        if not isinstance(expr, str):
            return [], {}
        # return eval('[' + expr + ']', None, self.data), {}

        comma_indices = []
        index = len(expr)
        depth = 0
        arr = ''
        dic = ''
        is_literal = False # TODO: case when delimiters contained in string literal

        # break string into arr (args part) and dict (kw part)
        for i, c in enumerate(expr):
            if c in '([{' and not is_literal:
                depth += 1
            elif c in ')]}' and not is_literal:
                depth -= 1
            elif c == ',' and depth == 0:
                comma_indices.append(i)
            elif c == '=' and depth == 0 and i > 0 and expr[i-1] not in '!><=+-*/%^':
                index = comma_indices[-1]
                break
        arr, dic = expr[:index], expr[index+1:]

        # parse dict
        dic_buf = []
        i = 0
        while i < len(dic):
            c = dic[i]
            if c in '([{' and not is_literal:
                depth += 1
                dic_buf.append(c)
            elif c in ')]}' and not is_literal:
                depth -= 1
                dic_buf.append(c)
            elif c == ',' and depth == 0:
                comma_indices.append(i)
                dic_buf.append(c)
            elif c == '=' and depth == 0 and expr[i-1] not in '!><=+-*/%^':
                dic_buf[-1] = '"' + dic_buf[-1] + '"'
                dic_buf.append(':')
            elif c.isalpha() or c == '_':
                buf = [c]
                for d in dic[i+1:]:
                    if d.isalnum() or d == '_':
                        buf.append(d)
                    else:
                        break
                identifier = ''.join(buf)
                dic_buf.append(identifier)
                i += len(identifier) - 1
            else:
                dic_buf.append(c)
            i += 1

        dic = ''.join(dic_buf)
        # eval(expr, globals, locals)
        return eval('[' + arr + '], {' + dic + '}', None, self.data)

    def parse_value(self, expr: str) -> object:
        if not isinstance(expr, str):
            return None
        return eval(expr, None, self.data)

    def parse_args(self, node: Element) -> list:
        if node.tag == 'Text' and 'args' not in node.attrib:
            return [node.text] # some grammar sugar
        else:
            expr = node.attrib.get('args', '')
            return self.parse_value('[' + expr + ']')

    def parse_kw(self, node: Element) -> dict:
        preserved_attrs = {'id', 'class', 'args'}
        kw = {}
        for attr in node.attrib:
            if attr not in preserved_attrs and '.' not in attr:
                expr = node.attrib.get(attr, None)
                kw[attr] = self.parse_value(expr)
        return kw

    def parse_node(self, node: Element) -> Mobject:

        # create object
        constructor = eval(node.tag)
        if node.tag == 'VGroup':
            args = [self.parse_node(child) for child in node]
        else:
            args = self.parse_args(node)
        kw = self.parse_kw(node)
        obj = constructor(*args, **kw)

        # save object
        self.objs.append(obj)

        # save object id
        id = node.attrib.get('id', None)
        if id:
            self.ids[id] = obj

        # save object to classes
        className = node.attrib.get('class', None)
        if className:
            for key in className.split():
                arr = self.classes.get(key, [])
                arr.append(obj)
                self.classes[key] = arr

        # set attrs / call methods on obj
        for attr in node.attrib:
            if attr.startswith('call.'):
                method = getattr(obj, attr[5:])
                expr = node.attrib.get(attr, None)
                args, kw = self.parse_kwargs(expr)
                method(*args, **kw)
            elif attr.startswith('attr.'):
                path = attr[5:].split('.')
                context = reduce(getattr, path[:-1], obj)
                expr = node.attrib.get(attr, True) # attr value defaults to True
                args, kw = self.parse_kwargs(expr)
                setattr(context, path[-1], args[0]) # take args[0] and ignore others

        return obj
        
    def __getitem__(self, key: str) -> Mobject or tuple:
        if isinstance(key, str):
            return self.ids[key]
        elif isinstance(key, tuple):
            return (self.ids[id] for id in key)
        else:
            raise TypeError('key must be str or tuple')
