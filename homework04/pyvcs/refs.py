import pathlib
import typing as tp


def update_ref(
    gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str
) -> None:
    with open(gitdir / ref, "w") as f:
        f.write(new_value)


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    with open(gitdir / name, "w") as f:
        f.write("ref: " + ref)


def ref_resolve(gitdir: pathlib.Path, refname: str) -> str:
    if refname == "HEAD":
        refname = get_ref(gitdir)
    with open(gitdir / refname) as f:
        return f.read().strip()


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    try:
        return ref_resolve(gitdir, "HEAD")
    except FileNotFoundError:
        return None


def is_detached(gitdir: pathlib.Path) -> bool:
    with open(gitdir / "HEAD") as f:
        return "ref" not in f.read()


def get_ref(gitdir: pathlib.Path) -> str:
    with open(gitdir / "HEAD") as f:
        ref = f.read()
        if "ref:" in ref:
            return ref.split()[1]
        else:
            return ref.strip()
