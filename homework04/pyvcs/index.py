import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        values = (
            self.ctime_s,
            self.ctime_n,
            self.mtime_s,
            self.mtime_n,
            self.dev,
            self.ino,
            self.mode,
            self.uid,
            self.gid,
            self.size,
            self.sha1,
            self.flags,
            self.name.encode(),
        )
        return struct.pack(f">10i20sh{len(self.name)}s3x", *values)

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        unpacked = list(struct.unpack(f">10i20sh{len(data) - 62}s", data))
        unpacked[-1] = unpacked[-1][:-3].decode()
        return GitIndexEntry(*unpacked)


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    res: tp.List[GitIndexEntry] = []
    if not (gitdir / "index").exists():
        return []
    with open(gitdir / "index", "rb") as f:
        data = f.read()
    k = struct.unpack(">LL", data[4:12])[1]
    ins = data[12:-20]
    count = 0
    for i in range(k):
        start = count + 62
        end = ins[start:].find(b"\x00\x00\x00") + start + 3
        res.append(GitIndexEntry.unpack(ins[count:end]))
        count = end
    return res


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    data = struct.pack("!4s2i", *[b"DIRC", 2, len(entries)])
    for entry in entries:
        data += entry.pack()
    with open(gitdir / "index", "wb") as f:
        f.write(data)
        f.write(hashlib.sha1(data).digest())


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    for entry in read_index(gitdir):
        if details:
            print(f"{str(oct(entry.mode))[2:]} {entry.sha1.hex()} 0\t{entry.name}")
        else:
            print(entry.name)


def update_index(
    gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True
) -> None:
    if (gitdir / "index").exists():
        files = read_index(gitdir)
    else:
        files = []
    for path in paths:
        with open(path) as f:
            ins = f.read()
        hash = hash_object(ins.encode(), "blob", True)
        stat = os.stat(path)
        files.append(
            GitIndexEntry(
                ctime_s=int(stat.st_ctime),
                ctime_n=0,
                mtime_s=int(stat.st_mtime),
                mtime_n=0,
                dev=stat.st_dev,
                ino=stat.st_ino,
                mode=stat.st_mode,
                uid=stat.st_uid,
                gid=stat.st_gid,
                size=stat.st_size,
                sha1=bytes.fromhex(hash),
                flags=7,
                name=str(path).replace("\\", "/"),
            )
        )
    files.sort(key=operator.attrgetter("name"))
    write_index(gitdir, files)
