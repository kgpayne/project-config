

def property_maker(name):
    storage_name = '_' + name.lower()

    @property
    def prop(self):
        return getattr(self, storage_name)

    @prop.setter
    def prop(self, value):
        setattr(self, storage_name, value)

    return prop


def make_class(classname, **options):
    class Class: pass
    Class.__name__ = classname
    Class._dict = options

    for key, value in options.items():
        storage_name = '_' + key.lower()
        setattr(Class, storage_name, value)
        setattr(Class, key.lower(), property_maker(key))

    return Class


class Base:

    def __init__(self, class_):
        self.class_ = class_


class Item(Base):
    pass


class Array(Base):
    pass


class Model:

    def __init__(self, values: dict):
        setattr(self, "_dict", values)
        for attribute, base in self.__class__.__dict__.items():
            if isinstance(base, Item):
                setattr(self, attribute, base.class_(values.get(attribute, None)))
            if isinstance(base, Array):
                setattr(
                    self, attribute, [
                        base.class_(value) for value in values.get(attribute, [])
                    ]
                )

class File(Model):
    pass
