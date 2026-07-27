import os

SOURCE_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".java",
    ".cpp",
    ".c",
    ".cs",
    ".go",
    ".rs",
}


def get_source_files(repo_path: str, changed_files: list | None):

    paths = []

    # Local repository review (full scan)
    if not changed_files:
        return [repo_path]

    paths = []

    for file in changed_files:

        full_path = os.path.join(
            repo_path,
            file["filename"],
        )

        extension = os.path.splitext(full_path)[1].lower()

        if extension in SOURCE_EXTENSIONS:
            paths.append(full_path)

    return paths