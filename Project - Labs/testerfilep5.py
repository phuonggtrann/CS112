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
	
REQUIRED_DEFNS = ["read_votes",
                  "read_abbreviations",
                  "write_votes",
                  "add_candidate",
                  "remove_candidate",
                  "merge_votes",
                  "incorporate_precinct",
                  "number_of_votes",
                  "popular_votes_performance",
                  "candidates_difference"
                  ]

# for method names in classes that will be tested
SUB_DEFNS = ["combined"]

# definitions that are used for extra credit
EXTRA_CREDIT_DEFNS = ["reverse_result"]

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

def getDict():
	return {'GA': [('Allen', 'W', 5, 0), ('Buchanan', 'W', 31, 0), ('Byrne', 'W', 8, 0), ('Castle', 'W', 1110, 0), ('Clinton', 'DEM', 1877963, 0), ('Collins', 'W', 22, 0), ('Cubbler', 'W', 24, 0), ('Elliott', 'W', 15, 0), ('Fox', 'W', 78, 0), ('Hoefling', 'W', 70, 0), ('Johnson', 'LIB', 125306, 0), ('Kotlikoff', 'W', 34, 0), ('Maturen', 'W', 151, 0), ('McMullin', 'W', 13017, 0), ('Muhammad', 'W', 30, 0), ('Smith', 'W', 53, 0), ('Stein', 'W', 7674, 0), ('Trump', 'REP', 2089104, 16), ('Urbach', 'W', 5, 0), ('Wilson', 'W', 32, 0)], 'RI': [('Abstain', 'W', 5, 0), ('AnyoneElse', 'W', 7, 0), ('Belichek', 'W', 19, 0), ('Biden', 'W', 160, 0), ('Bloomberg', 'W', 32, 0), ('Brady', 'W', 86, 0), ('Buffet', 'W', 5, 0), ('Buffett', 'W', 7, 0), ('Bush', 'W', 71, 0), ('Carson', 'W', 66, 0), ('Castle', 'W', 52, 0), ('Chaffee', 'W', 8, 0), ('Chrisley', 'W', 19, 0), ('Christ', 'W', 70, 0), ('Christie', 'W', 11, 0), ('Clinton', 'DEM', 252525, 4), ('CohenT', 'W', 18, 0), ('CooperA', 'W', 5, 0), ('Cruz', 'W', 46, 0), ('DeLaFuente', 'ADP', 671, 0), ('Duck', 'W', 18, 0), ('Fecteau', 'W', 8, 0), ('Fiorina', 'W', 12, 0), ('GodAlmighty', 'W', 20, 0), ('GodHelpUs', 'W', 5, 0), ('Gowdy', 'W', 8, 0), ('Harambe', 'W', 15, 0), ('Healey', 'W', 5, 0), ('Hoefling', 'W', 7, 0), ('Huckabee', 'W', 9, 0), ('Johnson', 'LIB', 14746, 0), ('Kaine', 'W', 7, 0), ('Kasich', 'W', 695, 0), ('Kenniston', 'W', 6, 0), ('LaRiva', 'W', 8, 0), ('Lincoln', 'W', 13, 0), ('Maturen', 'W', 34, 0), ('McCain', 'W', 124, 0), ('McMullin', 'W', 773, 0), ('Me', 'W', 6, 0), ('Mouse', 'W', 79, 0), ('Murray', 'W', 5, 0), ('NA', 'W', 6, 0), ('Neuman', 'W', 8, 0), ('NoConfidence', 'W', 15, 0), ('NoOne', 'W', 8, 0), ('None', 'W', 19, 0), ('NoneOfTheAbove', 'W', 70, 0), ('Norton', 'W', 6, 0), ('Nutz', 'W', 6, 0), ('ObamaB', 'W', 13, 0), ('ObamaM', 'W', 34, 0), ('Pence', 'W', 291, 0), ('Pope Francis', 'W', 7, 0), ('Powell', 'W', 41, 0), ('RandPaul', 'W', 18, 0), ('Reagan', 'W', 5, 0), ('Reed', 'W', 5, 0), ('Rice', 'W', 26, 0), ('Romney', 'W', 273, 0), ('RonPaul', 'W', 11, 0), ('Roosevelt', 'W', 6, 0), ('Rubio', 'W', 99, 0), ('Ryan', 'W', 249, 0), ('Sanders', 'W', 3497, 0), ('Scattered', 'W', 2121, 0), ('Stein', 'GRE', 6220, 0), ('Supreme', 'W', 17, 0), ('Trump', 'REP', 180543, 0), ('UnityLoveHarmony', 'W', 5, 0), ('Ventura', 'W', 8, 0), ('Warren', 'W', 12, 0), ('Washington', 'W', 5, 0), ('Webb', 'W', 7, 0), ('WilliamsR', 'W', 7, 0)], 'NJ': [('Castle', 'CON', 6161, 0), ('Clinton', 'DEM', 2148278, 14), ('DeLaFuente', 'ADP', 1838, 0), ('Johnson', 'LIB', 72477, 0), ('Kennedy', 'SWP', 2156, 0), ('LaRiva', 'SLP', 1682, 0), ('Moorehead', 'WW', 1749, 0), ('Stein', 'GRE', 37772, 0), ('Trump', 'REP', 1601933, 0)], 'FL': [('Basiago', 'W', 24, 0), ('Castle', 'CPF', 16475, 0), ('Clinton', 'DEM', 4504975, 0), ('DeLaFuente', 'RPF', 9108, 0), ('Duncan', 'W', 25, 0), ('Fox', 'W', 2, 0), ('Gyurko', 'W', 19, 0), ('Johnson', 'LBF', 207043, 0), ('Kotlikoff', 'W', 74, 0), ('Stein', 'GPF', 64399, 0), ('Trump', 'REP', 4617886, 29), ('Valdivia', 'W', 9, 0)], 'NC': [('Clinton', 'DEM', 2189316, 0), ('Johnson', 'LIB', 130126, 0), ('Scattered', 'W', 47386, 0), ('Stein', 'W', 12105, 0), ('Trump', 'REP', 2362631, 15)], 'CA': [('Clinton', 'DEM', 8753792, 55), ('Johnson', 'LIB', 478500, 0), ('Kotlikoff', 'W', 402, 0), ('LaRiva', 'PAF', 66101, 0), ('Maturen', 'W', 1316, 0), ('McMullin', 'W', 39596, 0), ('Sanders', 'W', 79341, 0), ('Stein', 'GRE', 278658, 0), ('Trump', 'REP/AIP', 4483814, 0), ('White', 'W', 84, 0)], 'MS': [('Castle', 'CON', 3987, 0), ('Clinton', 'DEM', 485131, 0), ('DeLaFuente', 'ADP', 644, 0), ('Hedges', 'P', 715, 0), ('Johnson', 'LIB', 14435, 0), ('Stein', 'GRE', 3731, 0), ('Trump', 'REP', 700714, 6)], 'OH': [('Bell', 'W', 9, 0), ('Bickelmeyer', 'W', 6, 0), ('Castle', 'W', 1887, 0), ('Clinton', 'DEM', 2394164, 0), ('Duncan', 'N', 24235, 0), ('Fox', 'W', 5, 0), ('Hartnell', 'W', 589, 0), ('Hoefling', 'W', 268, 0), ('Jaynes', 'W', 8, 0), ('Johnson', 'N', 174498, 0), ('Keniston', 'W', 114, 0), ('Kirschner', 'W', 15, 0), ('Kotlikoff', 'W', 90, 0), ('Maldonado', 'W', 18, 0), ('Maturen', 'W', 552, 0), ('McMullin', 'W', 12574, 0), ('Moorehead', 'W', 19, 0), ('Schriner', 'W', 62, 0), ('Smith', 'W', 62, 0), ('Stein', 'GRE', 46271, 0), ('Stroh', 'W', 30, 0), ('Thomson', 'W', 6, 0), ('Trump', 'REP', 2841005, 18)], 'MA': [('AllOthers', 'W', 50488, 0), ('Clinton', 'DEM', 1995196, 11), ('Feegbeh', 'W', 28, 0), ('Johnson', 'LIB', 138018, 0), ('Kotlikoff', 'W', 28, 0), ('McMullin', 'W', 2719, 0), ('Moorehead', 'W', 15, 0), ('Stein', 'GR', 47661, 0), ('Trump', 'REP', 1090893, 0)], 'SD': [('Castle', 'CON', 4064, 0), ('Clinton', 'DEM', 117458, 0), ('Johnson', 'LIB', 20850, 0), ('Trump', 'REP', 227721, 3)], 'WV': [('Basiago', 'W', 4, 0), ('Buchanan', 'W', 3, 0), ('Castle', 'CON', 3807, 0), ('Clinton', 'DEM', 188794, 0), ('DeLaFuente', 'W', 3, 0), ('Duncan', 'W', 1, 0), ('Hartnell', 'W', 1, 0), ('Hoefling', 'W', 10, 0), ('Johnson', 'LIB', 23004, 0), ('Kotlikoff', 'W', 4, 0), ('LaRiva', 'W', 2, 0), ('Limbaugh', 'W', 3, 0), ('Maldonado', 'W', 1, 0), ('McMullin', 'W', 1104, 0), ('Moreau', 'W', 216, 0), ('PerryDarryl', 'W', 2, 0), ('Smith', 'W', 2, 0), ('SmithW', 'W', 13, 0), ('Stein', 'MTP', 8075, 0), ('Trump', 'REP', 489371, 5), ('White', 'W', 2, 0), ('Williams', 'W', 1, 0)], 'AR': [('Castle', 'CON', 4613, 0), ('Clinton', 'DEM', 380494, 0), ('Hedges', 'IND', 4709, 0), ('Johnson', 'LIB', 29949, 0), ('Kahn', 'IND', 3390, 0), ('McMullin', 'BFA', 13176, 0), ('Stein', 'GRE', 9473, 0), ('Trump', 'REP', 684872, 6)], 'DE': [('Buchanan', 'W', 4, 0), ('Castle', 'W', 74, 0), ('Clinton', 'DEM', 235603, 3), ('DeLaFuente', 'W', 3, 0), ('Duncan', 'W', 1, 0), ('Hartnell', 'W', 3, 0), ('Hoefling', 'W', 7, 0), ('Johnson', 'LIB', 14757, 0), ('Kahn', 'W', 1, 0), ('LaRiva', 'W', 3, 0), ('Limbaugh', 'W', 3, 0), ('Locke', 'W', 1, 0), ('Maldonado', 'W', 1, 0), ('McMullin', 'W', 706, 0), ('Other', 'W', 1407, 0), ('PerryDarryl', 'W', 1, 0), ('Scott', 'W', 2, 0), ('Smith', 'W', 3, 0), ('Sood', 'W', 1, 0), ('Stein', 'GRE', 6103, 0), ('Stout', 'W', 1, 0), ('Trump', 'REP', 185127, 0), ('White', 'W', 2, 0)], 'NH': [('Biden', 'W', 55, 0), ('Bush', 'W', 230, 0), ('Carson', 'W', 83, 0), ('Christie', 'W', 23, 0), ('Clinton', 'DEM', 348526, 4), ('Cruz', 'W', 129, 0), ('DeLaFuente', 'ADP', 678, 0), ('Johnson', 'LIB', 30777, 0), ('Kasich', 'W', 1365, 0), ('McCain', 'W', 127, 0), ('McMullin', 'W', 1064, 0), ('Paul', 'W', 98, 0), ('Pence', 'W', 937, 0), ('Romney', 'W', 540, 0), ('Rubio', 'W', 136, 0), ('Ryan', 'W', 280, 0), ('Sanders', 'W', 4493, 0), ('Scattered', 'W', 2411, 0), ('Stein', 'GRE', 6496, 0), ('Supreme', 'W', 58, 0), ('Trump', 'REP', 345790, 0)], 'NM': [('Castle', 'CON', 1514, 0), ('Clinton', 'DEM', 385234, 5), ('DeLaFuente', 'ADP', 475, 0), ('Johnson', 'LIB', 74541, 0), ('LaRiva', 'PSL', 1184, 0), ('McMullin', 'BFA', 5825, 0), ('Stein', 'GRE', 9879, 0), ('Trump', 'REP', 319667, 0)], 'NV': [('Castle', 'IAP', 5268, 0), ('Clinton', 'DEM', 539260, 6), ('DeLaFuente', 'NPY', 2552, 0), ('Johnson', 'LIB', 37384, 0), ('NoneofTheseCandidates', 'W', 28863, 0), ('Trump', 'REP', 512058, 0)], 'CT': [('Basiago', 'W', 42, 0), ('Blumenthal', 'W', 12, 0), ('Buchanan', 'W', 19, 0), ('Castle', 'W', 147, 0), ('Clinton', 'DEM', 897572, 7), ('CooperJ', 'W', 57, 0), ('Cummings', 'W', 5, 0), ('DeLaFuente', 'W', 12, 0), ('Deame', 'W', 13, 0), ('Evans', 'W', 44, 0), ('Fox', 'W', 3, 0), ('Hoefling', 'W', 31, 0), ('Johnson', 'LIB', 48676, 0), ('Klojzy', 'W', 6, 0), ('Kotlikoff', 'W', 23, 0), ('LaRiva', 'W', 41, 0), ('Maldonado', 'W', 4, 0), ('McMullin', 'W', 2108, 0), ('Schoenke', 'W', 15, 0), ('Skewes', 'W', 4, 0), ('Smith', 'W', 12, 0), ('Stein', 'GRE', 22841, 0), ('Trump', 'REP', 673215, 0), ('Wu', 'W', 18, 0)], 'PA': [('Castle', 'CON', 21572, 0), ('Clinton', 'DEM', 2926441, 0), ('Johnson', 'LIB', 146715, 0), ('Kahn', 'W', 3, 0), ('Kasich', 'W', 302, 0), ('McMullin', 'W', 6472, 0), ('Sanders', 'W', 6060, 0), ('Scattered', 'W', 37239, 0), ('Stein', 'GRE', 49941, 0), ('Trump', 'REP', 2970733, 20)], 'KS': [('Basiago', 'W', 6, 0), ('Castle', 'W', 646, 0), ('Clinton', 'DEM', 427005, 0), ('DeLaFuente', 'W', 3, 0), ('Hedges', 'W', 3, 0), ('Hoefling', 'W', 45, 0), ('Johnson', 'LIB', 55406, 0), ('Kahn', 'W', 2, 0), ('LaRiva', 'W', 7, 0), ('Maturen', 'W', 214, 0), ('McMullin', 'W', 6520, 0), ('PerryDarryl', 'W', 1, 0), ('Schriner', 'W', 3, 0), ('Smith', 'W', 6, 0), ('Sood', 'W', 10, 0), ('Stein', 'IND', 23506, 0), ('Sterling', 'W', 1, 0), ('Trump', 'REP', 671018, 6)], 'CO': [('Atwood', 'APV', 337, 0), ('Castle', 'AMC', 11699, 0), ('Clinton', 'DEM', 1338870, 9), ('DeLaFuente', 'W', 1255, 0), ('Fox', 'W', 2, 0), ('Hedges', 'P', 185, 0), ('Hoefling', 'AMP', 710, 0), ('Johnson', 'LIB', 144121, 0), ('Keniston', 'VPA', 5028, 0), ('Kennedy', 'SWP', 452, 0), ('Kopitke', 'IAP', 1096, 0), ('Kotlikoff', 'KFP', 392, 0), ('LaRiva', 'SLP', 531, 0), ('Lohmiller', 'W', 3, 0), ('Lyttle', 'NRP', 382, 0), ('Maldonado', 'IPC', 872, 0), ('Maturen', 'ASP', 862, 0), ('McMullin', 'UN', 28917, 0), ('Nieman', 'W', 1, 0), ('PerryBrian', 'W', 4, 0), ('PerryDavid', 'W', 11, 0), ('Scott', 'UN', 749, 0), ('Silva', 'NTP', 751, 0), ('Smith', 'UN', 1819, 0), ('Soltysik', 'SOC', 271, 0), ('Stein', 'GRE', 38437, 0), ('Sterner', 'W', 6, 0), ('Trump', 'REP', 1202484, 0)], 'ND': [('Castle', 'CON', 1833, 0), ('Clinton', 'DNL', 93758, 0), ('DeLaFuente', 'ADP', 364, 0), ('Johnson', 'LIB', 21434, 0), ('Scattered', 'W', 6397, 0), ('Stein', 'GRE', 3780, 0), ('Trump', 'REP', 216794, 3)], 'UT': [('Baird', 'W', 9, 0), ('Basiago', 'W', 4, 0), ('Buchanan', 'W', 1, 0), ('Burton', 'W', 1, 0), ('Castle', 'CON', 8032, 0), ('Clinton', 'DEM', 310676, 0), ('DeLaFuente', 'UN', 883, 0), ('Giordani', 'IAP', 2752, 0), ('Hoefling', 'W', 6, 0), ('Johnson', 'LIB', 39608, 0), ('Kennedy', 'UN', 521, 0), ('Kotlikoff', 'W', 9, 0), ('McMullin', 'UN', 243690, 0), ('Moorehead', 'UN', 544, 0), ('Smith', 'W', 19, 0), ('Soltysik', 'W', 4, 0), ('Stein', 'UN', 9438, 0), ('Tittle', 'W', 1, 0), ('Trump', 'REP', 515231, 6), ('Valdivia', 'W', 1, 0)], 'IA': [('Castle', 'CON', 5335, 0), ('Clinton', 'DEM', 653669, 0), ('DeLaFuente', 'NP', 451, 0), ('Johnson', 'LIB', 59186, 0), ('Kahn', 'NPI', 2247, 0), ('LaRiva', 'PSL', 323, 0), ('McMullin', 'NP', 12366, 0), ('Scattered', 'W', 17746, 0), ('Stein', 'IG', 11479, 0), ('Trump', 'REP', 800983, 6), ('Vacek', 'LMN', 2246, 0)], 'NY': [('Asherie', 'W', 9, 0), ('Blickley', 'W', 2, 0), ('Buchanan', 'W', 58, 0), ('Canns', 'W', 5, 0), ('Carter', 'W', 18, 0), ('Castle', 'W', 955, 0), ('Clinton', 'DEM', 4556118, 29), ('CohenA', 'W', 33, 0), ('Connolly', 'W', 30, 0), ('DeLaFuente', 'W', 35, 0), ('Fried', 'W', 6, 0), ('Gyurko', 'W', 76, 0), ('Hartnell', 'W', 42, 0), ('Hoefling', 'W', 137, 0), ('Ingbar', 'W', 8, 0), ('Johnson', 'IDP', 176598, 0), ('Kahn', 'W', 72, 0), ('Keniston', 'W', 90, 0), ('LaRiva', 'W', 175, 0), ('Mackler', 'W', 15, 0), ('Maturen', 'W', 458, 0), ('McMullin', 'W', 10397, 0), ('Moorehead', 'W', 68, 0), ('Mutford', 'W', 85, 0), ('RobertsC', 'W', 88, 0), ('Scattered', 'W', 48343, 0), ('Schoenke', 'W', 3, 0), ('Scott', 'W', 3, 0), ('Soltysik', 'W', 36, 0), ('Stein', 'GRE', 107935, 0), ('Trump', 'REP', 2819533, 0), ('Valdivia', 'W', 4, 0), ('Welsh', 'W', 1, 0), ('Whitaker', 'W', 1, 0), ('Wolff', 'W', 5, 0)], 'AL': [('Clinton', 'DEM', 729547, 0), ('Johnson', 'IND', 44467, 0), ('Scattered', 'W', 21712, 0), ('Stein', 'IND', 9391, 0), ('Trump', 'REP', 1318255, 9)], 'VT': [('Belichek', 'W', 7, 0), ('Biden', 'W', 57, 0), ('Bloomberg', 'W', 22, 0), ('Brady', 'W', 9, 0), ('Bush', 'W', 79, 0), ('Carson', 'W', 61, 0), ('Castle', 'W', 63, 0), ('Clinton', 'DEM', 178573, 3), ('Cruz', 'W', 63, 0), ('DeLaFuente', 'IND', 1063, 0), ('Douglas', 'W', 75, 0), ('Epstein', 'W', 11, 0), ('Fiorina', 'W', 11, 0), ('Gabard', 'W', 17, 0), ('Huckabee', 'W', 11, 0), ('Johnson', 'LIB', 10078, 0), ('Kasich', 'W', 827, 0), ('Keniston', 'W', 3, 0), ('Kotlikoff', 'W', 3, 0), ('LaRiva', 'LBU', 327, 0), ('Leahy', 'W', 7, 0), ('Maturen', 'W', 14, 0), ('McCain', 'W', 76, 0), ('McMullin', 'W', 640, 0), ('Nader', 'W', 7, 0), ('NoName', 'W', 255, 0), ('ObamaB', 'W', 8, 0), ('ObamaM', 'W', 15, 0), ('Ortiz', 'W', 8, 0), ('Osborne', 'W', 2, 0), ('Pence', 'W', 298, 0), ('Powell', 'W', 25, 0), ('RandPaul', 'W', 26, 0), ('Rice', 'W', 18, 0), ('Romney', 'W', 120, 0), ('RonPaul', 'W', 25, 0), ('Rubio', 'W', 93, 0), ('Ryan', 'W', 208, 0), ('Sanders', 'W', 18218, 0), ('Scattered', 'W', 1478, 0), ('Smith', 'W', 1, 0), ('Soltysik', 'W', 2, 0), ('Stein', 'GRE', 6758, 0), ('Supreme', 'W', 10, 0), ('Trump', 'REP', 95369, 0), ('Tuttle', 'W', 6, 0), ('Warren', 'W', 13, 0), ('Weld', 'W', 5, 0), ('White', 'W', 2, 0)], 'TX': [('Castle', 'W', 4261, 0), ('Clinton', 'DEM', 3877868, 0), ('Cubbler', 'W', 314, 0), ('Fox', 'W', 45, 0), ('Hoefling', 'W', 932, 0), ('Johnson', 'LIB', 283492, 0), ('Kotlikoff', 'W', 1037, 0), ('Lee', 'W', 67, 0), ('Maturen', 'W', 1401, 0), ('McMullin', 'W', 42366, 0), ('Moorehead', 'W', 122, 0), ('Morrow', 'W', 145, 0), ('Soltysik', 'W', 72, 0), ('Steffes', 'W', 71, 0), ('Stein', 'GRE', 71558, 0), ('Trump', 'REP', 4685047, 36), ('Valdivia', 'W', 428, 0)], 'SC': [('Castle', 'CON', 5765, 0), ('Clinton', 'DEM', 855373, 0), ('Johnson', 'LIB', 49204, 0), ('McMullin', 'IDP', 21016, 0), ('Skewes', 'AM', 3246, 0), ('Stein', 'GRE', 13034, 0), ('Trump', 'REP', 1155389, 9)], 'ME': [('Castle', 'W', 333, 0), ('Clinton', 'DEM', 357735, 3), ('Fox', 'W', 7, 0), ('Johnson', 'LIB', 38105, 0), ('Kotlikoff', 'W', 16, 0), ('McMullin', 'W', 1887, 0), ('Stein', 'GI', 14251, 0), ('Trump', 'REP', 335593, 1)], 'HI': [('Castle', 'CON', 4508, 0), ('Clinton', 'DEM', 266891, 3), ('Johnson', 'LIB', 15954, 0), ('Stein', 'GRE', 12737, 0), ('Trump', 'REP', 128847, 0)], 'MN': [('Ball', 'W', 24, 0), ('Bartlett', 'W', 41, 0), ('Castle', 'CON', 9456, 0), ('Clinton', 'DFL', 1367716, 10), ('DeLaFuente', 'ADP', 1431, 0), ('Duncan', 'W', 1, 0), ('Gerhard', 'W', 1, 0), ('Hartnell', 'W', 2, 0), ('Hoefling', 'W', 28, 0), ('Johnson', 'LIB', 112972, 0), ('Keniston', 'W', 31, 0), ('Kennedy', 'SWP', 1672, 0), ('Koplitz', 'W', 2, 0), ('Kotlikoff', 'W', 17, 0), ('LaRiva', 'W', 12, 0), ('Lynch', 'W', 1, 0), ('Mallapadi', 'W', 2, 0), ('Maturen', 'W', 244, 0), ('McMullin', 'IDP', 53076, 0), ('Muffoletto', 'W', 29, 0), ('Payeur', 'W', 2, 0), ('Roberts', 'W', 1, 0), ('RobertsC', 'W', 15, 0), ('Robertson', 'W', 1, 0), ('Scattered', 'W', 26714, 0), ('Schriner', 'W', 4, 0), ('Schumacher', 'W', 1, 0), ('Sidner', 'W', 4, 0), ('Smith', 'W', 3, 0), ('Snell', 'W', 1, 0), ('Soltysik', 'W', 15, 0), ('Stein', 'GRE', 36985, 0), ('Trump', 'REP', 1322951, 0), ('Vacek', 'LMN', 11291, 0), ('Wettschreck', 'W', 4, 0), ('Wharton', 'W', 53, 0), ('White', 'W', 10, 0)], 'IN': [('BrownR', 'IND', 11, 0), ('Castle', 'W', 1937, 0), ('Clinton', 'DEM', 1033126, 0), ('DeLaFuente', 'W', 21, 0), ('Duncan', 'W', 25, 0), ('Fox', 'W', 1, 0), ('Hoefling', 'W', 269, 0), ('Jackson', 'W', 121, 0), ('Johnson', 'LIB', 133993, 0), ('Kelly', 'W', 44, 0), ('Kotlikoff', 'W', 49, 0), ('Maldonado', 'W', 7, 0), ('Mullis', 'W', 22, 0), ('Roberts', 'W', 148, 0), ('Soltysik', 'W', 57, 0), ('Stein', 'W', 7841, 0), ('Trump', 'REP', 1557286, 11)], 'DC': [('Clinton', 'DEM', 282830, 3), ('Johnson', 'LIB', 4906, 0), ('Scattered', 'W', 6551, 0), ('Stein', 'STG', 4258, 0), ('Trump', 'REP', 12723, 0)], 'AZ': [('Buchanan', 'W', 56, 0), ('Carter', 'DEM', 42, 0), ('Castle', 'W', 1058, 0), ('Clinton', 'DEM', 1161167, 0), ('Corsetti', 'W', 3, 0), ('DeLaFuente', 'W', 29, 0), ('Fox', 'W', 14, 0), ('Hartnell', 'W', 11, 0), ('Hoefling', 'W', 85, 0), ('In-Albon', 'W', 24, 0), ('Johnson', 'LIB', 106327, 0), ('Kotlikoff', 'W', 52, 0), ('Maldonado', 'W', 20, 0), ('McMullin', 'W', 17449, 0), ('Schoenke', 'W', 4, 0), ('Smith', 'W', 62, 0), ('Stein', 'GRE', 34345, 0), ('Steinacker', 'W', 4, 0), ('Tittle', 'W', 12, 0), ('Trump', 'REP', 1252401, 11)], 'OK': [('Clinton', 'DEM', 420375, 0), ('Johnson', 'LIB', 83481, 0), ('Trump', 'REP', 949136, 7)], 'KY': [('Castle', 'W', 438, 0), ('Clark', 'W', 2, 0), ('Clinton', 'DEM', 628854, 0), ('Cubbler', 'W', 6, 0), ('DeLaFuente', 'ADP', 1128, 0), ('Duncan', 'W', 2, 0), ('Ellis', 'W', 14, 0), ('Fox', 'W', 1, 0), ('Hartnell', 'W', 5, 0), ('Hoefling', 'W', 39, 0), ('Jackson', 'W', 18, 0), ('Johnson', 'LIB', 53752, 0), ('Keniston', 'W', 22, 0), ('Kotlikoff', 'W', 8, 0), ('Ling', 'W', 1, 0), ('Luesing', 'W', 6, 0), ('Maldonado', 'W', 2, 0), ('Maturen', 'W', 155, 0), ('McMullin', 'IND', 22780, 0), ('PerryDavid', 'W', 4, 0), ('Schoenke', 'W', 2, 0), ('Smith', 'W', 9, 0), ('Stein', 'GRE', 13913, 0), ('Stevens', 'W', 12, 0), ('Tittle', 'W', 1, 0), ('Trump', 'REP', 1202971, 8), ('White', 'W', 4, 0)], 'WI': [('Castle', 'CON', 12162, 0), ('Clinton', 'DEM', 1382536, 0), ('DeLaFuente', 'ADP', 1502, 0), ('Fox', 'W', 47, 0), ('Hoefling', 'W', 80, 0), ('Johnson', 'LIB', 106674, 0), ('Keniston', 'W', 67, 0), ('Kotlikoff', 'W', 15, 0), ('Maldonado', 'W', 4, 0), ('Maturen', 'W', 284, 0), ('McMullin', 'W', 11855, 0), ('Moorehead', 'WW', 1770, 0), ('Scattered', 'W', 22764, 0), ('Schoenke', 'W', 1, 0), ('Soltysik', 'W', 33, 0), ('Stein', 'WG', 31072, 0), ('Trump', 'REP', 1405284, 10)], 'MT': [('Basiago', 'W', 3, 0), ('Buchanan', 'W', 2, 0), ('Castle', 'W', 296, 0), ('Clinton', 'DEM', 177709, 0), ('DeLaFuente', 'ADP', 1570, 0), ('Hoefling', 'W', 10, 0), ('Johnson', 'LIB', 28037, 0), ('Kotlikoff', 'W', 7, 0), ('Maldonado', 'W', 1, 0), ('McMullin', 'W', 2297, 0), ('Morris', 'W', 1, 0), ('PerryDarryl', 'W', 1, 0), ('Schriner', 'W', 1, 0), ('Smith', 'W', 1, 0), ('Soltysik', 'W', 1, 0), ('Stein', 'GRE', 7970, 0), ('Trump', 'REP', 279240, 3)], 'WY': [('Castle', 'CON', 2042, 0), ('Clinton', 'DEM', 55973, 0), ('DeLaFuente', 'IND', 709, 0), ('Johnson', 'LIB', 13287, 0), ('Scattered', 'W', 6904, 0), ('Stein', 'IND', 2515, 0), ('Trump', 'REP', 174419, 3)], 'IL': [('Anderson', 'W', 61, 0), ('Breivogel', 'W', 12, 0), ('Brumfield', 'W', 5, 0), ('Castle', 'W', 1138, 0), ('Clinton', 'DEM', 3090729, 20), ('Fox', 'W', 3, 0), ('Harper', 'W', 1, 0), ('Hartnell', 'W', 6, 0), ('Hoefling', 'W', 175, 0), ('Johnson', 'LIB', 209596, 0), ('JohnsonN', 'W', 1, 0), ('Kotlikoff', 'W', 82, 0), ('Lee', 'W', 7, 0), ('Maldonado', 'W', 20, 0), ('McKee', 'W', 24, 0), ('McMullin', 'W', 11655, 0), ('Meluch', 'W', 3, 0), ('Morris', 'W', 10, 0), ('Roberts', 'W', 8, 0), ('Schoenke', 'W', 25, 0), ('Seeberg', 'W', 27, 0), ('SmithD', 'W', 4, 0), ('Stack', 'W', 10, 0), ('Stein', 'GRE', 76802, 0), ('Struck', 'W', 1, 0), ('Trump', 'REP', 2146015, 0), ('Tyree', 'W', 3, 0), ('Wysinger', 'W', 1, 0)], 'MD': [('Adams', 'W', 44, 0), ('Bolar', 'W', 7, 0), ('Boring', 'W', 53, 0), ('Bowhall', 'W', 7, 0), ('Boyles', 'W', 5, 0), ('Breivogel', 'W', 20, 0), ('BrownD', 'W', 15, 0), ('BrownT', 'W', 4, 0), ('Buchanan', 'W', 25, 0), ('Carlisle', 'W', 51, 0), ('Castle', 'W', 566, 0), ('Clinton', 'DEM', 1677928, 10), ('DeLaFuente', 'W', 14, 0), ('Duncan', 'W', 18, 0), ('Edgell', 'W', 1, 0), ('Flippin', 'W', 6, 0), ('Fox', 'W', 9, 0), ('Gates', 'W', 36, 0), ('Hartnell', 'W', 24, 0), ('Hedges', 'W', 5, 0), ('Hoefling', 'W', 42, 0), ('Jennings', 'W', 4, 0), ('Johnson', 'LIB', 79605, 0), ('Kahn', 'W', 18, 0), ('Keita', 'W', 2, 0), ('Kotlikoff', 'W', 73, 0), ('LaRiva', 'W', 48, 0), ('Locke', 'W', 10, 0), ('Maldonado', 'W', 12, 0), ('Maturen', 'W', 504, 0), ('McCarthy', 'W', 97, 0), ('McMullin', 'W', 9630, 0), ('Other', 'W', 33263, 0), ('Pendleton', 'W', 17, 0), ('Puskar', 'W', 7, 0), ('Reid', 'W', 53, 0), ('Schoenke', 'W', 3, 0), ('Schriner', 'W', 9, 0), ('Smith', 'W', 13, 0), ('SmithC', 'W', 11, 0), ('Soldjah', 'W', 13, 0), ('Soltysik', 'W', 6, 0), ('Stein', 'GRE', 35945, 0), ('Symonette', 'W', 10, 0), ('Terry', 'W', 1, 0), ('Thomas', 'W', 16, 0), ('Trump', 'REP', 943169, 0), ('Vakil', 'W', 1, 0), ('Valdivia', 'W', 11, 0), ('Vogel-Walcutt', 'W', 2, 0), ('White', 'W', 11, 0), ('Williams', 'W', 1, 0), ('Wysinger', 'W', 1, 0)], 'ID': [('Castle', 'IND', 4403, 0), ('Clinton', 'DEM', 189765, 0), ('Copeland', 'CON', 2356, 0), ('DeLaFuente', 'IND', 1373, 0), ('Johnson', 'LIB', 28331, 0), ('McMullin', 'IND', 46476, 0), ('Stein', 'IND', 8496, 0), ('Trump', 'REP', 409055, 4)], 'OR': [('Clinton', 'DEM', 1002106, 7), ('Johnson', 'LIB', 94231, 0), ('Miscellaneous', 'W', 72594, 0), ('Stein', 'PG/PRO', 50002, 0), ('Trump', 'REP', 782403, 0)], 'MO': [('Castle', 'CON', 13092, 0), ('Clinton', 'DEM', 1071068, 0), ('DeLaFuente', 'W', 6, 0), ('Hoefling', 'W', 48, 0), ('Johnson', 'LIB', 97359, 0), ('Kotlikoff', 'W', 28, 0), ('McMullin', 'W', 7071, 0), ('Schoenke', 'W', 3, 0), ('Stein', 'GRE', 25419, 0), ('Trump', 'REP', 1594511, 10)], 'VA': [('AllOthers', 'W', 33749, 0), ('Clinton', 'DEM', 1981473, 13), ('Johnson', 'LIB', 118274, 0), ('McMullin', 'IND', 54054, 0), ('Stein', 'GRE', 27638, 0), ('Trump', 'REP', 1769443, 0)], 'TN': [('Castle', 'W', 1584, 0), ('Clinton', 'DEM', 870695, 0), ('DeLaFuente', 'IND', 4075, 0), ('Fox', 'W', 6, 0), ('Hoefling', 'W', 132, 0), ('Johnson', 'IND', 70397, 0), ('Kennedy', 'IND', 2877, 0), ('Kotlikoff', 'W', 20, 0), ('Limbaugh', 'W', 53, 0), ('McMullin', 'W', 11991, 0), ('Schoenke', 'W', 3, 0), ('Smith', 'IND', 7276, 0), ('Stein', 'IND', 15993, 0), ('Trump', 'REP', 1522925, 11)], 'MI': [('Castle', 'UST', 16139, 0), ('Clinton', 'DEM', 2268839, 0), ('Fox', 'W', 10, 0), ('Hartnell', 'W', 39, 0), ('Hoefling', 'W', 95, 0), ('Johnson', 'LIB', 172136, 0), ('Kotlikoff', 'W', 87, 0), ('Maturen', 'W', 517, 0), ('McMullin', 'W', 8177, 0), ('Moorehead', 'W', 30, 0), ('Soltysik', 'NLP', 2209, 0), ('Stein', 'GRE', 51463, 0), ('Trump', 'REP', 2279543, 16)], 'AK': [('Castle', 'CON', 3866, 0), ('Clinton', 'DEM', 116454, 0), ('DeLaFuente', 'NAF', 1240, 0), ('Johnson', 'LIB', 18725, 0), ('Scattered', 'W', 9201, 0), ('Stein', 'GRE', 5735, 0), ('Trump', 'REP', 163387, 3)], 'NE': [('Clinton', 'DEM', 284494, 0), ('Johnson', 'LIB', 38946, 0), ('Scattered', 'W', 16051, 0), ('Stein', 'BP', 8775, 0), ('Trump', 'REP', 495961, 5)], 'WA': [('Castle', 'CON', 17623, 0), ('Clinton', 'DEM', 1742718, 8), ('Johnson', 'LIB', 160879, 0), ('Kennedy', 'SWP', 4307, 0), ('LaRiva', 'SLP', 3523, 0), ('Scattered', 'W', 107805, 0), ('Stein', 'GRE', 58417, 0), ('Trump', 'REP', 1221747, 0)], 'LA': [('Castle', 'CON', 3129, 0), ('Clinton', 'DEM', 780154, 0), ('Hoefling', 'LFC', 1581, 0), ('Jacob', 'LTC', 749, 0), ('Johnson', 'LIB', 37978, 0), ('Keniston', 'VP', 1881, 0), ('Kennedy', 'SWP', 480, 0), ('Kotlikoff', 'IOC', 1048, 0), ('LaRiva', 'SLP', 446, 0), ('McMullin', 'CCS', 8547, 0), ('Stein', 'GRE', 14031, 0), ('Trump', 'REP', 1178638, 8), ('White', 'SEA', 370, 0)]}

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

	# read_votes tests	     
	def test_read_votes_1  (self):self.assertNotEqual(read_votes('votes.csv'), False)
	def test_read_votes_2  (self):self.assertEqual(read_votes('votes.csv'),getDict())
	def test_read_votes_3  (self):self.assertEqual(read_votes('votes.csv')['VA'][2],('Johnson', 'LIB', 118274, 0))
	def test_read_votes_4  (self):self.assertEqual(read_votes('votes.csv')['TX'][-1],('Valdivia', 'W', 428, 0))
	def test_read_votes_5  (self):self.assertEqual(read_votes('votes.csv')['DC'],[('Clinton', 'DEM', 282830, 3),('Johnson', 'LIB', 4906, 0),('Scattered', 'W', 6551, 0),('Stein', 'STG', 4258, 0),('Trump', 'REP', 12723, 0)])
	def test_read_votes_6  (self):self.assertEqual(len(read_votes('votes.csv')['RI']),75)
	def test_read_votes_7  (self):self.assertEqual(len(read_votes('votes.csv')['WY']),7)
	def test_read_votes_8  (self):self.assertEqual(len(read_votes('votes.csv')['DC']),5)
	def test_read_votes_9  (self):self.assertEqual(len(read_votes('votes.csv')),51)
	def test_read_votes_10 (self):
		db = read_votes('votes.csv')
		self.assertNotIn('state', db)

	# read_abbreviations tests	
	def test_read_abbreviations_1  (self): self.assertNotEqual(read_abbreviations('abbreviations.csv'), False)
	def test_read_abbreviations_2  (self): self.assertEqual(len(read_abbreviations('abbreviations.csv')), 401)
	def test_read_abbreviations_3  (self): self.assertEqual(read_abbreviations('abbreviations.csv')['WEP'], 'Women\'s Equality Party')
	def test_read_abbreviations_4  (self): self.assertEqual(read_abbreviations('abbreviations.csv')['RNN'], 'Representing the 99%')
	def test_read_abbreviations_5  (self): self.assertEqual(read_abbreviations('abbreviations.csv')['WF'], 'Working Families')
	def test_read_abbreviations_6  (self): self.assertEqual(len(read_abbreviations('abbreviations.csv')['Moorehead']), 17)
	def test_read_abbreviations_7  (self):
		db = read_abbreviations('abbreviations.csv')
		self.assertNotIn('abbreviation', db)
	def test_read_abbreviations_8  (self):
		db = read_abbreviations('abbreviations.csv')
		self.assertNotEqual(db['DEM'], 'Democratic ')
     

	# write_votes tests	
	def test_write_votes_1  (self):
		self.assertTrue(write_votes(getDict(), '__votes_copy.csv'))
	def test_write_votes_2  (self):
		write_votes(getDict(), '__votes_copy.csv')
		self.assertEqual(len(read_votes('__votes_copy.csv')), 51)
	def test_write_votes_3  (self):
		write_votes(getDict(), '__votes_copy.csv')
		self.assertEqual(len(read_votes('__votes_copy.csv')['MD']), 53)
	def test_write_votes_4  (self):
		write_votes(getDict(), '__votes_copy.csv')
		self.assertEqual(read_votes('__votes_copy.csv')['SD'], [('Castle', 'CON', 4064, 0), ('Clinton', 'DEM', 117458, 0), ('Johnson', 'LIB', 20850, 0), ('Trump', 'REP', 227721, 3)])
	def test_write_votes_5  (self):
		write_votes(getDict(), '__votes_copy.csv')
		self.assertEqual(read_votes('__votes_copy.csv')['HI'], [('Castle', 'CON', 4508, 0), ('Clinton', 'DEM', 266891, 3), ('Johnson', 'LIB', 15954, 0), ('Stein', 'GRE', 12737, 0), ('Trump', 'REP', 128847, 0)])
	def test_write_votes_6  (self):
		write_votes(getDict(), '__votes_copy.csv')
		self.assertEqual(read_votes('__votes_copy.csv')['WY'], [('Castle', 'CON', 2042, 0), ('Clinton', 'DEM', 55973, 0), ('DeLaFuente', 'IND', 709, 0), ('Johnson', 'LIB', 13287, 0), ('Scattered', 'W', 6904, 0), ('Stein', 'IND', 2515, 0), ('Trump', 'REP', 174419, 3)])

	# add_candidate tests	
	def test_add_candidate_1  (self):
		db = getDict()
		add_candidate(db, 'PR', 'Socrates', 'IND', 100, 0)
		self.assertEqual(db['PR'], [('Socrates', 'IND', 100, 0)])
	def test_add_candidate_2  (self):
		db = getDict()
		add_candidate(db, 'VR', 'Trump', 'R', 1234, 10)
		add_candidate(db, 'VR', 'Clinton', 'D', 1234, 10)
		self.assertEqual(db['VR'], [('Clinton', 'D', 1234, 10), ('Trump', 'R', 1234, 10)])
	def test_add_candidate_3  (self):
		db = getDict()
		add_candidate(db, 'VA', 'Castle', 'W', 100, 0)
		self.assertEqual(db['VA'], [('AllOthers', 'W', 33749, 0), ('Castle', 'W', 100, 0), ('Clinton', 'DEM', 1981473, 13), ('Johnson', 'LIB', 118274, 0), ('McMullin', 'IND', 54054, 0), ('Stein', 'GRE', 27638, 0), ('Trump', 'REP', 1769443, 0)])
	def test_add_candidate_4  (self):
		db = getDict()
		add_candidate(db, 'AL', 'Castle', 'W', 100, 0)
		self.assertEqual(db['AL'], [('Castle', 'W', 100, 0), ('Clinton', 'DEM', 729547, 0), ('Johnson', 'IND', 44467, 0), ('Scattered', 'W', 21712, 0), ('Stein', 'IND', 9391, 0), ('Trump', 'REP', 1318255, 9)])
	def test_add_candidate_5  (self):
		db = getDict()
		add_candidate(db, 'AL', 'White', 'W', 4321, 5)
		self.assertEqual(db['AL'], [('Clinton', 'DEM', 729547, 0), ('Johnson', 'IND', 44467, 0), ('Scattered', 'W', 21712, 0), ('Stein', 'IND', 9391, 0), ('Trump', 'REP', 1318255, 9), ('White', 'W', 4321, 5)])
	def test_add_candidate_6  (self):
		db = getDict()
		add_candidate(db, 'AL', 'White', 'W', 4321, 5)
		add_candidate(db, 'AL', 'White', 'W', 3210, 4)
		add_candidate(db, 'AL', 'White', 'W', 2104, 3)
		self.assertEqual(db['AL'], [('Clinton', 'DEM', 729547, 0), ('Johnson', 'IND', 44467, 0), ('Scattered', 'W', 21712, 0), ('Stein', 'IND', 9391, 0), ('Trump', 'REP', 1318255, 9), ('White', 'W', 2104, 3)])
	def test_add_candidate_7  (self):
		db = getDict()
		add_candidate(db, 'DC', 'Clinton', 'DEM', 111111, 3)
		self.assertEqual(db['DC'], [('Clinton', 'DEM', 111111, 3), ('Johnson', 'LIB', 4906, 0), ('Scattered', 'W', 6551, 0), ('Stein', 'STG', 4258, 0), ('Trump', 'REP', 12723, 0)])
	def test_add_candidate_8  (self):
		db = getDict()
		add_candidate(db, 'DC', 'Clinton', 'DEM', 111111, 0)
		add_candidate(db, 'DC', 'Trump', 'REP', 222222, 3)
		self.assertEqual(db['DC'], [('Clinton', 'DEM', 111111, 0), ('Johnson', 'LIB', 4906, 0), ('Scattered', 'W', 6551, 0), ('Stein', 'STG', 4258, 0), ('Trump', 'REP', 222222, 3)])
	def test_add_candidate_9  (self):
		db = getDict()
		add_candidate(db, 'DC', 'Johnson', 'LIB', 4906, 0)
		add_candidate(db, 'DC', 'Stein', 'W', 4906, 3)
		self.assertEqual(db['DC'], [('Clinton', 'DEM', 282830, 3), ('Johnson', 'LIB', 4906, 0), ('Scattered', 'W', 6551, 0), ('Stein', 'W', 4906, 3), ('Trump', 'REP', 12723, 0)])

	# remove_candidate tests	
	def test_remove_candidate_1  (self):
		db = getDict()
		self.assertEqual(remove_candidate(db, 'Johnson', 'VR'), False)
	def test_remove_candidate_2  (self):
		db = getDict()
		remove_candidate(db, 'Stein', 'OK')
		self.assertEqual(db['OK'], [('Clinton', 'DEM', 420375, 0), ('Johnson', 'LIB', 83481, 0), ('Trump', 'REP', 949136, 7)])
	def test_remove_candidate_3  (self):
		db = getDict()
		remove_candidate(db, 'Johnson', 'OK')
		self.assertEqual(db['OK'], [('Clinton', 'DEM', 420375, 0), ('Trump', 'REP', 949136, 7)])
	def test_remove_candidate_4  (self):
		db = getDict()
		remove_candidate(db, 'Clinton', 'OK')
		self.assertEqual(db['OK'], [('Johnson', 'LIB', 83481, 0), ('Trump', 'REP', 949136, 7)])
	def test_remove_candidate_5  (self):
		db = getDict()
		remove_candidate(db, 'Clinton', 'OK')
		remove_candidate(db, 'Johnson', 'OK')
		remove_candidate(db, 'Trump', 'OK')
		self.assertNotIn('OK', db)
	def test_remove_candidate_6  (self):
		db = getDict()
		remove_candidate(db, 'Clinton')
		self.assertEqual(db['OK'], [('Johnson', 'LIB', 83481, 0), ('Trump', 'REP', 949136, 7)])
	def test_remove_candidate_7  (self):
		db = getDict()
		remove_candidate(db, 'Trump')
		self.assertEqual(db['OK'], [('Clinton', 'DEM', 420375, 0), ('Johnson', 'LIB', 83481, 0)])
	def test_remove_candidate_8  (self):
		db = getDict()
		remove_candidate(db, 'Trump')
		remove_candidate(db, 'Clinton')
		self.assertEqual(db['DC'], [('Johnson', 'LIB', 4906, 0), ('Scattered', 'W', 6551, 0), ('Stein', 'STG', 4258, 0)])
	def test_remove_candidate_9  (self):
		db = getDict()
		remove_candidate(db, 'Trump')
		remove_candidate(db, 'Clinton')
		remove_candidate(db, 'Johnson')
		self.assertNotIn('OK', db)

	# merge_votes tests	
	def test_merge_votes_1  (self):
		db = getDict()
		merge_votes(db,'Clinton', 'Trump', 'top2', 'REP_DEM', 'DC')
		self.assertEqual(db['DC'], [('Johnson', 'LIB', 4906, 0), ('Scattered', 'W', 6551, 0), ('Stein', 'STG', 4258, 0), ('top2', 'REP_DEM', 295553, 3)])
	def test_merge_votes_2  (self):
		db = getDict()
		merge_votes(db,'Clinton', 'Trump', 'top2', 'REP_DEM', 'ME')
		self.assertEqual(db['ME'], [('Castle', 'W', 333, 0), ('Fox', 'W', 7, 0), ('Johnson', 'LIB', 38105, 0), ('Kotlikoff', 'W', 16, 0), ('McMullin', 'W', 1887, 0), ('Stein', 'GI', 14251, 0), ('top2', 'REP_DEM', 693328, 4)])
	def test_merge_votes_3  (self):
		db = getDict()
		merge_votes(db,'Trump', 'Pence', 'TrumpPence', 'REP', 'WY')
		self.assertEqual(db['WY'], [('Castle', 'CON', 2042, 0), ('Clinton', 'DEM', 55973, 0), ('DeLaFuente', 'IND', 709, 0), ('Johnson', 'LIB', 13287, 0), ('Scattered', 'W', 6904, 0), ('Stein', 'IND', 2515, 0), ('TrumpPence', 'REP', 174419, 3)])
	def test_merge_votes_4  (self):
		db = getDict()
		merge_votes(db,'Trump', 'Pence', 'TrumpPence', 'REP', 'WY')
		self.assertEqual(db['SD'], [('Castle', 'CON', 4064, 0), ('Clinton', 'DEM', 117458, 0), ('Johnson', 'LIB', 20850, 0), ('Trump', 'REP', 227721, 3)])
	def test_merge_votes_5  (self):
		db = getDict()
		merge_votes(db,'Castle', 'Clinton', 'CC', 'CONDEM', 'SD')
		merge_votes(db,'Johnson', 'Trump', 'JT', 'LIBREP', 'SD')
		merge_votes(db,'CC', 'JT', 'CCJT', 'CONDEMLIBREP', 'SD')
		self.assertEqual(db['SD'], [('CCJT', 'CONDEMLIBREP', 370093, 3)])
	def test_merge_votes_6  (self):
		db = getDict()
		merge_votes(db,'Clinton', 'Trump', 'top2', 'REP_DEM')
		self.assertEqual(db['OK'], [('Johnson', 'LIB', 83481, 0), ('top2', 'REP_DEM', 1369511, 7)])
	def test_merge_votes_7  (self):
		db = getDict()
		merge_votes(db,'Donald', 'Duck', 'Walt', 'Disney')
		self.assertEqual(db['DC'], [('Clinton', 'DEM', 282830, 3), ('Johnson', 'LIB', 4906, 0), ('Scattered', 'W', 6551, 0), ('Stein', 'STG', 4258, 0), ('Trump', 'REP', 12723, 0)])
	def test_merge_votes_8  (self):
		db = getDict()
		merge_votes(db,'Scattered', 'Other', 'VARIOUS', 'W')
		self.assertEqual(db['NC'], [('Clinton', 'DEM', 2189316, 0), ('Johnson', 'LIB', 130126, 0), ('Stein', 'W', 12105, 0), ('Trump', 'REP', 2362631, 15), ('VARIOUS', 'W', 47386, 0)])

	# incorporate_precinct tests	
	def test_incorporate_precinct_1  (self):
		db = getDict()
		self.assertEqual(incorporate_precinct(db,'Socrates', 'VA', 100), False)
	def test_incorporate_precinct_2  (self):
		db = getDict()
		self.assertEqual(incorporate_precinct(db,'Clinton', 'VR', 100), False)
	def test_incorporate_precinct_3  (self):
		db = getDict()
		self.assertIsNone(incorporate_precinct(db,'Clinton', 'VA', 100))
	def test_incorporate_precinct_4  (self):
		db = getDict()
		incorporate_precinct(db,'McMullin', 'VA', 10000)
		self.assertEqual(db['VA'][3],('McMullin', 'IND', 64054, 0))
	def test_incorporate_precinct_5  (self):
		db = getDict()
		incorporate_precinct(db,'McMullin', 'VA', 10000)
		self.assertEqual(db['VT'][23],('McMullin', 'W', 640, 0))
	def test_incorporate_precinct_6  (self):
		db = getDict()
		incorporate_precinct(db,'McMullin', 'VA', 10000)
		incorporate_precinct(db,'McMullin', 'VA', -10000)
		self.assertEqual(db['VA'][3],('McMullin', 'IND', 54054, 0))
	def test_incorporate_precinct_7  (self):
		db = getDict()
		incorporate_precinct(db,'McMullin', 'VA', -100000)
		self.assertEqual(db['VA'],[('AllOthers', 'W', 33749, 0), ('Clinton', 'DEM', 1981473, 13), ('Johnson', 'LIB', 118274, 0), ('Stein', 'GRE', 27638, 0), ('Trump', 'REP', 1769443, 0)])
	def test_incorporate_precinct_8  (self):
		db = getDict()
		incorporate_precinct(db,'AllOthers', 'VA', -33749)
		incorporate_precinct(db,'McMullin', 'VA', -54054)
		incorporate_precinct(db,'Clinton', 'VA', -1981473)
		incorporate_precinct(db,'Johnson', 'VA', -118274)
		incorporate_precinct(db,'Stein', 'VA', -27638)
		incorporate_precinct(db,'Trump', 'VA', -1769443)
		self.assertNotIn('VA',db)

	# number_of_votes tests	
	def test_number_of_votes_1  (self):
		db = getDict()
		self.assertEqual(number_of_votes(db,'Trump', 'Electoral', 'tally', 'RI'), False)
	def test_number_of_votes_2  (self):
		db = getDict()
		self.assertEqual(number_of_votes(db,'Trump', 'electoral', 'Tally'), False)
	def test_number_of_votes_3  (self):
		db = getDict()
		self.assertEqual(number_of_votes(db,'White', 'popular', 'tally', 'VA'), False)
	def test_number_of_votes_4  (self):
		db = getDict()
		self.assertEqual(number_of_votes(db,'Clinton', 'popular', 'tally', 'PR'), False)
	def test_number_of_votes_5  (self):
		db = getDict()
		self.assertEqual(number_of_votes(db,'Clinton', 'popular', 'tally'), 65853514)
	def test_number_of_votes_6  (self):
		db = getDict()
		self.assertEqual(number_of_votes(db,'Trump', 'popular', 'tally'), 62984828)
	def test_number_of_votes_7  (self):
		db = getDict()
		self.assertEqual(number_of_votes(db,'Clinton', 'popular', 'percent'), 48.18)
	def test_number_of_votes_8  (self):
		db = getDict()
		self.assertEqual(number_of_votes(db,'Trump', 'popular', 'percent'), 46.09)
	def test_number_of_votes_9  (self):
		db = getDict()
		self.assertEqual(number_of_votes(db,'Trump', 'electoral', 'percent'), 57.25)
	def test_number_of_votes_10 (self):
		db = getDict()
		self.assertEqual(number_of_votes(db,'Clinton', 'electoral', 'percent', 'ME'), 75.00)
	def test_number_of_votes_11  (self):
		db = getDict()
		self.assertEqual(number_of_votes(db,'McMullin', 'popular', 'percent', 'VA'), 1.36)
	def test_number_of_votes_12  (self):
		db = getDict()
		self.assertEqual(number_of_votes(db,'Johnson', 'popular', 'percent', 'VA'), 2.97)

	# popular_votes_performance tests	
	def test_popular_votes_performance_1  (self):
		db = getDict()
		self.assertEqual(popular_votes_performance(db,'Clinton', 'tally', 'average'), False)
	def test_popular_votes_performance_2  (self):
		db = getDict()
		self.assertEqual(popular_votes_performance(db,'Socrates', 'percent', 'min'), False)
	def test_popular_votes_performance_3  (self):
		db = getDict()
		self.assertEqual(popular_votes_performance(db,'Clinton', 'percent'), 'District of Columbia')
	def test_popular_votes_performance_4  (self):
		db = getDict()
		self.assertEqual(popular_votes_performance(db,'Clinton', 'tally', 'min'), 'Wyoming')
	def test_popular_votes_performance_5  (self):
		db = getDict()
		self.assertEqual(popular_votes_performance(db,'Trump', 'percent', 'max'), 'West Virginia')
	def test_popular_votes_performance_6  (self):
		db = getDict()
		self.assertEqual(popular_votes_performance(db,'Trump', 'tally', 'min'), 'District of Columbia')
	def test_popular_votes_performance_7  (self):
		db = getDict()
		self.assertEqual(popular_votes_performance(db,'Johnson', 'percent'), 'New Mexico')
	def test_popular_votes_performance_8  (self):
		db = getDict()
		self.assertEqual(popular_votes_performance(db,'Stein', 'percent', 'max'), 'Hawaii')
	def test_popular_votes_performance_9  (self):
		db = getDict()
		self.assertEqual(popular_votes_performance(db,'McMullin', 'percent'), 'Utah')

	# candidates_difference tests	
	def test_candidates_difference_1  (self):
		db = getDict()
		self.assertEqual(candidates_difference(db,'McMullin', 'Trump', 'best'), False)
	def test_candidates_difference_2  (self):
		db = getDict()
		self.assertEqual(candidates_difference(db,'McMullin', 'trump'), False)
	def test_candidates_difference_3  (self):
		db = getDict()
		self.assertEqual(candidates_difference(db,'Clinton', 'Trump','largest'), 'District of Columbia')
	def test_candidates_difference_4  (self):
		db = getDict()
		self.assertEqual(candidates_difference(db,'Trump', 'Clinton','smallest'), 'Michigan')
	def test_candidates_difference_5  (self):
		db = getDict()
		self.assertEqual(candidates_difference(db,'Johnson', 'Clinton','smallest'), 'Wyoming')
	def test_candidates_difference_6  (self):
		db = getDict()
		self.assertEqual(candidates_difference(db,'Stein', 'Trump','smallest'), 'District of Columbia')

	# combined tests
	def test_combined_1  (self):
		db = getDict()
		add_candidate(db, 'SD', 'Socrates', 'IND', 100, 0)
		write_votes(db, '__votes_copy.csv')
		self.assertEqual(read_votes('__votes_copy.csv')['SD'], [('Castle', 'CON', 4064, 0), ('Clinton', 'DEM', 117458, 0), ('Johnson', 'LIB', 20850, 0), ('Socrates', 'IND', 100, 0), ('Trump', 'REP', 227721, 3)])
	def test_combined_2  (self):
		db = getDict()
		remove_candidate(db, 'Clinton')
		write_votes(db, '__votes_copy.csv')
		self.assertEqual(read_votes('__votes_copy.csv')['OK'], [('Johnson', 'LIB', 83481, 0), ('Trump', 'REP', 949136, 7)])
	def test_combined_3  (self):
		db = getDict()
		merge_votes(db,'Clinton', 'Trump', 'top2', 'REP_DEM')
		write_votes(db, '__votes_copy.csv')
		self.assertEqual(read_votes('__votes_copy.csv')['ME'], [('Castle', 'W', 333, 0), ('Fox', 'W', 7, 0), ('Johnson', 'LIB', 38105, 0), ('Kotlikoff', 'W', 16, 0), ('McMullin', 'W', 1887, 0), ('Stein', 'GI', 14251, 0), ('top2', 'REP_DEM', 693328, 4)])
	def test_combined_4  (self):
		db = getDict()
		merge_votes(db,'Scattered', 'Clinton', 'SC', 'SC')
		merge_votes(db,'Trump', 'Johnson', 'TJ', 'TJ')
		merge_votes(db,'SC', 'TJ', 'SCTJ', 'SCTJ')
		merge_votes(db,'SCTJ', 'Stein', 'SCTJS', 'SCTJS')
		remove_candidate(db, 'SCTJS')
		self.assertNotIn('NC', db)
	def test_combined_5  (self):
		db = getDict()
		incorporate_precinct(db,'AllOthers', 'VA', -33749)
		merge_votes(db,'McMullin', 'Clinton', 'MC', '_', 'VA')
		incorporate_precinct(db,'MC', 'VA', -3000000)
		merge_votes(db,'Johnson', 'Stein', 'JS', '_', 'VA')
		incorporate_precinct(db,'JS', 'VA', -200000)
		incorporate_precinct(db,'Trump', 'VA', -1769442)
		self.assertEqual(db['VA'],[('Trump', 'REP', 1, 0)])

	# extra credit:
	def test_extra_credit_reverse_result_1 (self):
		db = getDict()
		self.assertEqual(reverse_result(db, 'Trump'), False)
	def test_extra_credit_reverse_result_2 (self):
		db = getDict()
		self.assertEqual(reverse_result(db, 'Clinton'), ['Michigan', 'Pennsylvania', 'Wisconsin'])
	def test_extra_credit_reverse_result_3 (self):
		db = getDict()
		self.assertEqual(reverse_result(db, 'Johnson'), ['Maine', 'Utah', 'Wisconsin', 'Michigan', 'Arizona', 'Alaska', 'Pennsylvania', 'Florida', 'North Carolina', 'Iowa', 'Georgia', 'Ohio', 'Texas', 'Montana', 'Kansas', 'Indiana', 'South Carolina', 'Missouri', 'Nebraska', 'Idaho', 'South Dakota', 'Louisiana', 'North Dakota', 'Mississippi', 'Tennessee', 'Arkansas'])
	def test_extra_credit_reverse_result_4 (self):
		db = getDict()
		self.assertEqual(reverse_result(db, 'Stein'), ['Maine', 'Utah', 'Wisconsin', 'Michigan', 'Arizona', 'Pennsylvania', 'Florida', 'Alaska', 'North Carolina', 'Iowa', 'Georgia', 'Ohio', 'Texas', 'South Carolina', 'Montana', 'Kansas', 'Missouri', 'Indiana', 'Louisiana', 'Mississippi', 'Nebraska', 'Idaho', 'Arkansas', 'Tennessee', 'Alabama'])
	def test_extra_credit_reverse_result_5 (self):
		db = getDict()
		self.assertEqual(reverse_result(db, 'Socrates'), False)
	
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
		
#		print("TTS ====> ",list(map(lambda f: (f,id(f)),fs)))
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
		
#			print("TTS ====> ",list(map(lambda f: (f,id(f)),fs)))
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
#		print(dirpath,dirnames,filez)
		if dirpath==".":
			continue
		for file in filez:
			if file==this_file:
				continue
			filenames.append(os.path.join(dirpath,file))
#		print(dirpath,dirnames,filez,"\n")
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
			for fn in REQUIRED_DEFNS+EXTRA_CREDIT_DEFNS	:
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
		
# 			try:
# 				print("\n |||||||||| scrupe: "+str(scruples))
# 			except Exception as e:
# 				print("NO SCRUPE.",e)
# 			scruples = None
		
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
# 			print("\n\n\nbegin attempt:")
			while True:
				try:
					f = open("student.py","a")
					f.close()
					break
				except:
					pass
# 			print ("\n\nSUCCESS!")
				
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
			return((filename+"_IMPORT_ERROR_TRY_AGAIN	",0,1))	
		except Exception as e:
			print("Exception in loading"+filename+":\n"+str(e))
			print("Run your file without the tester to see the details")
			return(filename+str(e.__reduce__()[0]),0,1)
	
	# make a global for each expected definition.
	for fn in REQUIRED_DEFNS+EXTRA_CREDIT_DEFNS	:
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