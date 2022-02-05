
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
