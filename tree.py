import argparse
import pathlib
from collections import namedtuple
from typing import Generator


Symbols = namedtuple(
    "Symbols",
    (
        "node_str",
        "pass_str",
        "last_node_str",
        "last_pass_str",
    ),
)


all_symbols = (
    Symbols("├───", "│   ", "└───", "    "),
    Symbols("|---", "|   ", "\---", "    "),
)

symbols: Symbols


def get_rows(
    path: pathlib.Path, node_str: str, pass_str: str
) -> Generator[str, None, None]:
    # 生成用于打印的字符串
    yield node_str + path.name
    # 如果是目录,就递归
    if path.is_dir():
        for sub_file in get_tree_nodes(path):
            yield pass_str + sub_file


def get_tree_nodes(path: pathlib.Path) -> Generator[str, None, None]:
    path_iter = path.iterdir()
    try:
        # 这里是为了得到迭代的最后一个（最后一个的显示和其他的不同），延迟生成
        last_file = next(path_iter)
    # 当前目录无权限或为空忽略
    except (PermissionError, StopIteration):
        return
    for file in path_iter:
        yield from get_rows(last_file, symbols.node_str, symbols.pass_str)
        last_file = file
    yield from get_rows(last_file, symbols.last_node_str, symbols.last_pass_str)


def main():
    parser = argparse.ArgumentParser(
        description="Graphically displays the folder structure of a drive or path."
    )
    parser.add_argument(
        "path",
        metavar="PATH",
        type=str,
        nargs="?",
        help="A directory that serves as the root of the tree",
    )
    parser.add_argument(
        "-a",
        "--ascii",
        action="store_true",
        default=False,
        help="Use ASCII instead of extended characters",
    )
    parser.add_argument(
        "-f",
        "--file",
        metavar="FILE",
        type=str,
        help="Output to a file.",
    )
    args = parser.parse_args()
    path = args.path
    use_ascii = args.ascii
    file_str = args.file
    global symbols
    symbols = all_symbols[use_ascii]

    # 没有指定路径，就默认当前路径
    if path is None:
        path = pathlib.Path(".")
    else:
        path = pathlib.Path(path)
        if not path.is_dir():
            raise NotADirectoryError("the directory does NOT exist")
    # 开始输出
    if file_str is not None:
        with open(file_str, "x", newline="\n") as f:
            f.write(f"{path}\n")
            for text in get_tree_nodes(path):
                f.write(f"{text}\n")
    else:
        print(path)
        for text in get_tree_nodes(path):
            print(text)


if __name__ == '__main__':
    main()
