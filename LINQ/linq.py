class Range:
    def __init__(self, arg):
        self._obj = arg

    def select(self, func):
        self._obj = [func(item) for item in self._obj]
        return self

    def where(self, func):
        result = []
        for item in self._obj:
            if func(item):
                result.append(item)
        self._obj = result
        return self

    def flatten(self):
        result = []
        for sequence in self._obj:
            for item in sequence:
                result.append(item)
        self._obj = result
        return self

    def take(self, num):
        self._obj = self._obj[0:num]
        return self

    def group_by(self, key):
        result = {}
        for item in self._obj:
            k = key(item)
            if k in result:
                result[k].append(item)
            else:
                result[k] = [item]

        self._obj = []
        for key, value in result.items():
            self._obj.append((key, value))
        return self

    def order_by(self, key):
        self._obj = sorted(self._obj, key=key)
        return self

    def to_list(self):
        return self._obj

