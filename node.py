from numpy import float_

class Node:
    lat = None
    lang = None
    state = None

    def __str__(self):
        return str(self.state)

    def __init__(self, lat, lang, state):
        self.lat = lat
        self.lang = lang
        self.state = state

        try:
            assert isinstance(self.lat, float_)
            assert isinstance(self.lang, float_)
            assert isinstance(self.lat, bool)
        except AssertionError as ae:
            print(ae)

    def get_state(self):
        return self.state

    def get_points(self):
        return [self.lat, self.lang]