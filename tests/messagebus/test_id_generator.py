import time
import unittest

from rustic_ai.messagebus.utils import GemstoneGenerator, Priority


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.generator = GemstoneGenerator(1)
        self.generator2 = GemstoneGenerator(2)

    def test_id_generator(self):
        # Test that IDs are unique
        id1 = self.generator.get_id(Priority.NORMAL)
        id2 = self.generator.get_id(Priority.NORMAL)
        self.assertNotEqual(id1, id2)

    def test_id_generator_sorting(self):
        # Test that IDs are sorted by priority then time
        id1 = self.generator.get_id(Priority.NORMAL)
        id2 = self.generator.get_id(Priority.HIGH)
        id3 = self.generator.get_id(Priority.LOW)
        time.sleep(0.001)
        id4 = self.generator.get_id(Priority.URGENT)
        id5 = self.generator.get_id(Priority.NORMAL)
        sorted_ids = sorted([id1, id2, id3, id4, id5])
        self.assertEqual(sorted_ids, [id4, id2, id1, id5, id3])

    def test_id_generator_across_generators(self):
        # Test that IDs are unique across generators
        id1 = self.generator.get_id(Priority.NORMAL)
        id2 = self.generator2.get_id(Priority.NORMAL)
        self.assertNotEqual(id1, id2)

    def test_id_generator_sorting_across_generators(self):
        # Test that IDs are sorted by priority then time across generators
        id1 = self.generator.get_id(Priority.NORMAL)
        id2 = self.generator2.get_id(Priority.IMPORTANT)
        time.sleep(0.001)
        id3 = self.generator.get_id(Priority.IMPORTANT)
        id4 = self.generator.get_id(Priority.NORMAL)
        id5 = self.generator2.get_id(Priority.URGENT)
        sorted_ids = sorted([id1, id2, id3, id4, id5])
        self.assertEqual(sorted_ids, [id5, id2, id3, id1, id4])

    def test_id_generator_by_priority_and_time(self):
        # Test that IDs are sorted by priority then time
        id1 = self.generator.get_id(Priority.NORMAL)
        id2 = self.generator.get_id(Priority.HIGH)
        id3 = self.generator.get_id(Priority.LOW)
        id4 = self.generator.get_id(Priority.NORMAL)
        id5 = self.generator.get_id(Priority.URGENT)
        id6 = self.generator.get_id(Priority.LOW)
        sorted_ids = sorted([id1, id2, id3, id4, id5, id6])
        self.assertEqual(sorted_ids, [id5, id2, id1, id4, id3, id6])

    def test_id_conversion_to_int_and_back(self):
        # Test that IDs can be converted to ints and back
        id1 = self.generator.get_id(Priority.URGENT)
        id2 = id1.to_int()
        id3 = id1.from_int(id2)
        self.assertEqual(id1, id3)


if __name__ == "__main__":
    unittest.main()
