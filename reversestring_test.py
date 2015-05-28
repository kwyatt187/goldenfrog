import unittest
from reversestring import reversestring

class TestReverseStringMethod(unittest.TestCase):
    def test_reversestring(self):
        string = 'This is only a test'
        self.assertEqual(reversestring(string), 'tsEt A ylnO sI sIht')
        string = 'Happy birthday to you'
        self.assertEqual(reversestring(string), 'UOy Ot yAdhtrIb yppAh')
        

if __name__ == '__main__':
    unittest.main()
