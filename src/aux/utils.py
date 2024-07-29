    
class DotDict(dict):
    """dot.notation access to dictionary attributes"""
    def __getattr__(self, item):
        value = self.get(item)
        if isinstance(value, dict) and not isinstance(value, DotDict):
            value = DotDict(value)
            self[item] = value
        return value

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, item):
        del self[item]
