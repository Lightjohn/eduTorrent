import itertools


class Encoder:
    def encode(self, data: object, encode=True):
        if isinstance(data, int):
            str_data = f"i{data}e"
        elif isinstance(data, str):
            str_data = f"{len(data)}:{data}"
        elif isinstance(data, list):
            encoded_data = [self.encode(i, False) for i in data]
            str_data = f"l{''.join(encoded_data)}e"
        elif isinstance(data, dict):
            all_elem = list(itertools.chain(*data.items()))
            encoded_data = [self.encode(i, False) for i in all_elem]
            str_data = f"d{''.join(encoded_data)}e"
        elif isinstance(data, bytes):
            str_data = f"{len(data)}:{data.decode('latin-1')}"
        else:
            raise RuntimeError("Invalid data", data)
        return str_data.encode('latin-1') if encode else str_data


class Decoder:
    TOKEN_INTEGER = b'i'
    TOKEN_LIST = b'l'
    TOKEN_DICT = b'd'
    TOKEN_END = b'e'
    TOKEN_STRING_SEPARATOR = b':'

    def __init__(self):
        self._index = 0
        self._max = 0
        self._data = None

    def decode(self, data: bytes):
        self._index = 0
        self._max = len(data)
        self._data = data
        return self._decode()

    def _decode(self):
        struct = self._get()
        if self._index >= self._max:
            return None
        elif struct == self.TOKEN_LIST:
            self._inc()
            return self._parse_list()
        elif struct == self.TOKEN_DICT:
            self._inc()
            return self._parse_dict()
        elif struct == self.TOKEN_INTEGER:
            return self._parse_int()
        elif struct in b"0123456789":
            return self._parse_str()
        elif struct == self.TOKEN_END:
            self._inc()
            return None
        else:
            raise RuntimeError("Invalid data", self._index, self._data)

    def _index_end(self, token):
        return self._data.index(token, self._index)

    def _parse_dict(self):
        return_dict = {}
        key, val = self._get_key_val()
        while key is not None and val is not None:
            return_dict[key] = val
            key, val = self._get_key_val()
        return return_dict

    def _get_key_val(self):
        return self._decode(), self._decode()

    def _parse_list(self):
        return_list = []
        while (result := self._decode()) is not None:
            return_list.append(result)
        return return_list

    def _parse_str(self):
        index_size = self._index_end(self.TOKEN_STRING_SEPARATOR)
        str_size = int(self._data[self._index:index_size])
        b_string = self._data[index_size + 1: index_size + 1 + str_size]
        self._index = index_size + 1 + str_size
        return b_string

    def _parse_int(self):
        index_end = self._index_end(self.TOKEN_END)
        result = self._data[self._index + 1:index_end]
        self._index = index_end + 1
        return int(result)

    def _inc(self):
        self._index += 1

    def _get(self):
        return self._data[self._index:self._index + 1]

