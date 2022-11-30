import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    store = (f"{fmt} {len(data)}\0").encode() + data
    filename = hashlib.sha1(store).hexdigest()
    if write:
        gitdir = repo_find()
        os.makedirs(gitdir / "objects" / filename[:2], exist_ok=True)
        with open(gitdir / "objects" / filename[:2] / filename[2:], "wb") as f:
            f.write(zlib.compress(store))
    return filename


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    if not 4 <= len(obj_name) <= 40:
        raise Exception(f"Not a valid object name {obj_name}")
    objects = []
    dir_path = gitdir / "objects" / obj_name[:2]
    for obj_path in dir_path.iterdir():
        if obj_name[2:] in obj_path.name:
            objects.append(obj_name[:2] + obj_path.name)
    if not len(objects):
        raise Exception(f"Not a valid object name {obj_name}")
    return objects


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    if (gitdir / "objects" / obj_name[:2] / obj_name[2:]).exists():
        return obj_name
    else:
        return ""


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    path = gitdir / "objects" / sha[:2] / sha[2:]
    with open(path, "rb") as f:
        full = zlib.decompress(f.read())
    head = full[: full.find(b"\x00")]
    l = head[: head.find(b" ")]
    data = full[(full.find(b"\x00") + 1) :]
    return l.decode(), data


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    res = []
    while len(data) > 0:
        mode = int(data[: data.find(b" ")].decode())
        data = data[data.find(b" ") + 1 :]
        name = data[: data.find(b"\x00")].decode()
        data = data[data.find(b"\x00") + 1 :]
        sha = bytes.hex(data[:20])
        data = data[20:]
        res.append((mode, name, sha))
    return res


def cat_file(obj_name: str, pretty: bool = True) -> None:
    obj = read_object(obj_name, repo_find())
    if pretty:
        if obj[0] == "tree":
            res = ""
            for f in read_tree(obj[1]):
                res += (
                    str(f[0]).zfill(6)
                    + " "
                    + read_object(f[2], repo_find())[0]
                    + " "
                    + f[2]
                    + "\t"
                    + f[1]
                    + "\n"
                )
            print(res)
        else:
            print(obj[1].decode())


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    res = []
    for mode, name, sha in read_tree(read_object(tree_sha, gitdir)[1]):
        if read_object(sha, gitdir)[0] == "tree":
            tree = find_tree_files(sha, gitdir)
            for i in tree:
                res.append((name + "/" + i[0], i[1]))
        else:
            res.append((name, sha))
    return res


def commit_parse(raw: bytes, start: int = 0, dct=None):
    data = zlib.decompress(raw)
    return data[data.find(b"tree") + 5 : data.find(b"tree") + 45]
