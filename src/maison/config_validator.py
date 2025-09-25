from maison import service
from maison import types


class Validator:
    def validate(
        self, values: types.ConfigValues, schema: type[service.IsSchema]
    ) -> types.ConfigValues:
        validated_schema = schema(**values)
        return validated_schema.model_dump()
