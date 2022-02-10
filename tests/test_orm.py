from pydantic import SecretStr


class TestORM:
    """Test ORM"""

    def test_parse_obj(self, example_config_model, example_config_values):
        plugin = example_config_model.parse_obj(example_config_values)
        assert plugin.commands["info"].args == "--test"
        assert plugin.settings[0].kind == "string"
        assert plugin.settings[1].value == SecretStr("s3cr3t")
        assert plugin.settings[2].value == 10
        assert plugin.settings[3].value.year == 2021
