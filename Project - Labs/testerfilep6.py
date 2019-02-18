# Based on testing harness dated 2017-06-02.

# STUDENTS: TO USE:
# 
# The following command will test all test cases on your file:
#   
#   MAC:
#   python3 <thisfile.py> <your_one_file.py>
# 
#   PC:
#   python <thisfile.py> <your_one_file.py>
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
	
REQUIRED_DEFNS = [	"Line",
					"Call",
					"PlanType",
					"PhonePlan",
					"CallError",
					"PhonePlanError"
				 ]

# for method names in classes that will be tested. They have to be here
# so that we don't complain about missing global function definitions.
# Really, any chosen name for test batches can go here regardless of actual
# method names in the code.
SUB_DEFNS = [	"activate_all",
				"deactivate_all",
				"add_call",
				"make_call",
				"add_calls",
				"mins_by_line",
				"calls_by_line",
				"remove_call",
				"add_line",
				"remove_line",
				"calculate_bill",
				"pay_bill"
			]

# definitions that are used for extra credit
EXTRA_CREDIT_DEFNS = [ ]

# how many points are test cases worth?
weight_required     = 1
weight_extra_credit = 1

# don't count extra credit; usually 100% if this is graded entirely by tests.
# it's up to you the instructor to do the math and add this up!
# TODO: auto-calculate this based on all possible tests.
total_points_from_tests = 100

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



import inspect # for enforcing usage of an operator or function
import ast     # for enforcing usage of an operator or function

# checks if a call to the function is present in the code. Of course it 
# might not actually be used in their solution...
def enforce_func_usage(func, funcname):
	dumptext = ast.dump(ast.parse(inspect.getsource(func).strip()))
	batches = dumptext.split("value=Call")
	for batch in batches:
		parts = batch.split("attr=")
		for part in parts:
			if part.startswith("'"+funcname+"'"):
				return
	raise Exception("You're required to call "+funcname+" in your solution.")


# END SPECIALIZATION SECTION

################################################################################
################################################################################
################################################################################


# enter batch mode by giving a directory to work on as the only argument.
BATCH_MODE = len(sys.argv)==2 and (sys.argv[1] in ["."] or os.path.isdir(sys.argv[1]))

# This class contains multiple "unit tests" that each check
# various inputs to specific functions, checking that we get
# the correct behavior (output value) from completing the call.
class AllTests (unittest.TestCase):
		
    ############################################################################
	
	def test_Line_1(self):
		"""Line init"""
		l = Line("GMU",703,9931000,False)
		self.assertEqual(l.name, "GMU")
		self.assertEqual(l.area_code, 703)
		self.assertEqual(l.number, 9931000)
		self.assertEqual(l.is_active, False)
		
	def test_Line_2(self):
		"""Line init, default parameter"""
		l = Line("GMU",703,9931000)
		self.assertEqual(l.name, "GMU")
		self.assertEqual(l.area_code, 703)
		self.assertEqual(l.number, 9931000)
		self.assertEqual(l.is_active, True)

	def test_Line_3(self):
		"""Line str"""
		l = Line("GMU",703,9931000,True)
		self.assertEqual(str(l),"703-9931000(GMU)")

	def test_Line_4(self):
		"""Line repr"""
		l = Line("GMU",703,9931000,True)
		self.assertEqual(repr(l),"Line('GMU', 703, 9931000)")

	def test_Line_5(self):
		"""Line eq"""
		l1 = Line("GMU",703,9931000)
		l2 = Line("GMU",703,9931000,True)
		l3 = Line("School",703,9931000,False)
		self.assertEqual(l1,l2)
		self.assertEqual(l1,l3)

	def test_Line_6(self):
		"""Line eq"""
		l1 = Line("GMU",703,9931000,True)
		l2 = Line("GMU",703,5551000,True)
		l3 = Line("GMU",212,9931000,True)
		self.assertNotEqual(l1,l2)
		self.assertNotEqual(l1,l3)
		#str1 = "703-9931000(GMU)"
		#self.assertNotEqual(l1,str1)

	def test_Line_7(self):
		"""Line activate"""
		l1 = Line("GMU",703,9931000,False)
		l1.activate()
		self.assertTrue(l1.is_active)

	def test_Line_8(self):
		"""Line deactivate"""
		l1 = Line("GMU",703,9931000,True)
		l1.deactivate()
		self.assertFalse(l1.is_active)
		
    ########################################################################### 
	
	def test_Call_1 (self):
		"""Call init"""
		l1 = Line("GMU",703,9931000,True)		
		l2 = Line("George",703,5551234,True) 
		c = Call(l1,l2,20)
		self.assertEqual(c.caller,l1)
		self.assertEqual(c.callee,l2)
		self.assertEqual(c.length,20)

	def test_Call_2 (self):
		"""Call str"""
		l1 = Line("GMU",703,9931000,True)		
		l2 = Line("George",703,5551234,True) 
		c = Call(l1,l2,20)
		self.assertEqual(str(c),"Call(Line('GMU', 703, 9931000), Line('George', 703, 5551234), 20)")

	def test_Call_3 (self):
		"""Call repr"""
		l1 = Line("GMU",703,9931000,True)		
		l2 = Line("George",703,5551234,True) 
		c = Call(l1,l2,20)
		self.assertEqual(str(c),"Call(Line('GMU', 703, 9931000), Line('George', 703, 5551234), 20)")

	def test_Call_4 (self):
		"""Call is_local"""
		l1 = Line("GMU",703,9931000,True)		
		l2 = Line("George",703,5551234,True) 
		c = Call(l1,l2,20)
		self.assertEqual(c.is_local(),True)
		
	def test_Call_5 (self):
		"""Call is_local"""
		l1 = Line("GMU",703,9931000,True)		
		l2 = Line("Mason",212,5551000,True)
		c = Call(l1,l2,30)
		self.assertEqual(c.is_local(),False)

    ########################################################################### 

	def test_PlanType_1 (self):
		"""PlanType init"""
		t = PlanType(20.0,200,0.50,False)		
		self.assertEqual(t.basic_rate,20.0)
		self.assertEqual(t.default_mins,200)
		self.assertEqual(t.rate_per_min,0.50)
		self.assertEqual(t.has_rollover,False)
		
	def test_PlanType_2 (self):
		"""PlanType init, default parameter"""
		t = PlanType(20.0,200,0.50)		
		self.assertEqual(t.basic_rate,20.0)
		self.assertEqual(t.default_mins,200)
		self.assertEqual(t.rate_per_min,0.50)
		self.assertEqual(t.has_rollover,True)

	def test_PlanType_3 (self):
		"""PlanType str"""
		t = PlanType(20.0,200,0.50,False)		
		self.assertEqual(str(t),"PlanType(20.00, 200, 0.50, False)")

	def test_PlanType_4 (self):
		"""PlanType repr"""
		t = PlanType(20.0,200,0.50,False)		
		self.assertEqual(repr(t),"PlanType(20.00, 200, 0.50, False)")

		
    ########################################################################### 

	def test_CallError_1 (self):
		"""CallError init"""
		ce1 = CallError('test')
		self.assertEqual(ce1.msg, 'test')
		ce2 = CallError('my error message')
		self.assertEqual(ce2.msg, 'my error message')

	def test_CallError_2 (self):
		"""CallError str"""
		ce1 = CallError('test')
		ce2 = CallError('my error message')
		self.assertEqual(str(ce1), "CallError: test")
		self.assertEqual(str(ce2), "CallError: my error message")

	def test_CallError_3 (self):
		"""CallError repr"""
		ce1 = CallError('test')
		ce2 = CallError('my error message')
		self.assertEqual(repr(ce1), "CallError('test')")
		self.assertEqual(repr(ce2), "CallError('my error message')")

	def test_CallError_4 (self):
		"""Call attempt triggers CallError: negative call length"""
		l1 = Line("GMU",703,9931000,True)		
		l2 = Line("George",703,5551234,True) 
		try:
			c = Call(l1,l2,-20)
			self.fail ("should have raised CallError, because call length cannot be negative.")
		except CallError:
			pass	
		
	def test_CallError_5 (self):
		"""Call attempt triggers CallError: caller and callee are the same"""
		l1 = Line("GMU",703,9931000,True)		
		try:
			c = Call(l1,l1,20)
			self.fail ("should have raised CallError, because a line cannot call itself.")
		except CallError:
			pass	

	def test_CallError_6 (self):
		"""Call attempt triggers CallError: caller/callee not active"""
		l1 = Line("GMU",703,9931000,False)		
		l2 = Line("George",703,5551234,True) 
		try:
			c1 = Call(l1,l2,20)
			c2 = Call(l2,l1,20)
			self.fail ("should have raised CallError, because caller/callee is inactive.")
		except CallError:
			pass	

	def test_CallError_7 (self):
		"""Call attempt triggers CallError: error message checking"""
		l1 = Line("GMU",703,9931000,True)		
		l2 = Line("George",703,5551234,True) 
		try:
			c = Call(l1,l2,-20)
			self.fail ("should have raised CallError, because call length cannot be negative.")
		except CallError as ce:
			self.assertEqual(ce.msg,"negative call length: -20")	

	def test_CallError_8 (self):
		"""Call attempt triggers CallError: error message checking"""
		l1 = Line("GMU",703,9931000,True)		
		l2 = Line("George",703,5551234,False) 
		try:
			c = Call(l1,l1,10)
			self.fail ("should have raised CallError, because a line cannot call itself.")
		except CallError as ce:
			self.assertEqual(ce.msg,"line 703-9931000(GMU) cannot call itself")	

		try:
			c1 = Call(l1,l2,20)
			self.fail ("should have raised CallError, because callee is inactive.")
		except CallError as ce:
			self.assertEqual(ce.msg,"line 703-5551234(George) not active")	

				
    ########################################################################### 

	def test_PhonePlanError_1 (self):
		"""PhonePlanError init"""
		pe1 = PhonePlanError('test')
		self.assertEqual(pe1.msg, 'test')
		pe2 = PhonePlanError('my error message')
		self.assertEqual(pe2.msg, 'my error message')

	def test_PhonePlanError_2 (self):
		"""PhonePlanError str"""
		pe1 = PhonePlanError('test phone plan')
		pe2 = PhonePlanError('my phone plan error')
		self.assertEqual(str(pe1), "PhonePlanError: test phone plan")
		self.assertEqual(str(pe2), "PhonePlanError: my phone plan error")

	def test_PhonePlanError_3 (self):
		"""PhonePlanError repr"""
		pe1 = PhonePlanError('test phone plan')
		pe2 = PhonePlanError('my phone plan error')
		self.assertEqual(repr(pe1), "PhonePlanError('test phone plan')")
		self.assertEqual(repr(pe2), "PhonePlanError('my phone plan error')")
	
    ########################################################################### 
    
	
	def test_PhonePlan_1 (self):
		"""PhonePlan init"""
		l1 = Line("GMU",703,9931000,True)		
		l2 = Line("George",703,5551234,True) 
		t = PlanType(20.0,200,0.50,False)
		p = PhonePlan(t,[l1,l2])
		self.assertEqual(p.type, t)
		self.assertEqual(p.lines,[l1,l2])
		self.assertEqual(p.calls,[])
		self.assertEqual(p.balance, 0)
		self.assertEqual(p.rollover_mins, 0)
		self.assertEqual(p.mins_to_pay, 0)

	def test_PhonePlan_2 (self):
		"""PhonePlan init, default parameters"""
		t = PlanType(20.0,200,0.50,False)
		p = PhonePlan(t)
		self.assertEqual(p.type, t)
		self.assertEqual(p.lines,[])
		self.assertEqual(p.calls,[])
		self.assertEqual(p.balance, 0)
		self.assertEqual(p.rollover_mins, 0)
		self.assertEqual(p.mins_to_pay, 0)

	def test_PhonePlan_3 (self):
		"""PhonePlan str/repr"""
		t = PlanType(20.0,200,0.50,False)
		p = PhonePlan(t)
		self.assertEqual(str(p), "PhonePlan(PlanType(20.00, 200, 0.50, False), [], [])")
		self.assertEqual(repr(p), "PhonePlan(PlanType(20.00, 200, 0.50, False), [], [])")
		
	def test_PhonePlan_4 (self):
		"""PhonePlan str/repr"""
		l1 = Line("GMU",703,9931000,True)		
		l2 = Line("George",703,5551234,True) 
		t = PlanType(20.0,200,0.50,False)
		p = PhonePlan(t,[l1,l2])
		self.assertEqual(str(p), "PhonePlan(PlanType(20.00, 200, 0.50, False), [Line('GMU', 703, 9931000), Line('George', 703, 5551234)], [])")
		self.assertEqual(repr(p), "PhonePlan(PlanType(20.00, 200, 0.50, False), [Line('GMU', 703, 9931000), Line('George', 703, 5551234)], [])")
	
    ########################################################################### 

	def test_activate_all_1 (self):
		"""activate_all: originally all active"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",212,5551234) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l2,l3])
		p.activate_all()
		self.assertTrue(l1.is_active)
		self.assertTrue(l2.is_active)
		self.assertTrue(l3.is_active)
			
	def test_activate_all_2 (self):
		"""activate_all: originally none active"""
		l1 = Line("GMU",703,9931000,False)		
		l2 = Line("George",703,5551234,False) 
		l3 = Line("Mason",212,5551234,False) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l2,l3])
		p.activate_all()
		self.assertTrue(l1.is_active)
		self.assertTrue(l2.is_active)
		self.assertTrue(l3.is_active)

	def test_activate_all_3 (self):
		"""activate_all: originally some active"""
		l1 = Line("GMU",703,9931000,False)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",212,5551234,False) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l2,l3])
		p.activate_all()
		self.assertTrue(l1.is_active)
		self.assertTrue(l2.is_active)
		self.assertTrue(l3.is_active)

    ########################################################################### 

	def test_deactivate_all_1 (self):
		"""activate_all: originally all active"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",212,5551234) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l2,l3])
		p.deactivate_all()
		self.assertFalse(l1.is_active)
		self.assertFalse(l2.is_active)
		self.assertFalse(l3.is_active)
			
	def test_deactivate_all_2 (self):
		"""activate_all: originally none active"""
		l1 = Line("GMU",703,9931000,False)		
		l2 = Line("George",703,5551234,False) 
		l3 = Line("Mason",212,5551234,False) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l2,l3])
		p.deactivate_all()
		self.assertFalse(l1.is_active)
		self.assertFalse(l2.is_active)
		self.assertFalse(l3.is_active)

	def test_deactivate_all_3 (self):
		"""activate_all: originally some active"""
		l1 = Line("GMU",703,9931000,False)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",212,5551234,False) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l2,l3])
		p.deactivate_all()
		self.assertFalse(l1.is_active)
		self.assertFalse(l2.is_active)
		self.assertFalse(l3.is_active)

    ########################################################################### 

	def test_add_call_1 (self):
		"""add_call: added (only call), not billable"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1])
		c = Call(l1,l2,20)
		p.add_call(c)
		self.assertEqual(p.calls, [c]) #call appended
		self.assertEqual(p.mins_to_pay, 0) #local call is free

	def test_add_call_2 (self):
		"""add_call: added (only call), not billable"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",240,5551234) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l2])
		c = Call(l1,l2,20)
		p.add_call(c)
		self.assertEqual(p.calls, [c]) #call appended
		self.assertEqual(p.mins_to_pay, 0) #call between two lines of this plan is free

	def test_add_call_3 (self):
		"""add_call: added (only call), billable"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",240,5551234) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1])
		c = Call(l1,l2,20)
		p.add_call(c)
		self.assertEqual(p.calls, [c]) #call appended
		self.assertEqual(p.mins_to_pay, 20) #update mins_to_pay

	def test_add_call_4 (self):
		"""add_call: added multiple calls, all free"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",240,5551234) 
		l3 = Line("Mason",703,5551234) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l2])
		c1 = Call(l1,l2,20)
		p.add_call(c1)
		c2 = Call(l1,l2,15)
		p.add_call(c2)
		c3 = Call(l3,l1,18)
		p.add_call(c3)
		self.assertEqual(p.calls,[c1,c2,c3])
		self.assertEqual(p.mins_to_pay, 0) #all calls free

	def test_add_call_5 (self):
		"""add_call: added multiple calls, some billable"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",240,5551234) 
		l3 = Line("Mason",703,5551234) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1])
		c1 = Call(l1,l2,20)
		p.add_call(c1)
		c2 = Call(l3,l1,15)
		p.add_call(c2)
		c3 = Call(l1,l2,18)
		p.add_call(c3)
		self.assertEqual(p.calls,[c1,c2,c3])
		self.assertEqual(p.mins_to_pay, 38) # c1 and c3 are billable

	def test_add_call_6 (self):
		"""add_call: added multiple calls, all billable"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",240,5551234) 
		l3 = Line("Mason",704,5551234) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1])
		c1 = Call(l1,l2,20)
		p.add_call(c1)
		c2 = Call(l3,l1,15)
		p.add_call(c2)
		c3 = Call(l1,l2,18)
		p.add_call(c3)
		self.assertEqual(p.calls,[c1,c2,c3])
		self.assertEqual(p.mins_to_pay, 53) # all are billable

	def test_add_call_7 (self):
		"""add_call: failed to add"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",212,5551234) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1])
		c = Call(l2,l3,18)
		try:
			p.add_call(c)
			self.fail("should have raised PhonePlanError, because neither caller nor callee belongs to the plan.")
		except PhonePlanError:
			pass

	def test_add_call_8 (self):
		"""add_call: failed to add"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",212,5551234) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1])
		c1 = Call(l1,l2,20)
		p.add_call(c1)
		c2 = Call(l3,l1,15)
		p.add_call(c2)
		c3 = Call(l2,l3,18)
		try:
			p.add_call(c3)
			self.fail("should have raised PhonePlanError, because neither caller nor callee belongs to the plan.")
		except PhonePlanError as pe:
			self.assertEqual(p.calls,[c1,c2])
			self.assertEqual(p.mins_to_pay,15) #c2 needs to pay
			self.assertEqual(pe.msg,"call cannot be added")

	
    ########################################################################### 

	def test_add_calls_1 (self):
		"""add_calls: all added, free calls"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",240,5551234) 
		l3 = Line("Mason",703,5551234) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l2])
		c1 = Call(l1,l2,20)
		c2 = Call(l1,l2,15)
		c3 = Call(l3,l1,18)
		ans = p.add_calls([c1,c2,c3])
		self.assertEqual(ans, 3)
		self.assertEqual(p.calls,[c1,c2,c3])
		self.assertEqual(p.mins_to_pay, 0) #all calls free
		
		# this line requires that your definition of add_calls directly includes a call to add_call().
		enforce_func_usage(PhonePlan.add_calls,"add_call")

	def test_add_calls_2 (self):
		"""add_calls: all added, all not free"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",240,5551234) 
		l3 = Line("Mason",202,5551234) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1])
		c1 = Call(l1,l2,10)
		c2 = Call(l2,l1,20)
		c3 = Call(l3,l1,30)
		ans = p.add_calls([c1,c2,c3])
		self.assertEqual(ans, 3)
		self.assertEqual(p.calls,[c1,c2,c3])
		self.assertEqual(p.mins_to_pay, 60) # no free calls
		
		# this line requires that your definition of add_calls directly includes a call to add_call().
		enforce_func_usage(PhonePlan.add_calls,"add_call")

	def test_add_calls_3 (self):
		"""add_calls: all added, some free"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",240,5551234) 
		l3 = Line("Mason",202,5551234) 
		l4 = Line("Washinton",703,5556000) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l2])
		c1 = Call(l1,l2,10)
		c2 = Call(l2,l3,20)
		c3 = Call(l3,l1,30)
		c4 = Call(l1,l4,40)
		ans = p.add_calls([c1,c2,c3,c4])
		self.assertEqual(ans, 4)
		self.assertEqual(p.calls,[c1,c2,c3,c4])
		self.assertEqual(p.mins_to_pay, 50) # some free calls
		
		# this line requires that your definition of add_calls directly includes a call to add_call().
		enforce_func_usage(PhonePlan.add_calls,"add_call")

	def test_add_calls_4 (self):
		"""add_calls: none added due to PhonePlanError"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",240,5551234) 
		l3 = Line("Mason",202,5551234) 
		l4 = Line("Washinton",703,5556000) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1])
		c1 = Call(l3,l2,10)
		c2 = Call(l2,l4,20)
		c3 = Call(l3,l4,30)
		ans = p.add_calls([c1,c2,c3])
		self.assertEqual(ans, 0) #none added successfully
		self.assertEqual(p.calls,[])
		self.assertEqual(p.mins_to_pay, 0)
		
		# this line requires that your definition of add_calls directly includes a call to add_call().
		enforce_func_usage(PhonePlan.add_calls,"add_call")

	def test_add_calls_5 (self):
		"""add_calls: some not added due to PhonePlanError"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",240,5551234) 
		l3 = Line("Mason",202,5551234) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1])
		c1 = Call(l1,l2,10)
		c2 = Call(l2,l3,20)
		c3 = Call(l3,l1,30)
		c4 = Call(l3,l2,40)
		ans = p.add_calls([c1,c2,c3,c4])
		self.assertEqual(ans, 2) # 2 calls of the given list added successfully
		self.assertEqual(p.calls,[c1,c3])
		self.assertEqual(p.mins_to_pay,40) 
		
		# this line requires that your definition of add_calls directly includes a call to add_call().
		enforce_func_usage(PhonePlan.add_calls,"add_call")
		
    ########################################################################### 

	def test_make_call_1 (self):
		"""make_call: call made successfully, free call"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1])
		ans = p.make_call(l1,l2,10)
		self.assertEqual(ans,True)
		self.assertEqual(len(p.calls),1)
		self.assertEqual(p.calls[0].caller,l1)
		self.assertEqual(p.calls[0].callee,l2)		
		self.assertEqual(p.calls[0].length,10)
		self.assertEqual(p.mins_to_pay,0) 

	def test_make_call_2 (self):
		"""make_call: call made successfully, free call"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",301,5551234) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l2])
		ans = p.make_call(l1,l2,10)
		self.assertEqual(ans,True)
		self.assertEqual(len(p.calls),1)
		self.assertEqual(p.calls[0].caller,l1)
		self.assertEqual(p.calls[0].callee,l2)		
		self.assertEqual(p.calls[0].length,10)
		self.assertEqual(p.mins_to_pay,0) 

	def test_make_call_3 (self):
		"""make_call: call made successfully, billable call"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",301,5551234) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1])
		ans = p.make_call(l1,l2,10)
		self.assertEqual(ans,True)
		self.assertEqual(len(p.calls),1)
		self.assertEqual(p.calls[0].caller,l1)
		self.assertEqual(p.calls[0].callee,l2)		
		self.assertEqual(p.calls[0].length,10)
		self.assertEqual(p.mins_to_pay,10) 
		
	def test_make_call_4 (self):
		"""make_call: multiple calls made successfully"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",212,5551234) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1])
		p.make_call(l1,l2,10)
		self.assertEqual(p.make_call(l2,l1,25),True)
		self.assertEqual(p.make_call(l1,l3,5),True)

		self.assertEqual(len(p.calls),3)
		self.assertEqual(p.calls[0].caller,l1)
		self.assertEqual(p.calls[1].callee,l1)		
		self.assertEqual(p.calls[2].length,5)
		self.assertEqual(p.mins_to_pay,5) #c1 and c2 are free

	def test_make_call_5 (self):
		"""make_call: call fails due to CallError"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1])
		self.assertEqual(p.make_call(l1,l2,-5),False) #negative length
		self.assertEqual(len(p.calls),0) #no call added
		self.assertEqual(p.mins_to_pay,0) 

	def test_make_call_6 (self):
		"""make_call: call fails due to CallError"""
		l1 = Line("GMU",703,9931000)		
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1])
		self.assertEqual(p.make_call(l1,l1,5),False) #line calls itself
		self.assertEqual(len(p.calls),0) #no call added
		self.assertEqual(p.mins_to_pay,0) 

	def test_make_call_7 (self):
		"""make_call: call fails due to CallError"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234,False) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1])
		self.assertEqual(p.make_call(l1,l2,5),False) #line calls an inactive line
		self.assertEqual(len(p.calls),0) #no call added
		self.assertEqual(p.mins_to_pay,0) 

	def test_make_call_8 (self):
		"""make_call: call fails due to PhonePlanError"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",212,5551234) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1])
		self.assertEqual(p.make_call(l2,l3,5),False) #lines do not belong to this plan
		self.assertEqual(len(p.calls),0) #no call added
		self.assertEqual(p.mins_to_pay,0) 


    ########################################################################### 

	def test_mins_by_line_1 (self):
		"""mins_by_line: no call for the line"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",212,5554321) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l3])
		c1 = Call(l1,l2,10)
		c2 = Call(l2,l1,20)
		p.calls = [c1,c2] 
		self.assertEqual(p.mins_by_line(l3),0) 

	def test_mins_by_line_2 (self):
		"""mins_by_line: one call for the line"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l3])
		c1 = Call(l1,l2,10)
		c2 = Call(l2,l1,20)
		c3 = Call(l3,l2,5)
		p.calls = [c1,c2,c3] 
		self.assertEqual(p.mins_by_line(l3),5) 

	def test_mins_by_line_3 (self):
		"""mins_by_line: multiple calls for the line"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l3])
		c1 = Call(l1,l2,10)
		c2 = Call(l2,l1,20)
		c3 = Call(l3,l2,5)
		c4 = Call(l3,l1,17)
		p.calls = [c1,c2,c3,c4] 
		self.assertEqual(p.mins_by_line(l1),47) 

	def test_mins_by_line_4 (self):
		"""mins_by_line: line not in the plan"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l3])
		c1 = Call(l1,l2,10)
		c2 = Call(l2,l1,20)
		c3 = Call(l3,l2,5)
		p.calls = [c1,c2,c3] 
		self.assertEqual(p.mins_by_line(l2),0) 
	
    ############################################################################

	def test_calls_by_line_1 (self):
		"""calls_by_line: no call for the line"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l3])
		c1 = Call(l1,l2,10)
		c2 = Call(l2,l1,20)
		p.calls = [c1,c2] 
		self.assertEqual(p.calls_by_line(l3),0) 
		
	def test_calls_by_line_2 (self):
		"""calls_by_line: one call for the line"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l3])
		c1 = Call(l1,l2,10)
		c2 = Call(l2,l3,20)
		p.calls = [c1,c2] 
		self.assertEqual(p.calls_by_line(l1),1) 

	def test_calls_by_line_3 (self):
		"""calls_by_line: multiple calls for the line"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l3])
		c1 = Call(l1,l2,10)
		c2 = Call(l2,l1,20)
		c3 = Call(l3,l2,5)
		c4 = Call(l3,l1,17)
		p.calls = [c1,c2,c3,c4] 
		self.assertEqual(p.calls_by_line(l1),3) 

	def test_calls_by_line_4 (self):
		"""calls_by_line: line not in the plan"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l3])
		c1 = Call(l1,l2,10)
		c2 = Call(l2,l1,20)
		c3 = Call(l3,l2,5)
		p.calls = [c1,c2,c3] 
		self.assertEqual(p.calls_by_line(l2),0) 
		
    ########################################################################### 

	def test_remove_call_1 (self):
		"""remove_call: removed the only call"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l3])
		c1 = Call(l1,l2,10)
		p.calls = [c1] 
		p.remove_call(c1)
		self.assertEqual(p.calls, []) 

	def test_remove_call_2 (self):
		"""remove_call: removed from front"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l3])
		c1 = Call(l1,l2,10)
		c2 = Call(l2,l1,20)
		c3 = Call(l3,l2,5)
		c4 = Call(l3,l1,17)
		p.calls = [c1,c2,c3,c4] 
		p.remove_call(c1)
		self.assertEqual(p.calls, [c2,c3,c4]) 

	def test_remove_call_3 (self):
		"""remove_call: removed from middle"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l3])
		c1 = Call(l1,l2,10)
		c2 = Call(l2,l1,20)
		c3 = Call(l3,l2,5)
		c4 = Call(l3,l1,17)
		p.calls = [c1,c2,c3,c4] 
		p.remove_call(c2)
		self.assertEqual(p.calls, [c1,c3,c4]) 

	def test_remove_call_4 (self):
		"""remove_call: removed from end"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l3])
		c1 = Call(l1,l2,10)
		c2 = Call(l2,l1,20)
		c3 = Call(l3,l2,5)
		c4 = Call(l3,l1,17)
		p.calls = [c1,c2,c3,c4] 
		p.remove_call(c4)
		self.assertEqual(p.calls, [c1,c2,c3]) 

	def test_remove_call_5 (self):
		"""remove_call: no call to remove from an empty list"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l3])
		c1 = Call(l1,l2,10)
		try:
			p.remove_call(c1) # try to remove from an empty list
			self.fail("should have raised PhonePlanError because no such call to remove")
		except PhonePlanError:
			pass

	def test_remove_call_6 (self):
		"""remove_call: no call to remove from an empty list"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l3])
		c1 = Call(l1,l2,10)
		try:
			p.remove_call(c1) # try to remove from an empty list
			self.fail("should have raised PhonePlanError because no such call to remove")
		except PhonePlanError as pe:
			self.assertEqual(pe.msg, "no such call to remove") 

	def test_remove_call_7 (self):
		"""remove_call: no such call to remove"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l3])
		c1 = Call(l1,l2,10)
		c2 = Call(l2,l1,20)
		c3 = Call(l3,l2,5)
		c4 = Call(l3,l1,17)
		p.calls = [c1,c2,c3] 
		try:
			p.remove_call(c4)
			self.fail("should have raised PhonePlanError because no such call to remove")
		except PhonePlanError:
			self.assertEqual(p.calls, [c1,c2,c3]) 

    ########################################################################### 

	def test_add_line_1 (self):
		"""add_line: line added (only line)"""
		l1 = Line("GMU",703,9931000)		
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t)
		p.add_line(l1)
		self.assertEqual(p.lines, [l1]) 

	def test_add_line_2 (self):
		"""add_line: line added at the end of non-empty list"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1])
		p.add_line(l2)
		self.assertEqual(p.lines, [l1,l2]) 

	def test_add_line_3 (self):
		"""add_line: duplicated line fail to add"""
		l1 = Line("GMU",703,9931000)		
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1])
		try:
			p.add_line(l1)
			p.fail("should have raised PhonePlanError: try to add duplicated line")
		except PhonePlanError as pe:
			self.assertEqual(p.lines, [l1]) 

	def test_add_line_4 (self):
		"""add_line: duplicated line fail to add"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l2,l3])
		try:
			p.add_line(Line("school",703,9931000))
			p.fail("should have raised PhonePlanError: try to add duplicated line")
		except PhonePlanError:
			self.assertEqual(p.lines, [l1,l2,l3]) 

	def test_add_line_5 (self):
		"""add_line: duplicated line fail to add, check error msg"""
		l1 = Line("GMU",703,9931000)		
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1])
		try:
			p.add_line(l1)
			p.fail("should have raised PhonePlanError: try to add duplicated line")
		except PhonePlanError as pe:
			self.assertEqual(pe.msg, "duplicated line to add") 

    ########################################################################### 

	def test_remove_line_1 (self):
		"""remove_line: line removed (only line), no call"""
		l1 = Line("GMU",703,9931000)		
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1])
		p.remove_line(l1)
		self.assertEqual(p.lines, []) 
		self.assertEqual(p.calls, []) 

	def test_remove_line_2 (self):
		"""remove_line: line removed from front, no call for that line"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l2,l3])
		p.remove_line(l1)
		self.assertEqual(p.lines, [l2,l3]) 
		self.assertEqual(p.calls, []) 

	def test_remove_line_3 (self):
		"""remove_line: line removed from middle, no call for that line"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l2,l3])
		p.remove_line(Line("name",703,5551234))
		self.assertEqual(p.lines, [l1,l3]) 
		self.assertEqual(p.calls, []) 

	def test_remove_line_4 (self):
		"""remove_line: line removed from end, no call for that line"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l2,l3])
		p.remove_line(Line("name",703,5554321))
		self.assertEqual(p.lines, [l1,l2]) 
		self.assertEqual(p.calls, []) 

	def test_remove_line_5 (self):
		"""remove_line: line removed, no call removed"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l2,l3])
		c1 = Call(l1,l2,10)
		c2 = Call(l2,l1,20)
		c3 = Call(l3,l2,5)
		c4 = Call(l1,l3,50)
		p.calls = [c1,c2,c3,c4] 
		p.remove_line(l3)
		self.assertEqual(p.lines, [l1,l2]) 
		self.assertEqual(p.calls, [c1,c2,c3,c4]) 

	def test_remove_line_6 (self):
		"""remove_line: line removed, one call removed"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l2])
		c1 = Call(l1,l2,10)
		c2 = Call(l2,l1,20)
		c3 = Call(l3,l2,5)
		p.calls = [c1,c2,c3] 
		p.remove_line(l2)
		self.assertEqual(p.lines, [l1]) 
		self.assertEqual(p.calls, [c1,c2]) 

	def test_remove_line_7 (self):
		"""remove_line: line removed, multiple calls removed"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l2])
		c1 = Call(l1,l2,10)
		c2 = Call(l2,l3,25)
		c3 = Call(l2,l1,20)
		c4 = Call(l3,l2,5)
		p.calls = [c1,c2,c3,c4] 
		p.remove_line(l2)
		self.assertEqual(p.lines, [l1]) 
		self.assertEqual(p.calls, [c1,c3]) 

	def test_remove_line_8 (self):
		"""remove_line: line removed, multiple calls removed"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l2])
		c1 = Call(l1,l2,10)
		c2 = Call(l2,l3,25)
		c3 = Call(l2,l1,20)
		c4 = Call(l2,l3,25)
		c5 = Call(l3,l2,5)
		c6 = Call(l1,l3,26)
		p.calls = [c1,c2,c3,c4,c5,c6] 
		p.remove_line(l2)
		self.assertEqual(p.lines, [l1]) 
		self.assertEqual(p.calls, [c1,c3,c6]) 

	def test_remove_line_9 (self):
		"""remove_line: line removed, all calls removed"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1])
		c1 = Call(l1,l2,10)
		c2 = Call(l2,l1,25)
		c3 = Call(l3,l1,20)
		c4 = Call(l1,l3,5)
		p.calls = [c1,c2,c3,c4] 
		p.remove_line(l1)
		self.assertEqual(p.lines, []) 
		self.assertEqual(p.calls, []) 

	def test_remove_line_10 (self):
		"""remove_line: empty list; no line to remove"""
		l1 = Line("GMU",703,9931000)		
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[])
		try:
			p.remove_line(l1)
			p.fail("should have raised PhonePlanError: no such line to remove")
		except PhonePlanError as pe:
			self.assertEqual(pe.msg, "no such line to remove") 

	def test_remove_line_11 (self):
		"""remove_line: no such line to remove"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l2])
		try:
			p.remove_line(l3)
			p.fail("should have raised PhonePlanError: no such line to remove")
		except PhonePlanError as pe:
			self.assertEqual(p.lines, [l1,l2]) 

    ########################################################################### 


	def test_calculate_bill_1 (self):
		"""calculate_bill: billable minutes covered by default mins"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l2,l3])
		p.mins_to_pay = 200  #assume call record has been cleared but mins calcualted
		p.calculate_bill()
		self.assertEqual(p.balance, 20.0)
		self.assertEqual(p.mins_to_pay, 0) 
 
		
	def test_calculate_bill_2 (self):
		"""calculate_bill: billable minutes covered by default mins, rollover updated"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l2,l3])
		p.mins_to_pay = 180  #assume call record has been cleared but mins calcualted
		p.calculate_bill()
		self.assertEqual(p.balance, 20.0) 
		self.assertEqual(p.rollover_mins, 20) 
		self.assertEqual(p.mins_to_pay, 0) 

	def test_calculate_bill_3 (self):
		"""calculate_bill: billable minutes covered by default mins, no rollover"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(20.0,200,0.50,False) # rollover not allowed
		p = PhonePlan(t,[l1,l2,l3])
		p.mins_to_pay = 180  #assume call record has been cleared but mins calcualted
		p.calculate_bill()
		self.assertEqual(p.balance, 20.0) 
		self.assertEqual(p.rollover_mins, 0) 
		self.assertEqual(p.mins_to_pay, 0) 

	def test_calculate_bill_4 (self):
		"""calculate_bill: billable minutes covered by default+rollover mins"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l2,l3])
		p.mins_to_pay = 280  #assume call record has been cleared but mins calcualted
		p.rollover_mins = 85 #assume rollover mins available
		p.calculate_bill()
		self.assertEqual(p.balance, 20.0) 
		self.assertEqual(p.rollover_mins, 5) 
		self.assertEqual(p.mins_to_pay, 0) 
		
	def test_calculate_bill_5 (self):
		"""calculate_bill: billable minutes not covered by default+rollover mins"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l2,l3])
		p.mins_to_pay = 280  #assume call record has been cleared but mins calcualted
		p.rollover_mins = 15 #assume rollover mins available
		p.calculate_bill()
		self.assertEqual(p.balance, 52.5) 
		self.assertEqual(p.rollover_mins, 0) 
		self.assertEqual(p.mins_to_pay, 0) 

	def test_calculate_bill_5 (self):
		"""calculate_bill: billable minutes not covered by default mins, no rollover mins"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(20.0,200,0.20,False)
		p = PhonePlan(t,[l1,l2,l3])
		p.mins_to_pay = 280  #assume call record has been cleared but mins calcualted
		p.calculate_bill()
		self.assertEqual(p.balance, 36) 
		self.assertEqual(p.rollover_mins, 0) 
		self.assertEqual(p.mins_to_pay, 0) 

	def test_calculate_bill_6 (self):
		"""calculate_bill: clear call record"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",215,5551234) 
		l3 = Line("Mason",412,5554321) 
		t = PlanType(30.0,100,0.50)
		p = PhonePlan(t,[l1])
		c1 = Call(l1,l2,10)
		c2 = Call(l2,l1,75)
		c3 = Call(l3,l1,40)
		c4 = Call(l1,l3,50)
		p.calls = [c1,c2,c3,c4] 
		p.mins_to_pay = 175
		p.calculate_bill()
		self.assertEqual(p.balance, 67.5) 
		self.assertEqual(p.rollover_mins, 0) 
		self.assertEqual(p.mins_to_pay, 0) 
		self.assertEqual(p.calls, []) 
		self.assertEqual(l1.is_active, True) 
		
	def test_calculate_bill_7 (self):
		"""calculate_bill: deactivate the only line"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",215,5551234) 
		l3 = Line("Mason",412,5554321) 
		t = PlanType(15.0,100,0.5)
		p = PhonePlan(t,[l1])
		c1 = Call(l1,l2,100)
		c2 = Call(l2,l1,5)
		c3 = Call(l3,l1,23)
		c4 = Call(l1,l2,117)
		p.calls = [c1,c2,c3,c4] 
		p.mins_to_pay = 100+5+23+117
		p.rollover_mins = 10
		p.calculate_bill()
		self.assertEqual(p.balance, 82.5) 
		self.assertEqual(p.rollover_mins, 0) 
		self.assertEqual(p.mins_to_pay, 0) 
		self.assertEqual(p.calls, []) 
		self.assertEqual(l1.is_active, False) #line deactivated due to high balance 

	def test_calculate_bill_8 (self):
		"""calculate_bill: deactivate all lines"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",215,5551234) 
		l3 = Line("Mason",412,5554321) 
		l4 = Line("Washington",304,5556789) 
		t = PlanType(10.0,150,1.5)
		p = PhonePlan(t,[l1,l2,l3])
		c1 = Call(l1,l4,100)
		c2 = Call(l2,l4,55)
		c3 = Call(l4,l3,148)
		c4 = Call(l4,l1,70)
		p.calls = [c1,c2,c3,c4] 
		p.mins_to_pay = 100+55+148+70
		p.rollover_mins = 20
		p.calculate_bill()
		self.assertEqual(p.balance, 314.5) 
		self.assertEqual(p.rollover_mins, 0) 
		self.assertEqual(p.mins_to_pay, 0) 
		self.assertEqual(p.calls, []) 
		self.assertEqual(l1.is_active, False) #line deactivated due to high balance 
		self.assertEqual(l2.is_active, False) #line deactivated due to high balance 
		self.assertEqual(l3.is_active, False) #line deactivated due to high balance 
		

    ########################################################################### 

	def test_pay_bill_1 (self):
		"""pay_bill: fully paid"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(50.0,200,0.50)
		p = PhonePlan(t,[l1,l2,l3])
		p.balance = 100  #assume balance calculated
		p.pay_bill()
		self.assertEqual(p.balance, 0)

	def test_pay_bill_2 (self):
		"""pay_bill: partially paid"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(50.0,200,0.50)
		p = PhonePlan(t,[l1,l2,l3])
		p.balance = 100  #assume balance calculated
		p.pay_bill(25)
		self.assertEqual(p.balance, 75)

	def test_pay_bill_3 (self):
		"""pay_bill: overly paid"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(50.0,200,0.50)
		p = PhonePlan(t,[l1,l2,l3])
		p.balance = 100  #assume balance calculated
		p.pay_bill(200)
		self.assertEqual(p.balance, -100)

	def test_pay_bill_4 (self):
		"""pay_bill: overly paid"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(50.0,200,0.50)
		p = PhonePlan(t,[l1,l2,l3])
		p.balance = -10  #assume credit
		p.pay_bill()
		self.assertEqual(p.balance, -10)

	def test_pay_bill_5 (self):
		"""pay_bill: fully paid, activate lines"""
		l1 = Line("GMU",703,9931000,False)	# assume inactive lines 	
		l2 = Line("George",703,5551234,False) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l2])
		p.balance = 100  #assume balance calculated > 4*base_rate
		p.pay_bill(100)
		self.assertEqual(p.balance, 0)
		self.assertEqual(l1.is_active, True)
		self.assertEqual(l2.is_active, True)

	def test_pay_bill_6 (self):
		"""pay_bill: partially paid, activate lines"""
		l1 = Line("GMU",703,9931000,False)	# assume inactive lines 	
		l2 = Line("George",703,5551234,False) 
		t = PlanType(20.0,200,0.50)
		p = PhonePlan(t,[l1,l2])
		p.balance = 100  #assume balance calculated > 4*base_rate
		p.pay_bill(20)
		self.assertEqual(p.balance, 80)
		self.assertEqual(l1.is_active, True)
		self.assertEqual(l2.is_active, True)

	def test_pay_bill_7 (self):
		"""pay_bill: negative amount to pay is ValueError"""
		l1 = Line("GMU",703,9931000)		
		l2 = Line("George",703,5551234) 
		l3 = Line("Mason",703,5554321) 
		t = PlanType(50.0,200,0.50)
		p = PhonePlan(t,[l1,l2,l3])
		p.balance = 80  #assume balance calculated 
		try:
			p.pay_bill(-20)
			self.fail("should have raised ValueError since pay amount cannot be negative")
		except ValueError as ve:
			self.assertEqual(p.balance, 80)
			self.assertEqual(str(ve), "amount to pay cannot be negative")

    ########################################################################### 
	
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
		print("\nScore based on test cases: %.2f / %d ( %d * %.2f + %d * %.2f) " % (
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