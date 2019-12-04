
class DOT:
    def __init__(self, graph):
        self.graph = graph

    def encode(self):
        dot = ['digraph {']

        for from_node in self.graph:
            for to_node in from_node:
                edge = from_node.name, to_node.name, from_node[to_node]
                if edge[2] is not None:
                    template = '{} -> {} [label={}]'
                else:
                    template = '{} -> {}'
                dot.append(template.format(*edge))

        return ('\n\t'.join(dot) + '\n}').expandtabs(2)
