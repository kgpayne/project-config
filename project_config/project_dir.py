from pathlib import Path
from typing import List, Union

from .orm import ConfigModel


class ProjectFile:
    def __init__(
        self,
        model: ConfigModel,
        path: Path,
        type_name: str = None,
        loader: str = None,
        required: bool = None,
    ):
        self.model = model
        self.path = path
        self.type_name = type_name or "default"
        self.required = required or False

    def validate(self, root: Path):
        if self.required and not (root / self.path).exists():
            raise FileNotFoundError(f"Required file {self.path} does not exist.")
        return bool((root / self.path).exists())


class ProjectFilePattern:
    def __init__(
        self,
        model: ConfigModel,
        type_name: str = None,
        loader: str = None,
        include_glob_patterns: List[str] = None,
        exclude_glob_patterns: List[str] = None,
    ):
        self.model = model
        self.type_name = type_name or "default"
        self.loader = loader or "yaml"
        self.include_glob_patterns = include_glob_patterns or []
        self.exclude_glob_patterns = exclude_glob_patterns or []

    def find_files(self, root: Path) -> List[ProjectFile]:
        """Find files matching include and exclude patters,
        relative to provided root.

        Args:
            root: Path to search patterns relative to.

        Returns:
            A list of ProjectFile instances
        """
        return []


class ProjectDir:
    def __init__(
        self, root: Path, files: List[Union[ProjectFile, ProjectFilePattern]] = None
    ):
        self.root = root
        self.files = files or []

    @property
    def discovered_files(self):
        found_files = []
        for file in self.files:
            if isinstance(file, ProjectFile):
                found_files.append(file)
            elif isinstance(file, ProjectFilePattern):
                found_files.extend(file.find_files(root=self.root))
        return [
            found_file
            for found_file in found_files
            if found_file.validate(root=self.root)
        ]
