from willump.graph.willump_graph_node import WillumpGraphNode

from typing import List
import ast


class WillumpPythonNode(WillumpGraphNode):
    """
    Willump Python node.  Represents arbitrary Python.  Can have any number of inputs.

    TODO:  Can also have any number of outputs.
    """
    is_async_node: bool

    def __init__(self, python_ast: ast.AST, input_names: List[str], output_name: str, in_nodes: List[WillumpGraphNode],
                 is_async_node: bool = False) -> None:
        self._arg_name = output_name
        self._in_nodes = in_nodes
        self._input_names = input_names
        self._python_ast = python_ast
        self.is_async_node = is_async_node

    def get_in_nodes(self) -> List[WillumpGraphNode]:
        return self._in_nodes

    def get_in_names(self) -> List[str]:
        return self._input_names

    def get_node_weld(self) -> str:
        return ""

    def get_output_name(self) -> str:
        return self._arg_name

    def get_python(self) -> ast.AST:
        return self._python_ast

    def __repr__(self):
        return "Willump Python node with inputs %s\n outputs %s\n and code %s\n" % \
               (str(list(map(lambda x: x.get_output_name(), self._in_nodes))), self._arg_name, ast.dump(self._python_ast))
