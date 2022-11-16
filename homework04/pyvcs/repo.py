import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    workdir = pathlib.Path(workdir)
    gitdir = os.environ.get("GIT_DIR") or ".git"
    path = workdir / gitdir
    for d in path.parents:
        if d.name == gitdir:
            path = d
    if path.exists():
        return path
    else:
        raise Exception("Not a git repository")


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    workdir = pathlib.Path(workdir)
    dir = os.environ.get("GIT_DIR") or ".git"
    path = workdir / dir
    if workdir.is_file():
        raise Exception(f"{workdir.name} is not a directory")
    path.mkdir()
    (path / "refs").mkdir()
    (path / "refs/heads").mkdir()
    (path / "refs/tags").mkdir()
    (path / "objects").mkdir()
    (path / "HEAD").write_text("ref: refs/heads/master\n")
    (path / "config").write_text(
        "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n"
    )
    (path / "description").write_text("Unnamed pyvcs repository.\n")
    return path
