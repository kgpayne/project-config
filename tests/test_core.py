import pytest

import project_config as pc

from .conftest import ProjectFile


def test_dict_storage(example_project, example_project_dict):
    assert example_project._dict == example_project_dict


def test_properties_created(example_project):

    assert set(["_dict", "_model", "plugins"]).issubset(
        example_project.__class__.__dict__.keys()
    )

    assert set(["_dict", "_model", "extractors"]).issubset(
        example_project.plugins.__class__.__dict__.keys()
    )

    assert set(["_dict", "_model", "name", "inherit_from", "pip_url"]).issubset(
        example_project.plugins.extractors[0].__class__.__dict__.keys()
    )


def test_edit_dict(example_project, example_project_dict):
    example_project.plugins.extractors[0].name = "updated-test-extractor"
    assert (
        example_project_dict["plugins"]["extractors"][0]["name"]
        == "updated-test-extractor"
    )


def test_required_field(example_project_dict):
    """This should raise on instantiation ideally.
    TODO: add validation on creation
    """
    example_project_dict["plugins"]["extractors"][0].pop("name")
    with pytest.raises(pc.RequiredFieldError):
        pf = ProjectFile.from_dict(example_project_dict)
        # raises on access, because of lazy-loading
        pf.plugins.extractors[0].name
