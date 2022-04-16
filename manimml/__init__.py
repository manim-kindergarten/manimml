from manimlib import *
# from manimml.mock import *
from xml.etree.ElementTree import ElementTree, Element
from functools import reduce


# Manim Markup Language
class ManimML:
    preserved_attrs = {'id', 'class', 'args', 'always_redraw'}
    sugar_tags = {'Text', 'Tex', 'TexText'}
    def __init__(self, *args, file: str, data: dict = {}):
        self.objs = []
        self.ids = dict()
        self.classes = dict()
        self.data = {}
        self.data.update(data) # copy data

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
                index = comma_indices[-1] if len(comma_indices) else -1
                break
        if index == -1:
            arr, dic = '', expr
        else:
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
        return self.parse_value('[' + arr + '], {' + dic + '}')

    def parse_value(self, expr: str) -> object:
        if not isinstance(expr, str):
            return None
        # eval(expr, globals, locals)
        return eval(expr, None, self.data) # 后面的 xml 可以引用前面的 id

    def parse_args(self, node: Element) -> list:
        if 'args' not in node.attrib and node.tag in ManimML.sugar_tags:
            return [node.text] # some grammar sugar
        else:
            expr = node.attrib.get('args', '')
            return self.parse_value('[' + expr + ']')

    def parse_kw(self, node: Element) -> dict:
        kw = {}
        for attr in node.attrib:
            if attr not in ManimML.preserved_attrs and '.' not in attr:
                expr = node.attrib.get(attr, None)
                kw[attr] = self.parse_value(expr)
        return kw

    def save(self, obj: Mobject, id: str):
        self.objs.append(obj)
        if id:
            self.ids[id] = obj
            self.data[id] = obj

    def parse_node(self, node: Element) -> Mobject:

        # find constructor, args, kw
        constructor = eval(node.tag, None, self.data)
        if node.tag == 'VGroup':
            args = [self.parse_node(child) for child in node]
        else:
            args = self.parse_args(node)
        kw = self.parse_kw(node)

        # create object
        if node.attrib.get('always_redraw', False):
            obj = always_redraw(constructor, *args, **kw)
        else:
            obj = constructor(*args, **kw)

        # save object
        self.save(obj, node.attrib.get('id', None))

        # save object to classes
        className = node.attrib.get('class', None)
        if className:
            for key in className.split():
                arr = self.classes.get(key, [])
                arr.append(obj)
                self.classes[key] = arr

        self.parse_attr(node, obj)
        return obj

    def invoke(self, obj: Mobject, attr: str, expr: str):
        # invoke method on obj
        method = getattr(obj, attr)
        if attr == 'copy':
            self.save(method(), expr)
        else:
            args, kw = self.parse_kwargs(expr)
            method(*args, **kw)

    def parse_attr(self, node: Element, obj: Mobject):
        # set attrs / call methods on obj
        for attr in node.attrib:
            if attr.startswith('call.'):
                expr = node.attrib.get(attr, None)
                self.invoke(obj, attr[5:], expr)
            elif attr.startswith('attr.'):
                path = attr[5:].split('.')
                context = reduce(getattr, path[:-1], obj)
                expr = node.attrib.get(attr, True) # attr value defaults to True
                args, kw = self.parse_kwargs(expr)
                setattr(context, path[-1], args[0]) # take args[0] and ignore others
            elif attr.startswith('calleach.'):
                expr = node.attrib.get(attr, None)
                args, kw = self.parse_kwargs(expr)
                attr = attr[9:]
                for child in obj: # VGroup is iterable
                    method = getattr(child, attr)
                    method(*args, **kw)
            elif attr.startswith('attreach.'):
                path = attr[9:].split('.')
                expr = node.attrib.get(attr, True)
                args, kw = self.parse_kwargs(expr)
                for child in obj:
                    context = reduce(getattr, path[:-1], child)
                    setattr(context, path[-1], args[0])
        
    def __getitem__(self, key: str) -> Mobject or tuple:
        if isinstance(key, str):
            return self.ids[key]
        elif isinstance(key, tuple):
            return (self.ids[id] for id in key)
        else:
            raise TypeError('key must be str or tuple')
