class TestProjectDir:
    def test_project_dir(self, example_project_directory):
        assert len(example_project_directory.discovered_files) == 1
