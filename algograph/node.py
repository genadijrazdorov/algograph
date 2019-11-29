from collections import abc


class Node(abc.MutableMapping):
    def __init__(self, name, children=None):
        self.name = name
        if children is None:
            children = {}
        self.children = children

    def __repr__(self):
        return "<{s.__class__.__name__} '{s.name}'>".format(s=self)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __delitem__(self, child):
        del self.children[child]

    def __getitem__(self, child):
        return self.children[child]

    def __iter__(self):
        return iter(self.children)

    def __len__(self):
        return len(self.children)

    def __setitem__(self, child, label):
        self.children[child] = label
