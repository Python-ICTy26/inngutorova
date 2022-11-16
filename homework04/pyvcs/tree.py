import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(
    gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = ""
) -> str:
    tree = b""
    for i in index:
        path = i.name.split("/")
        if "/" in i.name:
            tree += b"40000 "
            sha = hash_object(
                oct(i.mode)[2:].encode()
                + b" "
                + "/".join(path[1:]).encode()
                + b"\0"
                + i.sha1,
                "tree",
                True,
            )
            tree += path[0].encode() + b"\0" + bytes.fromhex(sha)
        else:
            tree += oct(i.mode)[2:].encode() + b" " + path[0].encode() + b"\0" + i.sha1
    return hash_object(tree, "tree", True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    if author == None:
        author = f"{os.environ['GIT_AUTHOR_NAME']} <{os.environ['GIT_AUTHOR_EMAIL']}>"
    timestamp = int(time.mktime(time.localtime()))
    utc_offset = -time.timezone
    author_time = "{} {}{:02}{:02}".format(
        timestamp,
        "+" if utc_offset > 0 else "-",
        abs(utc_offset) // 3600,
        (abs(utc_offset) // 60) % 60,
    )
    content = f"tree {tree}\n"
    if parent:
        content += f"parent {parent}\n"
    content += f"author {author} {author_time}\ncommitter {author} {author_time}\n\n{message}\n"
    sha = hash_object(content.encode("ascii"), "commit", True)
    return sha
