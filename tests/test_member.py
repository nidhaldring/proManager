

import unittest

from models.member import *

# mock objects
class MockDbManager:
	def execute(self,sql):
		return [("1","1","1","1")]
class MockQueryMaker:
	def makeInsertQuery(*args,**kargs):pass
	def makeDeleteQuery(*args,**kargs):pass
	def makeUpdateQuery(*args,**kargs):pass
	def makeSearchQuery(*args,**kargs):pass

#

class TestMember(unittest.TestCase):

	def __init__(self,*args,**kargs):

		super().__init__(*args,**kargs)
		Member.dbManager = MockDbManager()
		Member.queryMaker = MockQueryMaker()
		Member.table = "table"

	def setUp(self):
		self.u = Member("h","g","h@g.com")

	def test_delete_raises_when_deleting_unregistred_member(self):
		self.assertRaises(ModelNotInsertedException,self.u.delete)


	def test_insert_raises_when_reinserting_same_member(self):
		self.u.insert()
		self.assertRaises(ModelAlreadyInsertedException,self.u.insert)

	def test_register_set_member_id(self):
		self.u.insert()
		self.assertNotEqual(self.u.id,None)

	def test_delete_set_id_to_None(self):
		self.u.insert()
		self.u.delete()
		self.assertEqual(self.u.id,None)

	def test_update_raises_when_updating_unregistred_member(self):
		newData = {"email":"ff@ff.com","password":"555"}
		self.assertRaises(ModelNotInsertedException,self.u.update,newData)

	def test_update_change_member_attributes(self):
		newData = {"email":"ff@ff.com","password":"555"}
		self.u.insert().update(newData)
		for key,v in newData.items():
			self.assertEqual(getattr(self.u,key),v)

	def test_member_id_raises_when_attempted_to_be_changed(self):
		with self.assertRaises(AttributeError):
			self.u.id = 0

	def test_query_returns_Member_with_correct_condition(self):
		u = Member.query({"email":"1"})
		self.assertNotEqual(u,[])
		self.assertEqual(u[0].email,"1")
