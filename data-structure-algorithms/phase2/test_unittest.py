# -*- coding: utf-8 -*-
"""
Test program comparing solutions with the builtin list-based one.

@author: EDA Team
"""

# Classes provided by EDA Team
from phase2 import BST2
import unittest

class Test(unittest.TestCase):
    def setUp(self):
        self.tree = BST2()
        input_list = [14,11,13,12,10,5,4,6,2,1,3,8,7,9,18,16,15,17,
            19,30,29,24,23,21,20,22,25,27,26,28,31,33,32,34,36,35,37]
    
        for x in input_list:
            
            self.tree.insert(x)
            
    def test_test01(self):
        print("Exercise 1, case 1: If the lenght negative")
        
        self.assertEqual(self.tree.find_dist_k(10, -1), None)
    
    def test_test02(self):
        print("Exercise 1, case 2: One of the parameters is not a number")
        
        self.assertEqual(self.tree.find_dist_k("texto", -1), None)
        
    def test_test03(self):
        print("Exercise 1, case 3: If the element is not in the tree")
        self.assertEqual(self.tree.find_dist_k(100, 0), None)

    def test_test04(self):
        print("Exercise 1, case 4: If the lenght is 0")
        self.assertEqual(self.tree.find_dist_k(24, 0), [24])
        
    def test_test05(self):
        print("Exercise 1, case 5: Any other case")
        self.assertEqual(self.tree.find_dist_k(17, 7),  [4,6,23,25,32,34])
        

# Some usage examples
if __name__ == '__main__':
    unittest.main()

