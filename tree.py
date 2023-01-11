import argparse
import pathlib


def get_rows(path: pathlib.Path, node_str="├───", pass_str="│   "):
    # 生成用于打印的字符串
    # 如果是目录,就递归
    if path.is_dir():
        path_iter = get_tree_nodes(path)
        # 为了识别出无权限的情况，无权限时有额外的提示
        yield node_str + next(path_iter)
        for sub_file in path_iter:
            yield pass_str + sub_file
    else:
        yield node_str + path.name


def get_tree_nodes(path: pathlib.Path):
    path_iter = path.iterdir()
    # 可以检测访问权限、空目录
    try:
        # 这里是为了得到迭代的最后一个（最后一个的显示和其他的不同），延迟生成
        last_file = next(path_iter)
        yield path.name
    except PermissionError:
        yield path.name + "* Permission denied *"
    except StopIteration:
        yield path.name
    else:
        # 当前目录有权限且非空，才会生成
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
