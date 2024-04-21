class uniquestr(str):

    _lower = None

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return self is other

    def lower(self):
        if self._lower is None:
            lower = str.lower(self)
            if str.__eq__(lower, self): 
                self._lower = self
            else:
                self._lower = uniquestr(lower)
        return self._lower
