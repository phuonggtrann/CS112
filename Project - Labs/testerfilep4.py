# Based on testing harness dated 2017-06-02.

# STUDENTS: TO USE:
# 
# The following command will test all test cases on your file:
# 
#   python3 <thisfile.py> <your_one_file.py>
# 
# 
# You can also limit the tester to only the functions you want tested.
# Just add as many functions as you want tested on to the command line at the end.
# Example: to only run tests associated with func1 and func2, run this command:
# 
#   python3 <thisfile.py> <your_one_file.py> func1 func2
# 
# You really don't need to read the file any further, except that when
# a specific test fails, you'll get a line number - and it's certainly
# worth looking at those areas for details on what's being checked. This would
# all be the indented block of code starting with "class AllTests".


# INSTRUCTOR: TO PREPARE:
#  - add test cases to class AllTests. The test case functions' names must
# be precise - to test a function named foobar, the test must be named "test_foobar_#"
# where # may be any digits at the end, such as "test_foobar_13".
# - any extra-credit tests must be named "test_extra_credit_foobar_#"
# 
# - name all required definitions in REQUIRED_DEFNS, and all extra credit functions
#   in EXTRA_CREDIT_DEFNS. Do not include any unofficial helper functions. If you want
#   to make helper definitions to use while testing, those can also be added there for
#   clarity.
# 
# - to run on either a single file or all .py files in a folder (recursively):
#   python3 <thisfile.py> <your_one_file.py>
#   python3 <thisfile.py> <dir_of_files>
#   python3 <thisfile.py> .                    # current directory
# 
# A work in progress by Mark Snyder, Oct. 2015.
#  Edited by Yutao Zhong, Spring 2016.
#  Edited by Raven Russell, Spring 2017.
#  Edited by Mark Snyder, June 2017.


import unittest
import shutil
import sys
import os
import time

#import subprocess

import importlib

############################################################################
############################################################################
# BEGIN SPECIALIZATION SECTION (the only part you need to modify beyond 
# adding new test cases).

# name all expected definitions; if present, their definition (with correct
# number of arguments) will be used; if not, a decoy complainer function
# will be used, and all tests on that function should fail.
    
REQUIRED_DEFNS = [  "show",
                    "highest_point",
                    "on_map",
                    "is_map",
                    "neighbors",
                    "water_adjacent",
                    "count_coastline",
                    "on_ridge",
                    "is_peak",
                    "join_map_side",
                    "join_map_below",
                    "crop",
                    "flooded_map",
                    "flood_map",
                    "find_land",
                    "reorient",
                 ]

# for method names in classes that will be tested
SUB_DEFNS = [ ]

# definitions that are used for extra credit
EXTRA_CREDIT_DEFNS = ["get_island_spots", "connected_spots","remove_island"]

# how many points are test cases worth?
weight_required = 1
weight_extra_credit = 1

# don't count extra credit; usually 100% if this is graded entirely by tests.
# it's up to you the instructor to do the math and add this up!
# TODO: auto-calculate this based on all possible tests.
total_points_from_tests = 90

# how many seconds to wait between batch-mode gradings? 
# ideally we could enforce python to wait to open or import
# files when the system is ready but we've got a communication
# gap going on.
DELAY_OF_SHAME = 1


# set it to true when you run batch mode... 
CURRENTLY_GRADING = False



# what temporary file name should be used for the student?
# This can't be changed without hardcoding imports below, sorry.
# That's kind of the whole gimmick here that lets us import from
# the command-line argument without having to qualify the names.
RENAMED_FILE = "student"


def map1(): return [
         [0,0,0,0,0],
         [0,1,1,1,0],
         [0,1,3,1,0],
         [0,1,3,1,0],
         [0,1,3,1,0],
       ]

def map2(): return [
         [4,1,0, 0,0,0,2],
         [1,0,0,10,0,0,1],
         [0,0,1, 3,1,1,1],
       ]

def map3(): return [
         [5,4,5],
         [1,2,1],
         [0,1,1],
         [0,0,1],
         [6,3,1],
       ]

def map4(): return [
         [5,0,1,0,6],
         [0,0,0,9,0],
         [4,0,0,0,2],
         [0,0,0,0,0],
         [8,0,3,0,7],
       ]

def map5(): return [
         [ 0, 1, 0, 0, 0, 0, 0, 0],
         [ 0, 1, 1, 0, 0, 0, 0, 0],
         [ 1, 1, 2, 1, 1, 0, 0, 0],
         [ 0, 3, 5,12, 4, 1, 0, 0],
         [ 0, 1, 3, 5, 3, 1, 0, 0],
         [ 0, 0,11, 1, 1, 2, 1, 0],
         [ 0, 1, 1, 1, 2, 0, 0, 0],
         [ 0, 0, 1, 0, 0, 0, 0, 0],
       ]

def map6(): return [
         [4,6,7,6,5,4],
         [6,5,6,5,5,5],
         [6,5,3,4,5,6],
         [0,0,0,0,0,0],
         [8,8,8,8,8,6],
         [8,7,8,9,8,7],
         [8,8,8,8,8,6],
       ]


def map7(): return [
         [0,0,0,0,0,0],
         [0,5,0,0,5,0],
         [0,0,0,0,0,0],
         [0,5,0,0,5,0],
         [0,0,7,7,0,0],
         [0,6,0,0,6,0],
       ]

def map8(): return [
         [0,0,0,0,0,5,0,0],
         [0,1,0,0,6,5,0,0],
         [0,1,0,0,0,5,0,0],
         [0,1,2,2,0,5,0,0],
         [0,1,0,3,3,3,3,0],
         [0,0,0,0,4,0,0,0],
         [0,0,0,0,0,0,8,8],
         [0,0,0,0,0,8,8,8],
        ]


# END SPECIALIZATION SECTION
############################################################################
############################################################################


# enter batch mode by giving a directory to work on as the only argument.
BATCH_MODE = len(sys.argv)==2 and (sys.argv[1] in ["."] or os.path.isdir(sys.argv[1]))

# This class contains multiple "unit tests" that each check
# various inputs to specific functions, checking that we get
# the correct behavior (output value) from completing the call.
class AllTests (unittest.TestCase):
        
    ############################################################################
    
    # show tests
    def test_show_1  (self): self.assertEqual(show([[1,2,3],[4,5,6]]), "1 2 3\n4 5 6\n")
    def test_show_2  (self): self.assertEqual(show(map1()), '0 0 0 0 0\n0 1 1 1 0\n0 1 3 1 0\n0 1 3 1 0\n0 1 3 1 0\n')
    def test_show_3  (self): self.assertEqual(show(map2()), ' 4  1  0  0  0  0  2\n 1  0  0 10  0  0  1\n 0  0  1  3  1  1  1\n')
    def test_show_4  (self): self.assertEqual(show(map3()), '5 4 5\n1 2 1\n0 1 1\n0 0 1\n6 3 1\n')
    def test_show_5  (self): self.assertEqual(show(map4()), '5 0 1 0 6\n0 0 0 9 0\n4 0 0 0 2\n0 0 0 0 0\n8 0 3 0 7\n')
    def test_show_6  (self):
        m5 = map5()
        self.assertEqual(show(m5), ' 0  1  0  0  0  0  0  0\n 0  1  1  0  0  0  0  0\n 1  1  2  1  1  0  0  0\n 0  3  5 12  4  1  0  0\n 0  1  3  5  3  1  0  0\n 0  0 11  1  1  2  1  0\n 0  1  1  1  2  0  0  0\n 0  0  1  0  0  0  0  0\n')
        self.assertEqual(map5(),m5) # original must not be changed.
    def test_show_7  (self): self.assertEqual(show([[1,222,3],[45,5,678]]),"  1 222   3\n 45   5 678\n")

    # highest_point tests
    def test_highest_point_1  (self): self.assertEqual(highest_point(map1()), (2,2))
    def test_highest_point_2  (self): self.assertEqual(highest_point(map2()), (1,3))
    def test_highest_point_3  (self): self.assertEqual(highest_point(map3()), (4,0))
    def test_highest_point_4  (self): self.assertEqual(highest_point([[0,0,0],[0,0,0]]), None)
    def test_highest_point_5  (self): 
        self.assertEqual(highest_point(map5()), (3,3))
        m = [[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]]
        orig = [[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]]
        self.assertEqual(highest_point([[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]]), (0,0))
        self.assertEqual(orig, m) # original must not be changed.

    # on_map tests
    def test_on_map_1  (self): self.assertEqual(on_map(map1(),0,0), True)
    def test_on_map_2  (self): self.assertEqual(on_map(map1(),4,2), True)
    def test_on_map_3  (self): self.assertEqual(on_map(map2(),5,5), False)
    def test_on_map_4  (self): self.assertEqual(on_map(map3(),3,3), False)
    def test_on_map_5  (self):
        self.assertEqual(on_map(map3(),4,2), True)
        m = map5()
        self.assertEqual(on_map(m,-1, -3), False)
        self.assertEqual(map5(), m) # original must not be changed.

    # is_map tests
    def test_is_map_1  (self): self.assertEqual(is_map(map1()), True)
    def test_is_map_2  (self): self.assertEqual(is_map(map2()), True)
    def test_is_map_3  (self): self.assertEqual(is_map(map3()), True)
    def test_is_map_4  (self): self.assertEqual(is_map([]), False)
    def test_is_map_5  (self):
        # non-rectangular
        self.assertEqual(is_map([[1,2,3,4],[5],[6,7]]), False)
        
        # can't contain negatives
        self.assertEqual(is_map([[0,3],[-2,-5]]), False)
        
        # can't contain non-integers
        self.assertEqual(is_map([[True, "hi"],[3.0, {}]]),False)
        
        # must not change original map.
        m = [[-2,False, [1,2,3]], [4,5,6]]
        self.assertEqual(is_map(m), False)
        self.assertEqual(m,[[-2,False, [1,2,3]], [4,5,6]]) # original must not be changed.

    # neighbors tests
    def test_neighbors_1  (self):
        """middle area""" 
        self.assertEqual(neighbors(map1(),1,1), [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)])
    def test_neighbors_2  (self):
        """ upper edge"""
        self.assertEqual(neighbors(map2(),0,3), [(0, 2), (0, 4), (1, 2), (1, 3), (1, 4)])
    def test_neighbors_3  (self):
        """ lower-left corner"""
        self.assertEqual(neighbors(map2(),2,0), [(1, 0), (1, 1), (2, 1)])
    def test_neighbors_4  (self):
        """ lower-right corner"""
        self.assertEqual(neighbors(map4(),4,4), [(3, 3), (3, 4), (4, 3)])
    def test_neighbors_5  (self):
        """ right-side edge"""
        self.assertEqual(neighbors(map2(),1,6), [(0, 5), (0, 6), (1, 5), (2, 5), (2, 6)])
    def test_neighbors_6  (self):
        """ middle area"""
        m = map2()
        self.assertEqual(neighbors(m,1,5), [(0, 4), (0, 5), (0, 6), (1, 4), (1, 6), (2, 4), (2, 5), (2, 6)])
        self.assertEqual(map2(), m) # original must not be changed.
        self.assertEqual(neighbors(map1(),90,90),[])

    # water_adjacent tests
    def test_water_adjacent_1  (self): self.assertEqual(water_adjacent(map1(),1,1), True)
    def test_water_adjacent_2  (self): self.assertEqual(water_adjacent(map1(),2,2), False)
    def test_water_adjacent_3  (self): self.assertEqual(water_adjacent(map3(),2,2), True)
    def test_water_adjacent_4  (self): self.assertEqual(water_adjacent(map3(),0,0), False)
    def test_water_adjacent_5  (self):
        self.assertEqual(water_adjacent([[1,1,1],[1,0,1],[1,1,1]],1,1), False)
        
        m = map2()
        self.assertEqual(water_adjacent(m,1,6), True)
        self.assertEqual(map2(), m) # original must not be changed.
        
        # off-map locations aren't water-adjacent.
        self.assertEqual(water_adjacent(map1(),50,50), False)

    # count_coastline tests
    def test_count_coastline_1  (self): self.assertEqual(count_coastline(map1()), 9)
    def test_count_coastline_2  (self): self.assertEqual(count_coastline(map2()), 11)
    def test_count_coastline_3  (self): self.assertEqual(count_coastline([[1,1,1],[1,0,1],[1,1,1]]), 8)
    def test_count_coastline_4  (self): self.assertEqual(count_coastline([[0,0,0],[0,0,1],[1,0,0]]), 2)
    def test_count_coastline_5  (self):
        self.assertEqual(count_coastline(map5()), 23)
        
        m = [[0,1,1],[0,1,2],[0,1,3]]
        self.assertEqual(count_coastline(m), 3)
        self.assertEqual(m,[[0,1,1],[0,1,2],[0,1,3]]) # original must not be changed.

    # on_ridge tests
    def test_on_ridge_1  (self): self.assertEqual(on_ridge(map1(),2,2), True)
    def test_on_ridge_2  (self): self.assertEqual(on_ridge(map6(),1,1), True)
    def test_on_ridge_3  (self): self.assertEqual(on_ridge(map6(),1,3), False)
    def test_on_ridge_4  (self): self.assertEqual(on_ridge(map6(),1,4), True)
    def test_on_ridge_5  (self): self.assertEqual(on_ridge(map6(),5,1), False)
    def test_on_ridge_6  (self):
        m = map6()
        self.assertEqual(on_ridge(m,5,5), True)
        self.assertEqual(map6(), m) # original must not be changed.
        
        # off-map locations aren't on a ridge.
        self.assertEqual(on_ridge(map6(),7,6), False)

    # is_peak tests
    def test_is_peak_1  (self): self.assertEqual(is_peak(map2(),1,3), True)
    def test_is_peak_2  (self): self.assertEqual(is_peak(map2(),2,3), False)
    def test_is_peak_3  (self): self.assertEqual(is_peak(map5(),3,3), True)
    def test_is_peak_4  (self): self.assertEqual(is_peak(map5(),5,2), True)
    def test_is_peak_5  (self): self.assertEqual(is_peak(map4(),0,4), False)
    def test_is_peak_6  (self):
        m = map1()
        self.assertEqual(is_peak(m,2,2), False)
        self.assertEqual(map1(), m) # original must not be changed.

    # join_map_side tests
    def test_join_map_side_1  (self): self.assertEqual(join_map_side([[1,2],[5,6]], [[3,4],[7,8]]), [[1,2,3,4],[5,6,7,8]])
    def test_join_map_side_2  (self): self.assertEqual(join_map_side([[1],[2],[3],[4]], [[5],[6],[7],[8]]), [[1,5],[2,6],[3,7],[4,8]])
    def test_join_map_side_3  (self): self.assertEqual(join_map_side(map3(),map1()), [[5, 4, 5, 0, 0, 0, 0, 0], [1, 2, 1, 0, 1, 1, 1, 0], [0, 1, 1, 0, 1, 3, 1, 0], [0, 0, 1, 0, 1, 3, 1, 0], [6, 3, 1, 0, 1, 3, 1, 0]])
    def test_join_map_side_4  (self): self.assertEqual(join_map_side([[1,1,1],[1,1,1],[1,1,1]], join_map_side([[2,2,2],[2,2,2],[2,2,2]], [[3,3,3],[3,3,3],[3,3,3]])), [[1,1,1,2,2,2,3,3,3],[1,1,1,2,2,2,3,3,3],[1,1,1,2,2,2,3,3,3]])
    def test_join_map_side_5  (self):
        """ join_map_side: mismatched dimensions yield a None result."""
        m1 = map1()
        m2 = map2()
        m3 = map3()
        m5 = map5()
        self.assertEqual(join_map_side(m1,m2), None)
        self.assertEqual(join_map_side(m1,m5), None)
        self.assertEqual(join_map_side(m2,m3), None)
        self.assertEqual(join_map_side(m3,m2), None)
        self.assertEqual(map1(), m1) # original must not be changed.
        self.assertEqual(map2(), m2) # original must not be changed.
        self.assertEqual(map3(), m3) # original must not be changed.
        self.assertEqual(map5(), m5) # original must not be changed.
    def test_join_map_side_6  (self):
        m = [[1,2,3],[4,5,6]]
        ans = join_map_side(m,m)
        self.assertEqual(ans, [[1,2,3,1,2,3],[4,5,6,4,5,6]])
        # make sure we didn't cause any aliasing.
        self.assertNotEqual(id(m), id(ans))
        self.assertNotEqual(id(m[0]), id(ans[0]))
        self.assertNotEqual(id(m[1]), id(ans[1]))
        

    # join_map_below tests
    def test_join_map_below_1  (self): self.assertEqual(join_map_below([[1,1,1],[2,2,2]], [[3,3,3],[4,4,4]]), [[1,1,1],[2,2,2],[3,3,3],[4,4,4]])
    def test_join_map_below_2  (self): self.assertEqual(join_map_below([[1,2,3,4]],[[5,6,7,8]]), [[1,2,3,4],[5,6,7,8]])
    def test_join_map_below_3  (self):
        self.assertEqual(join_map_below(map1(),map1()), [[0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 1, 3, 1, 0], [0, 1, 3, 1, 0], [0, 1, 3, 1, 0], [0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 1, 3, 1, 0], [0, 1, 3, 1, 0], [0, 1, 3, 1, 0]])
        self.assertEqual(join_map_below(map4(),map1()), [[5, 0, 1, 0, 6], [0, 0, 0, 9, 0], [4, 0, 0, 0, 2], [0, 0, 0, 0, 0], [8, 0, 3, 0, 7], [0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 1, 3, 1, 0], [0, 1, 3, 1, 0], [0, 1, 3, 1, 0]])
    def test_join_map_below_4  (self):
        m1 = map1()
        m2 = map2()
        m3 = map3()
        m5 = map5()
        self.assertEqual(join_map_below(m1,m2), None)
        self.assertEqual(join_map_below(m2,m1), None)
        self.assertEqual(join_map_below(m1,m3), None)
        self.assertEqual(join_map_below(m3,m1), None)
        self.assertEqual(join_map_below(m1,m5), None)
        self.assertEqual(map1(), m1) # original must not be changed.
        self.assertEqual(map2(), m2) # original must not be changed.
        self.assertEqual(map3(), m3) # original must not be changed.
        self.assertEqual(map5(), m5) # original must not be changed.
    def test_join_map_below_5  (self):
        m = [[1,2,3],[4,5,6]]
        ans = join_map_below(m,m)
        self.assertEqual(ans, [[1,2,3],[4,5,6],[1,2,3],[4,5,6]])
        # make sure we didn't cause any aliasing.
        self.assertNotEqual(id(m), id(ans))
        self.assertNotEqual(id(m[0]), id(ans[0]))
        self.assertNotEqual(id(m[1]), id(ans[1]))
        
    # crop tests
    def test_crop_1  (self): self.assertEqual(crop(map1(),1,1,3,3), [[1,1,1],[1,3,1],[1,3,1]])
    def test_crop_2  (self): self.assertEqual(crop(map2(),0,0,2,3), [[4,1,0,0],[1,0,0,10],[0,0,1,3]])
    def test_crop_3  (self): self.assertEqual(crop(map5(),3,1,3,4), [[3,5,12,4]])
    def test_crop_4  (self): self.assertEqual(crop(map2(),0,3,2,5), [[0,0,0],[10,0,0],[3,1,1]])
    def test_crop_5  (self): self.assertEqual(crop(map2(),1,1,90,90), [[0,0,10,0,0,1],[0,1,3,1,1,1]])
    def test_crop_6  (self):
        m1 = map1()
        self.assertEqual(crop(m1,2,2,1,3), [])
        self.assertEqual(crop(m1,2,2,3,1), [])
        self.assertEqual(crop(m1,2,2,1,1), [])
        self.assertEqual(crop(m1,8,8,4,4), [])
        self.assertEqual(map1(), m1) # original must not be changed.
    def test_crop_7  (self):
        m = [[1,2,3],[4,5,6]]
        ans = crop(m,0,0,1,2)
        self.assertEqual(ans, [[1,2,3],[4,5,6]])
        # make sure we didn't cause any aliasing.
        self.assertNotEqual(id(m), id(ans))

    # flooded_map tests
    def test_flooded_map_1  (self): self.assertEqual(flooded_map(map1(),2), [[0,0,0,0,0],[0,0,0,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0]])
    def test_flooded_map_2  (self): self.assertEqual(flooded_map(map2(),3), [[1,0,0,0,0,0,0],[0,0,0,7,0,0,0],[0,0,0,0,0,0,0]])
    def test_flooded_map_3  (self): self.assertEqual(flooded_map([[5,5,5],[4,4,4],[3,3,3],[0,0,0]],3), [[2,2,2],[1,1,1],[0,0,0],[0,0,0]])
    def test_flooded_map_4  (self): self.assertEqual(flooded_map(map7(),3), [[0, 0, 0, 0, 0, 0], [0, 2, 0, 0, 2, 0], [0, 0, 0, 0, 0, 0], [0, 2, 0, 0, 2, 0], [0, 0, 4, 4, 0, 0], [0, 3, 0, 0, 3, 0]])
    def test_flooded_map_5  (self): self.assertEqual(flooded_map(map7(),5), [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 2, 2, 0, 0], [0, 1, 0, 0, 1, 0]])
    def test_flooded_map_6  (self):
        orig = [[1,2,3],[2,5,4],[1,1,1],[0,0,0]]
        ans = flooded_map(orig,2)
        self.assertEqual(ans,  [[0,0,1],[0,3,2],[0,0,0],[0,0,0]])
        self.assertEqual(orig, [[1,2,3],[2,5,4],[1,1,1],[0,0,0]]) # original must not be changed.

    # flood_map tests
    def test_flood_map_1  (self):
        m = [[3,3,3],[2,2,2]]
        flood_map(m,2)
        self.assertEqual(m,[[1,1,1],[0,0,0]])
    def test_flood_map_2  (self):
        m = [[10,10,4],[9,9,5],[8,8,6]]
        flood_map(m,4)
        self.assertEqual(m,[[6,6,0],[5,5,1],[4,4,2]])
    def test_flood_map_3  (self):
        m = [[10,10,4],[9,9,5],[8,8,6]]
        flood_map(m,9)
        self.assertEqual(m,[[1,1,0],[0,0,0],[0,0,0]])
    def test_flood_map_4  (self):
        # over-flooding reduces everything to water
        m = [[3,3],[2,2],[1,1]]
        flood_map(m,20)
        self.assertEqual(m,[[0,0],[0,0],[0,0]])
        # and sometimes only the middle becomes water.
        m = [[5,6],[2,3],[9,10]]
        flood_map(m,4)
        self.assertEqual(m,[[1,2],[0,0],[5,6]])
    def test_flood_map_6  (self):
        m = [[3,3,3],[2,2,2]]
        ans = flood_map(m,0)
        self.assertEqual(m,[[3,3,3],[2,2,2]])
        self.assertEqual(ans, None) # function should work in place and return None.

    # find_land tests
    def test_find_land_1  (self): self.assertEqual(find_land(map4(),2,2,"S"), 2)
    def test_find_land_2  (self): self.assertEqual(find_land(map4(),4,1,"NE"), None )
    def test_find_land_3  (self): self.assertEqual(find_land(map5(),7,0,"N"), 5)
    def test_find_land_4  (self):
        self.assertEqual(find_land(map1(),1,1,"W"), 0)
        self.assertEqual(find_land([[0,0,0,0,0,0,0,0,0,4]],0,0,"E"), 9)
    def test_find_land_6  (self):
        m3 = map3()
        m5 = map5()
        m7 = map7()
        self.assertEqual(find_land(m3,3,1,"SE"), 1)
        self.assertEqual(find_land(m7,5,5,"NW"), 4)
        self.assertEqual(find_land(m5,0,5,"SW"), 2)
        self.assertEqual(find_land(m5,0,6,"W"), 5)
        self.assertEqual(map3(), m3) # original must not be changed.
        self.assertEqual(map5(), m5) # original must not be changed.
        self.assertEqual(map7(), m7) # original must not be changed.

    # reorient tests
    def test_reorient_1 (self): self.assertEqual(reorient([[1,2],[3,4]]), [[3,1],[4,2]])
    def test_reorient_2 (self): self.assertEqual(reorient([[1,2,3],[4,5,6],[7,8,9],[10,11,12]]),    [[10, 7, 4, 1], [11, 8, 5, 2], [12, 9, 6, 3]])
    def test_reorient_3 (self): self.assertEqual(reorient(map1()), [[0, 0, 0, 0, 0], [1, 1, 1, 1, 0], [3, 3, 3, 1, 0], [1, 1, 1, 1, 0], [0, 0, 0, 0, 0]])
    def test_reorient_4 (self): self.assertEqual(reorient(map2()), [[0, 1, 4], [0, 0, 1], [1, 0, 0], [3, 10, 0], [1, 0, 0], [1, 0, 0], [1, 1, 2]])
    def test_reorient_5 (self): self.assertEqual(reorient(map3()), [[6, 0, 0, 1, 5], [3, 0, 1, 2, 4], [1, 1, 1, 1, 5]])
    def test_reorient_6 (self):
        m = [[1,2,3],[4,5,6],[7,8,9]]
        self.assertEqual(reorient(reorient(m)), [[9, 8, 7], [6, 5, 4], [3, 2, 1]])
        self.assertEqual(m,[[1,2,3],[4,5,6],[7,8,9]]) # original must not be changed.

    # extra credit:
    def test_extra_credit_get_island_spots_1 (self): self.assertEqual(get_island_spots(map7(),3,1), [(3, 1), (3, 4), (4, 2), (4, 3), (5, 1), (5, 4)])
    def test_extra_credit_get_island_spots_2 (self): self.assertEqual(get_island_spots(map8(),3,2), [(0, 5), (1, 1), (1, 4), (1, 5), (2, 1), (2, 5), (3, 1), (3, 2), (3, 3), (3, 5), (4, 1), (4, 3), (4, 4), (4, 5), (4, 6), (5, 4)])
    def test_extra_credit_get_island_spots_3 (self): self.assertEqual(get_island_spots(map8(),6,7), [(6, 6), (6, 7), (7, 5), (7, 6), (7, 7)])
    def test_extra_credit_connected_spots_1 (self):
        m6 = map6()
        m8 = map8()
        self.assertEqual(connected_spots(m6,2,0,1,5),True)
        self.assertEqual(connected_spots(m6,2,0,5,5),False)
        self.assertEqual(connected_spots(m8,1,1,4,3),True)
        self.assertEqual(connected_spots(m8,4,6,6,6),False)
        self.assertEqual(map6(), m6) # original must not be changed.
        self.assertEqual(map8(), m8) # original must not be changed.
    
    def test_extra_credit_remove_island_1 (self):
        m1 = [[1,2,0,0],[2,1,0,0],[0,0,0,4],[0,0,0,5]]
        remove_island(m1,0,0)
        self.assertEqual(m1, [[0,0,0,0],[0,0,0,0],[0,0,0,4],[0,0,0,5]])
        ans = remove_island(m1,2,3)
        self.assertEqual(m1, [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
        self.assertEqual(ans, None) # must return a None after making updates.

    ############################################################################
    
# This class digs through AllTests, counts and builds all the tests,
# so that we have an entire test suite that can be run as a group.
class TheTestSuite (unittest.TestSuite):
    # constructor.
    def __init__(self,wants):
        self.num_req = 0
        self.num_ec = 0
        # find all methods that begin with "test".
        fs = []
        for w in wants:
            for func in AllTests.__dict__:
                # append regular tests
                # drop any digits from the end of str(func).
                dropnum = str(func)
                while dropnum[-1] in "1234567890":
                    dropnum = dropnum[:-1]
                
                if dropnum==("test_"+w+"_") and (not (dropnum==("test_extra_credit_"+w+"_"))):
                    fs.append(AllTests(str(func)))
                if dropnum==("test_extra_credit_"+w+"_") and not BATCH_MODE:
                    fs.append(AllTests(str(func)))
        
#       print("TTS ====> ",list(map(lambda f: (f,id(f)),fs)))
        # call parent class's constructor.
        unittest.TestSuite.__init__(self,fs)

class TheExtraCreditTestSuite (unittest.TestSuite):
        # constructor.
        def __init__(self,wants):
            # find all methods that begin with "test_extra_credit_".
            fs = []
            for w in wants:
                for func in AllTests.__dict__:
                    if str(func).startswith("test_extra_credit_"+w):
                        fs.append(AllTests(str(func)))
        
#           print("TTS ====> ",list(map(lambda f: (f,id(f)),fs)))
            # call parent class's constructor.
            unittest.TestSuite.__init__(self,fs)

# all (non-directory) file names, regardless of folder depth,
# under the given directory 'dir'.
def files_list(dir):
    this_file = __file__
    if dir==".":
        dir = os.getcwd()
    info = os.walk(dir)
    filenames = []
    for (dirpath,dirnames,filez) in info:
#       print(dirpath,dirnames,filez)
        if dirpath==".":
            continue
        for file in filez:
            if file==this_file:
                continue
            filenames.append(os.path.join(dirpath,file))
#       print(dirpath,dirnames,filez,"\n")
    return filenames

def main():
    if len(sys.argv)<2:
        raise Exception("needed student's file name as command-line argument:"\
            +"\n\t\"python3 testerX.py gmason76_2xx_Px.py\"")
    
    if BATCH_MODE:
        print("BATCH MODE.\n")
        run_all()
        return
        
    else:
        want_all = len(sys.argv) <=2
        wants = []
        # remove batch_mode signifiers from want-candidates.
        want_candidates = sys.argv[2:]
        for i in range(len(want_candidates)-1,-1,-1):
            if want_candidates[i] in ['.'] or os.path.isdir(want_candidates[i]):
                del want_candidates[i]
    
        # set wants and extra_credits to either be the lists of things they want, or all of them when unspecified.
        wants = []
        extra_credits = []
        if not want_all:
            for w in want_candidates:
                if w in REQUIRED_DEFNS:
                    wants.append(w)
                elif w in SUB_DEFNS:
                    wants.append(w)
                elif w in EXTRA_CREDIT_DEFNS:
                    extra_credits.append(w)
                else:
                    raise Exception("asked to limit testing to unknown function '%s'."%w)
        else:
            wants = REQUIRED_DEFNS + SUB_DEFNS
            extra_credits = EXTRA_CREDIT_DEFNS
        
        # now that we have parsed the function names to test, run this one file.    
        run_one(wants,extra_credits)    
        return
    return # should be unreachable! 

# only used for non-batch mode, since it does the printing.
# it nicely prints less info when no extra credit was attempted.
def run_one(wants, extra_credits):
    
    has_reqs = len(wants)>0
    has_ec   = len(extra_credits)>0
    
    # make sure they exist.
    passed1 = 0
    passed2 = 0
    tried1 = 0
    tried2 = 0
    
    # only run tests if needed.
    if has_reqs:
        print("\nRunning required definitions:")
        (tag, passed1,tried1) = run_file(sys.argv[1],wants,False)
    if has_ec:
        print("\nRunning extra credit definitions:")
        (tag, passed2,tried2) = run_file(sys.argv[1],extra_credits,True)
    
    # print output based on what we ran.
    if has_reqs and not has_ec:
        print("\n%d/%d Required test cases passed (worth %d each)" % (passed1,tried1,weight_required) )
        print("\nScore based on test cases: %.2f/%d (%.2f*%d) " % (
                                                                passed1*weight_required, 
                                                                total_points_from_tests,
                                                                passed1,
                                                                weight_required
                                                             ))
    elif has_ec and not has_reqs:
        print("%d/%d Extra credit test cases passed (worth %d each)" % (passed2, tried2, weight_extra_credit))
    else: # has both, we assume.
        print("\n%d / %d Required test cases passed (worth %d each)" % (passed1,tried1,weight_required) )
        print("%d / %d Extra credit test cases passed (worth %d each)" % (passed2, tried2, weight_extra_credit))
        print("\nScore based on test cases: %.2f / %d ( %d * %d + %d * %d) " % (
                                                                passed1*weight_required+passed2*weight_extra_credit, 
                                                                total_points_from_tests,
                                                                passed1,
                                                                weight_required,
                                                                passed2,
                                                                weight_extra_credit
                                                             ))
    if CURRENTLY_GRADING:
        print("( %d %d %d %d )\n%s" % (passed1,tried1,passed2,tried2,tag))

# only used for batch mode.
def run_all():
        filenames = files_list(sys.argv[1])
        #print(filenames)
        
        wants = REQUIRED_DEFNS + SUB_DEFNS
        extra_credits = EXTRA_CREDIT_DEFNS
        
        results = []
        for filename in filenames:
            print(" Batching on : " +filename)
            # I'd like to use subprocess here, but I can't get it to give me the output when there's an error code returned... TODO for sure.
            lines = os.popen("python3 tester1p.py \""+filename+"\"").readlines()
            
            # delay of shame...
            time.sleep(DELAY_OF_SHAME)
            
            name = os.path.basename(lines[-1])
            stuff =lines[-2].split(" ")[1:-1]
            print("STUFF: ",stuff, "LINES: ", lines)
            (passed_req, tried_req, passed_ec, tried_ec) = stuff
            results.append((lines[-1],int(passed_req), int(tried_req), int(passed_ec), int(tried_ec)))
            continue
        
        print("\n\n\nGRAND RESULTS:\n")
        
            
        for (tag_req, passed_req, tried_req, passed_ec, tried_ec) in results:
            name = os.path.basename(tag_req).strip()
            earned   = passed_req*weight_required + passed_ec*weight_extra_credit
            possible = tried_req *weight_required # + tried_ec *weight_extra_credit
            print("%10s : %3d / %3d = %5.2d %% (%d/%d*%d + %d/%d*%d)" % (
                                                            name,
                                                            earned,
                                                            possible, 
                                                            (earned/possible)*100,
                                                            passed_req,tried_req,weight_required,
                                                            passed_ec,tried_ec,weight_extra_credit
                                                          ))
# only used for batch mode.
def run_all_orig():
        filenames = files_list(sys.argv[1])
        #print(filenames)
        
        wants = REQUIRED_DEFNS + SUB_DEFNS
        extra_credits = EXTRA_CREDIT_DEFNS
        
        results = []
        for filename in filenames:
            # wipe out all definitions between users.
            for fn in REQUIRED_DEFNS+EXTRA_CREDIT_DEFNS :
                globals()[fn] = decoy(fn)
                fn = decoy(fn)
            try:
                name = os.path.basename(filename)
                print("\n\n\nRUNNING: "+name)
                (tag_req, passed_req, tried_req) = run_file(filename,wants,False)
                (tag_ec,  passed_ec,  tried_ec ) = run_file(filename,extra_credits,True)
                results.append((tag_req,passed_req,tried_req,tag_ec,passed_ec,tried_ec))
                print(" ###### ", results)
            except SyntaxError as e:
                tag = filename+"_SYNTAX_ERROR"
                results.append((tag,0,len(wants),tag,0,len(extra_credits)))
            except NameError as e:
                tag =filename+"_Name_ERROR"
                results.append((tag,0,len(wants),tag,0,len(extra_credits)))
            except ValueError as e:
                tag = filename+"_VALUE_ERROR"
                results.append((tag,0,len(wants),tag,0,len(extra_credits)))
            except TypeError as e:
                tag = filename+"_TYPE_ERROR"
                results.append((tag,0,len(wants),tag,0,len(extra_credits)))
            except ImportError as e:
                tag = filename+"_IMPORT_ERROR_TRY_AGAIN"
                results.append((tag,0,len(wants),tag,0,len(extra_credits)))
            except Exception as e:
                tag = filename+str(e.__reduce__()[0])
                results.append((tag,0,len(wants),tag,0,len(extra_credits)))
        
#           try:
#               print("\n |||||||||| scrupe: "+str(scruples))
#           except Exception as e:
#               print("NO SCRUPE.",e)
#           scruples = None
        
        print("\n\n\nGRAND RESULTS:\n")
        for (tag_req, passed_req, tried_req, tag_ec, passed_ec, tried_ec) in results:
            name = os.path.basename(tag_req)
            earned   = passed_req*weight_required + passed_ec*weight_extra_credit
            possible = tried_req *weight_required # + tried_ec *weight_extra_credit
            print("%10s : %3d / %3d = %5.2d %% (%d/%d*%d + %d/%d*%d)" % (
                                                            name,
                                                            earned,
                                                            possible, 
                                                            (earned/possible)*100,
                                                            passed_req,tried_req,weight_required,
                                                            passed_ec,tried_ec,weight_extra_credit
                                                          ))

def try_copy(filename1, filename2, numTries):
    have_copy = False
    i = 0
    while (not have_copy) and (i < numTries):
        try:
            # move the student's code to a valid file.
            shutil.copy(filename1,filename2)
            
            # wait for file I/O to catch up...
            if(not wait_for_access(filename2, numTries)):
                return False
                
            have_copy = True
        except PermissionError:
            print("Trying to copy "+filename1+", may be locked...")
            i += 1
            time.sleep(1)
        except BaseException as e:
            print("\n\n\n\n\n\ntry-copy saw: "+e)
    
    if(i == numTries):
        return False
    return True

def try_remove(filename, numTries):
    removed = False
    i = 0
    while os.path.exists(filename) and (not removed) and (i < numTries):
        try:
            os.remove(filename)
            removed = True
        except OSError:
            print("Trying to remove "+filename+", may be locked...")
            i += 1
            time.sleep(1)
    if(i == numTries):
        return False
    return True

def wait_for_access(filename, numTries):
    i = 0
    while (not os.path.exists(filename) or not os.access(filename, os.R_OK)) and i < numTries:
        print("Waiting for access to "+filename+", may be locked...")
        time.sleep(1)
        i += 1
    if(i == numTries):
        return False
    return True

# this will group all the tests together, prepare them as 
# a test suite, and run them.
def run_file(filename,wants=None,checking_ec = False):
    if wants==None:
        wants = []
    
    # move the student's code to a valid file.
    if(not try_copy(filename,"student.py", 5)):
        print("Failed to copy " + filename + " to student.py.")
        quit()
        
    # import student's code, and *only* copy over the expected functions
    # for later use.
    import importlib
    count = 0
    while True:
        try:
#           print("\n\n\nbegin attempt:")
            while True:
                try:
                    f = open("student.py","a")
                    f.close()
                    break
                except:
                    pass
#           print ("\n\nSUCCESS!")
                
            import student
            importlib.reload(student)
            break
        except ImportError as e:
            print("import error getting student... trying again. "+os.getcwd(), os.path.exists("student.py"),e)
            time.sleep(0.5)
            while not os.path.exists("student.py"):
                time.sleep(0.5)
            count+=1
            if count>3:
                raise ImportError("too many attempts at importing!")
        except SyntaxError as e:
            print("SyntaxError in "+filename+":\n"+str(e))
            print("Run your file without the tester to see the details")
            return(filename+"_SYNTAX_ERROR",None, None, None)
        except NameError as e:
            print("NameError in "+filename+":\n"+str(e))
            print("Run your file without the tester to see the details")
            return((filename+"_Name_ERROR",0,1))    
        except ValueError as e:
            print("ValueError in "+filename+":\n"+str(e))
            print("Run your file without the tester to see the details")
            return(filename+"_VALUE_ERROR",0,1)
        except TypeError as e:
            print("TypeError in "+filename+":\n"+str(e))
            print("Run your file without the tester to see the details")
            return(filename+"_TYPE_ERROR",0,1)
        except ImportError as e:            
            print("ImportError in "+filename+":\n"+str(e))
            print("Run your file without the tester to see the details or try again")
            return((filename+"_IMPORT_ERROR_TRY_AGAIN   ",0,1)) 
        except Exception as e:
            print("Exception in loading"+filename+":\n"+str(e))
            print("Run your file without the tester to see the details")
            return(filename+str(e.__reduce__()[0]),0,1)
    
    # make a global for each expected definition.
    for fn in REQUIRED_DEFNS+EXTRA_CREDIT_DEFNS :
        globals()[fn] = decoy(fn)
        try:
            globals()[fn] = getattr(student,fn)
        except:
            if fn in wants:
                print("\nNO DEFINITION FOR '%s'." % fn) 
    
    if not checking_ec:
        # create an object that can run tests.
        runner = unittest.TextTestRunner()
    
        # define the suite of tests that should be run.
        suite = TheTestSuite(wants)
    
    
        # let the runner run the suite of tests.
        ans = runner.run(suite)
        num_errors   = len(ans.__dict__['errors'])
        num_failures = len(ans.__dict__['failures'])
        num_tests    = ans.__dict__['testsRun']
        num_passed   = num_tests - num_errors - num_failures
        # print(ans)
    
    else:
        # do the same for the extra credit.
        runner = unittest.TextTestRunner()
        suite = TheExtraCreditTestSuite(wants)
        ans = runner.run(suite)
        num_errors   = len(ans.__dict__['errors'])
        num_failures = len(ans.__dict__['failures'])
        num_tests    = ans.__dict__['testsRun']
        num_passed   = num_tests - num_errors - num_failures
        #print(ans)
    
    # remove our temporary file.
    os.remove("student.py")
    if os.path.exists("__pycache__"):
        shutil.rmtree("__pycache__")
    if(not try_remove("student.py", 5)):
        print("Failed to remove " + filename + " to student.py.")
    
    tag = ".".join(filename.split(".")[:-1])
    
    
    return (tag, num_passed, num_tests)


# make a global for each expected definition.
def decoy(name):
        # this can accept any kind/amount of args, and will print a helpful message.
        def failyfail(*args, **kwargs):
            return ("<no '%s' definition was found - missing, or typo perhaps?>" % name)
        return failyfail

# this determines if we were imported (not __main__) or not;
# when we are the one file being run, perform the tests! :)
if __name__ == "__main__":
    main()