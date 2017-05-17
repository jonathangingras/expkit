from unittest import TestCase
from expkit.utils.expando import Expando


obj = Expando(_89='opm', kiki=9)
obj2 = Expando.from_dict({89:'opm2', 'kiki':90})

class ExpandoTest(TestCase):
    def test_can_instanciate_from_kwargs(self):
        self.assertEqual({"_89": "opm", "kiki": 9}, vars(obj))

    def test_accesssing_non_existing_object_returns_None(self):
        self.assertEqual(None, obj[0])

    def test_setting_non_existing_object_sets_effectively(self):
        obj[1] = 1

        self.assertEqual(1, obj[1])
