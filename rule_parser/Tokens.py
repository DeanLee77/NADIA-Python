class Tokens:
    tokens_list = []
    tokens_string_list = []
    tokens_string = ''

    def __init__(self, tl, tsl, ts):
        if tl is None:
            self.tokens_list = []
        if tsl is None:
            self.tokens_string_list = []
        if ts is None:
            self.tokens_string = ''
        if (ts is not None) and (tsl is not None) and (ts is not None):
            self.tokens_list = tl
            self.tokens_string_list = tsl
            self.tokens_string = ts
