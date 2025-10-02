from maison import config_validator
from maison import typedefs


class Schema:
    def __init__(self, *args: object, **kwargs: object) -> None:
        pass

    def model_dump(self) -> typedefs.ConfigValues:
        return {"key": "validated"}


class TestValidate:
    def test_returns_validated_values(self):
        validator = config_validator.Validator()

        validated_values = validator.validate(
            values={"key": "something"}, schema=Schema
        )

        assert validated_values == {"key": "validated"}
