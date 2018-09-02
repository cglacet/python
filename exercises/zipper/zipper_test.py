import unittest


from zipper import Zipper


# Tests adapted from `problem-specifications//canonical-data.json` @ v1.1.0
class ZipperTest(unittest.TestCase):
    def test_empty(self):
        zipper = Zipper()
        with self.assertRaises(ValueError):
            zipper.value

    def test_insert_non_mutating(self):
        zipper = Zipper()
        zipper.insert(1)
        with self.assertRaises(ValueError):
            zipper.value

    def test_insert_and_get_value(self):
        expected = 1
        actual = Zipper().insert(expected).value
        self.assertEqual(actual, expected)

    def test_left(self):
        expected = 2
        zipper = Zipper().insert(1).left
        with self.assertRaises(ValueError):
            zipper.value
        actual = zipper.insert(expected).value
        self.assertEqual(actual, expected)

    def test_right(self):
        expected = 3
        zipper = Zipper().insert(1).right
        with self.assertRaises(ValueError):
            zipper.value
        zipper = zipper.insert(expected)
        self.assertEqual(zipper.value, expected)

    def test_left_and_right_inserts_non_mutating(self):
        expected = 1
        zipper = Zipper().insert(1)
        zipper.left.insert(2)
        zipper.right.insert(3)
        self.assertEqual(zipper.value, expected)

    def test_left_up_cancels(self):
        expected = 1
        zipper = Zipper().insert(expected)
        actual = zipper.left.up.value
        self.assertEqual(actual, expected)

    def test_right_up_cancels(self):
        expected = 2
        zipper = Zipper().insert(expected)
        actual = zipper.right.up.value
        self.assertEqual(actual, expected)

    def test_up_non_mutating(self):
        expected = 3
        zipper = Zipper().insert(1).left.insert(expected)
        zipper.up
        actual = zipper.value
        self.assertEqual(actual, expected)

    def test_set_value(self):
        expected = 2
        zipper = Zipper().insert(1).right.insert(3).up.left.insert(2)
        actual = zipper.set_value(zipper.value*expected).value//zipper.value
        self.assertEqual(actual, expected)

    def test_set_value_non_mutating(self):
        expected = 4
        zipper = Zipper().insert(expected)
        zipper.set_value(8)
        actual = zipper.value
        self.assertEqual(actual, expected)

    def test_root(self):
        expected = 1
        zipper = Zipper().insert(expected).right.insert(3).left.insert(5)
        actual = zipper.root.value
        self.assertEqual(actual, expected)

    def test_root_non_mutating(self):
        expected = 5
        zipper = Zipper().insert(expected).right.insert(3).left.insert(expected)
        zipper.root
        actual = zipper.value
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
