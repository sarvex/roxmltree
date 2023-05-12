#!/usr/bin/env python3

import sys
from lxml import etree


def escape_text(text):
    return text.encode('unicode_escape').decode("utf-8")


def split_qname(name):
    return name[1:].split('}') if name[0] == '{' else [None, name]


def print_ind(depth, *args, **kwargs):
    indent = '  ' * depth
    indent = indent[:-1]
    print(indent, *args, **kwargs)


def print_node(node, depth):
    if node.tag is etree.Comment:
        print_ind(depth, f'- Comment: "{escape_text(node.text)}"')

        if node.tail:
            print_ind(depth, f'- Text: "{escape_text(node.tail)}"')

        return

    if node.tag is etree.PI:
        print_ind(depth, '- PI:')
        print_ind(depth + 2, f'target: "{node.target}"')
        print_ind(depth + 2, f'value: "{escape_text(node.text)}"')

        if node.tail:
            print_ind(depth, f'- Text: "{escape_text(node.tail)}"')

        return

    print_ind(depth, '- Element:')
    if node.tag[0] == '{':
        uri, tag = split_qname(node.tag)
        print_ind(depth + 2, f'tag_name: {tag}@{uri}')
    else:
        print_ind(depth + 2, 'tag_name:', node.tag)

    if node.attrib:
        print_ind(depth + 2, 'attributes:')
        attrs = []
        for name, value in node.attrib.items():
            uri, tag = split_qname(name)
            if uri:
                attrs.append([f'{tag}@{uri}', value])
            else:
                attrs.append([tag, value])

        attrs = sorted(attrs, key=lambda x: x[0])

        for name, value in attrs:
            print_ind(depth + 3, f'{name}: "{escape_text(value)}"')

    if node.nsmap:
        print_ind(depth + 2, 'namespaces:')

        ns_list = []
        for name, value in node.nsmap.items():
            if not name and not value:
                ns_list.append(['None', '""'])
            elif not name:
                ns_list.append(['None', value])
            elif not value:
                ns_list.append([name, '""'])
            else:
                ns_list.append([name, value])

        ns_list = sorted(ns_list, key=lambda x: x[0])

        for name, value in ns_list:
            print_ind(depth + 3, f'{name}: {value}')

    if len(node):
        print_ind(depth + 2, 'children:')

        if node.text:
            print_ind(depth + 3, f'- Text: "{escape_text(node.text)}"')

        for child in node:
            print_node(child, depth + 3)
    elif node.text:
        print_ind(depth + 2, 'children:')
        print_ind(depth + 3, f'- Text: "{escape_text(node.text)}"')

    if node.tail:
        print_ind(depth, f'- Text: "{escape_text(node.tail)}"')


tree = etree.parse(sys.argv[1])
root = tree.getroot()

print('Document:')
print_node(root, 1)
