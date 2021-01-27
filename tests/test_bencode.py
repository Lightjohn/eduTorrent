
import unittest
from collections import OrderedDict

from bencode import Decoder, Encoder


class DecodingTests(unittest.TestCase):

    def test_integer(self):
        res = Decoder().decode(b'i123e')

        self.assertEqual(int(res), 123)

    def test_string(self):
        res = Decoder().decode(b'4:name')

        self.assertEqual(res, b'name')

    def test_min_string(self):
        res = Decoder().decode(b'1:a')

        self.assertEqual(res, b'a')

    def test_string_with_space(self):
        res = Decoder().decode(b'12:Middle Earth')

        self.assertEqual(res, b'Middle Earth')

    def test_list(self):
        res = Decoder().decode(b'l4:spam4:eggsi123ee')

        self.assertEqual(len(res), 3)
        self.assertEqual(res[0], b'spam')
        self.assertEqual(res[1], b'eggs')
        self.assertEqual(res[2], 123)

    def test_dict(self):
        res = Decoder().decode(b'd3:cow3:moo4:spam4:eggse')

        self.assertTrue(isinstance(res, dict))
        self.assertEqual(res[b'cow'], b'moo')
        self.assertEqual(res[b'spam'], b'eggs')


class EncodingTests(unittest.TestCase):
    def test_integer(self):
        res = Encoder().encode(123)

        self.assertEqual(b'i123e', res)

    def test_string(self):
        res = Encoder().encode('Middle Earth')

        self.assertEqual(b'12:Middle Earth', res)

    def test_list(self):
        res = Encoder().encode(['spam', 'eggs', 123])

        self.assertEqual(b'l4:spam4:eggsi123ee', res)

    def test_dict(self):

        d = OrderedDict()
        d['cow'] = 'moo'
        d['spam'] = 'eggs'
        res = Encoder().encode(d)

        self.assertEqual(b'd3:cow3:moo4:spam4:eggse', res)

    def test_nested_structure(self):
        outer = OrderedDict()
        b = OrderedDict()
        b['ba'] = 'foo'
        b['bb'] = 'bar'
        outer['a'] = 123
        outer['b'] = b
        outer['c'] = [['a', 'b'], 'z']
        res = Encoder().encode(outer)

        self.assertEqual(res,
                         b'd1:ai123e1:bd2:ba3:foo2:bb3:bare1:cll1:a1:be1:zee')
