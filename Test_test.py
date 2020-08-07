import unittest
import Family_Tree_Framework
from Sample_Family_Interface import get_data

class DSQTester(unittest.TestCase):
    def setUp(self):
        self.__family = Family_Tree_Framework.setup_family('Sample_Family_Record.csv',2019,6)


#EMPTY TREE TESTING

        #setup tests
    def test_person_data(self):
        self.assertEqual(get_data(self.__family,self.__family.find_member('anakin')), 'Anakin Skywalker:\n\tClass: 2020\n\tFandom Affiliation: Star Wars\n\nBig(s): Shmi Skywalker\nLittle(s): Luke Skywalker and Leia Skywalker\nCo-Big(s): Padme Amidala\nFamily: Skywalker Clan\nGenerations Descended: 2')

    def test_person_lineage(self):
        self.assertEqual(self.__family.get_lineage(self.__family.find_member('anakin')),'\t> Shmi Skywalker begat Anakin Skywalker.\n\t    Anakin Skywalker and Padme Amidala begat Leia Skywalker and Luke Skywalker.\n\t      Han Solo and Leia Skywalker begat Ben Solo.')
