from pathlib import Path


ASSETS_ROOT = Path(__file__).resolve().parents[1] / "app" / "assets"
TEMPORARY_NAMES = {
    ".DS_Store",
    "Thumbs.db",
}
TEMPORARY_SUFFIXES = {
    ".bak",
    ".orig",
    ".tmp",
}


def test_assets_package_exists() -> None:
    assert ASSETS_ROOT.is_dir()
    assert (ASSETS_ROOT / "__init__.py").is_file()


def test_assets_tree_has_no_temporary_files() -> None:
    temporary_files = [
        path.relative_to(ASSETS_ROOT)
        for path in ASSETS_ROOT.rglob("*")
        if path.is_file()
        and (
            path.name in TEMPORARY_NAMES
            or path.suffix.lower() in TEMPORARY_SUFFIXES
            or path.name.endswith("~")
        )
    ]

    assert temporary_files == []
