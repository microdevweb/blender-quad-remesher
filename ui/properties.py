# Custom Properties for Quad Remesher Addon

class CustomProperties:
    def __init__(self):
        self.property1 = None  # Description of property1
        self.property2 = None  # Description of property2
        self.property3 = None  # Description of property3

    def set_property1(self, value):
        self.property1 = value

    def set_property2(self, value):
        self.property2 = value

    def set_property3(self, value):
        self.property3 = value

    def get_properties(self):
        return {"property1": self.property1, "property2": self.property2, "property3": self.property3}
