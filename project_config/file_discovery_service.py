import copy
import glob
import hashlib
from pathlib import Path
from typing import Bool, List, Union

from pydantic import BaseModel, Protocol


class File:
    """Config storage container."""

    def __init__(self, path: Path):
        """Instantiate a File instance.

        Args:
            path: The absolute path to this file.
        """
        self.path = path

    def hash(self):
        """Return the MD5 hash of this file."""
        hash_md5 = hashlib.md5()
        with open(self.path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()


class PatternMap:
    """Glob pattern mapped to a Pydantic Model."""

    def __init__(
        self,
        pattern: str,
        model: BaseModel,
        content_type: Union[str, None] = None,
        recursive: Bool = False,
    ):
        """Instantiate a PatternMap instance.

        Args:
            pattern: A valid glob pattern string.
            model: A pydantic model to use
            content_type: Pydantic content type.
            recursive: Search for files by pattern recursively.
        """
        self.pattern = pattern
        self.model = model
        self.content_type = content_type
        self.recursive = recursive


class Document:
    def __init__(
        self,
        model: BaseModel,
        file: File,
        content_type: Union[str, None] = None,
        encoding: str = "utf-8",
        proto: Protocol = None,
        allow_pickle: bool = False,
    ):
        """Instantiate a Document.

        Args:
            model: The Pydantic model for ser/de.
            file: The file with Document contents.
            content_type: Pydantic content type.
            encoding: Pydantic encoding.
            proto: Pydantic protocol.
            allow_pickle: Pydantic allow pickle flag.
        """
        self.file = file
        self.model = model

        self.content_type = content_type
        self.encoding = encoding
        self.proto = proto
        self.allow_pickle = allow_pickle

        self._file_hash = copy(self.file.hash)
        self._contents = None

    def has_file_changed(self):
        return self.file.hash == self._file_hash

    def contents(self):
        if self.has_file_changed() or self._contents is None:
            self._file_hash = copy(self.file.hash)
            self._contents = self.model.parse_file(
                path=self.file.path,
                content_type=self.content_type,
                encoding=self.encoding,
                proto=self.proto,
                allow_pickle=self.allow_pickle,
            )
        return self._contents


class DocumentDiscoveryService:
    def __init__(self, root_dir: Path, pattern_maps: List[PatternMap]):
        """"""
        self.root_dir = root_dir
        self.pattern_maps = pattern_maps

        self._path_patterns = {}

    def _discover_files(self, pattern, recursive=False):
        return glob.glob(pattern, recursive=recursive)

    def get_documents(self):
        """Get documents from a list of pattern maps."""
        pattern_paths = {
            pattern_map: self.discover_files(
                pattern=pattern_map.pattern, recursive=pattern_map.recursive
            )
            for pattern_map in self.pattern_maps
        }

        path_pattern_maps = {}
        for pattern_map, paths in pattern_paths.items():
            for path in paths:
                if path not in path_pattern_maps.keys():
                    path_pattern_maps[path] = []
                path_pattern_maps[path].append(pattern_map)
        self._path_patterns = path_pattern_maps

        documents = []
        for path, pattern_maps in self._path_patterns.items():
            # TODO: handle duplicate matches better than this
            pattern_map = pattern_maps[0]
            document = Document(
                file=File(path=path),
                model=pattern_map.model,
                content_type=pattern_map.content_type,
            )
            documents.append(document)
        return documents
