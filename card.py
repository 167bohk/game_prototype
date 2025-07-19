class Card:
    def __init__(self, name="", description="",is_premium=False, number=0):
        self.name = name
        self.description = description
        self.is_premium = is_premium
        self.number = number

    def __repr__(self):
        return f"{self.name}, {self.description}, is premium={self.is_premium}, {self.number}"
