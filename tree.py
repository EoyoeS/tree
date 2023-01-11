import argparse
import pathlib


def get_rows(path: pathlib.Path, node_str="├───", pass_str="│   "):
    # 生成用于打印的字符串
    yield node_str + path.name
    # 如果是目录,就递归
    if path.is_dir():
        for sub_file in get_tree_nodes(path):
            yield pass_str + sub_file


def get_tree_nodes(path: pathlib.Path):
    # 这里是为了得到迭代的最后一个（最后一个的显示和其他的不同），延迟生成（可能遇到空目录）
    path_iter = path.iterdir()
    last_file = next(path_iter, None)
    # 当前目录是否为空。如果不是空，才会生成
    if last_file is not None:
        for file in path_iter:
            yield from get_rows(last_file)
            last_file = file
        yield from get_rows(last_file, node_str="└───", pass_str="    ")


def main():
    parser = argparse.ArgumentParser(
        description="Graphically displays the folder structure of a drive or path."
    )
    parser.add_argument("path", metavar="PATH", type=str, nargs="?")
    args = parser.parse_args()
    path = args.path
    # 没有指定路径，就默认当前路径
    if path is None:
        path = pathlib.Path(".")
    else:
        path = pathlib.Path(path)
        if not path.is_dir():
            raise NotADirectoryError("the directory does NOT exist")
    # 开始输出
    print(path)
    for text in get_tree_nodes(path):
        print(text)


if __name__ == '__main__':
    main()
