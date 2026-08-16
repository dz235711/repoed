import tree_sitter as ts

from core.model import SourceSpan, Coordinate


def src_span_from_node(node: ts.Node) -> SourceSpan:
    return SourceSpan(
        start=Coordinate(
            line=node.start_point[0],
            column=node.start_point[1],
            byte_offset=node.start_byte,
        ),
        end=Coordinate(
            line=node.end_point[0],
            column=node.end_point[1],
            byte_offset=node.end_byte,
        ),
    )
