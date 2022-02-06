

class RequiredFieldError(Exception):
    pass


class BaseField:
    """ Base Model field type class
    """

    def __init__(self, class_, required=False, default=None):
        self.class_ = class_
        self.required = required
        self.default = default


class Field(BaseField):
    """ Model field type, representing a scalar property.
    """
    pass


class Array(BaseField):
    """ Model field type, representing an array property.
    """
    pass


class BaseProperty:
    """ Base Property class.

    Used to create concrete data classes from Model representations.
    """
    pass


def property_maker(name):

    @property
    def prop(self):
        field_type = self._model.__dict__.get(name)
        value = self._dict.get(name)

        if isinstance(field_type, Field):
            if Model in field_type.class_.__bases__:
                return field_type.class_.from_dict(value)
            else:
                return value

        if isinstance(field_type, Array):
            if Model in field_type.class_.__bases__:
                return [
                    field_type.class_.from_dict(item)
                    for item in value
                ]
            else:
                return [item for item in value]

    @prop.setter
    def prop(self, value):
        self._dict[name] = value

    return prop


class Model:
    """ Object declaration class.

    Model subclasses are used to map a class representation
    to an underlying persistance representation (dict). it
    is also used to generate JSONSchema for represented objects.
    """
    @classmethod
    def from_dict(cls, values):

        class Class(BaseProperty): pass
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
