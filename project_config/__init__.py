from typing import Any


class RequiredFieldError(Exception):
    pass


class Base:
    pass


class BaseField:

    def __init__(self, class_, required=False, default=None):
        self.class_ = class_
        self.required = required
        self.default = default


class Item(BaseField):
    pass


class Array(BaseField):
    pass


def property_maker(name):

    @property
    def prop(self):
        field = self._model.__dict__.get(name)
        value = self._dict.get(name)

        if isinstance(field, Item):
            if Model in field.class_.__bases__:
                return field.class_.from_dict(value)
            else:
                return value

        if isinstance(field, Array):
            if Model in field.class_.__bases__:
                return [
                    field.class_.from_dict(item) for item in value
                ]
            else:
                return [item for item in value]

    @prop.setter
    def prop(self, value):
        self._dict[name] = value

    return prop


class Model:

    @classmethod
    def from_dict(cls, values):

        class Class(Base): pass
        Class.__name__ = cls.__name__
        setattr(Class, "_dict", values)
        setattr(Class, "_model", cls)

        for prop, field in cls.__dict__.items():
            if not prop.startswith('__'):

                if prop not in values:
                    if field.required:
                        raise RequiredFieldError(f"Required field '{prop}' not found.")
                else:
                    setattr(Class, prop, property_maker(prop))

        return Class()
