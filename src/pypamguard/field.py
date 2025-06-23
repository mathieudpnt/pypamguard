from field_types import Type

class Field:
    def __init__(self, name: str, field_type: Type ):
        self.name = name
        self.field_type = field_type

    def process(self, data):
        return self.field_type.process(data)

    def __str__(self):
        return f"{self.name}: {self.field_type}"