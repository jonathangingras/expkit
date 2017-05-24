from unittest import TestCase
from expkit.utils.expando import Expando


obj = Expando(_89='opm', kiki=9)
obj2 = Expando.from_dict({89:'opm2', 'kiki':90})

class ExpandoTest(TestCase):
    def test_can_instanciate_from_kwargs(self):
        self.assertEqual({"_89": "opm", "kiki": 9}, vars(obj))


    def test_getting_non_existing_attribute_returns_None(self):
        self.assertEqual(None, obj.non_existing)


    def test_setting_non_existing_object_sets_effectively(self):
        obj._1 = 1
        obj.someatt = "someval"

        self.assertEqual(1, obj._1)
        self.assertEqual("someval", obj.someatt)


    def test_accesssing_non_existing_object_returns_None_with_getitem(self):
        self.assertEqual(None, obj[0])


    def test_setting_non_existing_object_sets_effectively_with_setitem(self):
        obj[1] = 1
        obj["someatt"] = "someval"

        self.assertEqual(1, obj[1])
        self.assertEqual("someval", obj["someatt"])
