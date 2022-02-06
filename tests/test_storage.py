import pytest

import project_config as pc

from .conftest import ProjectFile


def test_raise_storage_error(example_project, example_project_dict):

    with pytest.raises(pc.StorageNotFound):
        pf = ProjectFile.from_dict(example_project_dict)
        # raises on access, because of lazy-loading
        extractor = pf.plugins.extractors[0]
        extractor.name = "updated-test-extractor"
        extractor.commit()
