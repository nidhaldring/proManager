

import unittest

from models.utils.sqlQueryMaker import SQLQueryMaker

class TestSQLQueryMaker(unittest.TestCase):

	def __init__(self,*args,**kargs):

		super().__init__(*args,**kargs)
		self.queryMaker = SQLQueryMaker("test")

	def test_makeInsertQuery_with_single_value(self):

		expectedQuery = "insert into test(row) values('5');"
		sql = self.queryMaker.makeInsertQuery({"row":5})
		self.assertEqual(expectedQuery,sql)

	def test_makeInsertQuery_with_multiple_values(self):

		expectedQuery = "insert into test(row1,row2,row3) values('5','5','5');"
		sql = self.queryMaker.makeInsertQuery({"row1":5,"row2":5,"row3":5})
		self.assertEqual(expectedQuery,sql)

	def test_makeDeleteQuery_with_single_condition(self):

		expectedQuery = "delete from test where id='5';"
		sql = self.queryMaker.makeDeleteQuery({"id":"5"})
		self.assertEqual(expectedQuery,sql)

	def test_makeDeleteQuery_with_multiple_conditions(self):

		expectedQuery = "delete from test where id='5' and v='1';"
		sql = self.queryMaker.makeDeleteQuery({"id":"5","v":"1"})
		self.assertEqual(expectedQuery,sql)

	def test_makeUpdateQuery_with_single_data_value_and_single_condition(self):

		expectedQuery = "update test set v='5' where id='5';"
		sql = self.queryMaker.makeUpdateQuery({"v":"5"},{"id":"5"})
		self.assertEqual(expectedQuery,sql)

	def test_makeUpdateQuery_with_multiple_data_values_and_multiple_conditions(self):

		expectedQuery = "update test set v='5',c='5' where id='5' and v='2';"
		sql = self.queryMaker.makeUpdateQuery({"v":"5","c":"5"},{"id":"5","v":"2"})
		self.assertEqual(expectedQuery,sql)

	def test_makeSearchQuery_with_single_value_condition(self):

		expectedQuery = "select * from test where id='5';"
		sql = self.queryMaker.makeSearchQuery({"id":"5"})
		self.assertEqual(expectedQuery,sql)

	def test_makeSearchQuery_with_multiple_conditions(self):

		expectedQuery = "select * from test where id='5' and v='2';"
		sql = self.queryMaker.makeSearchQuery({"id":"5","v":"2"})
		self.assertEqual(expectedQuery,sql)

	def test_makeSearchQuery_with_limit(self):
		
		expectedQuery = "select * from test where id='5' limit 5;"
		sql = self.queryMaker.makeSearchQuery({"id":"5"},limit=5)
		self.assertEqual(expectedQuery,sql)

	def test_makeSearQuery_raises_when_desc_is_set_to_True_without_giving_orderBy_list(self):

		with self.assertRaises(Exception):
			self.queryMaker.makeSearchQuery({"id":"5"},desc=True)

	def test_makeSearchQyery_with_orderBy_list(self):

		expectedQuery = "select * from test where id='5' order by s,n;"
		sql = self.queryMaker.makeSearchQuery({"id":"5"},orderBy=["s","n"])
		self.assertEqual(expectedQuery,sql)

	def test_makeSearchQuery_with_orderBy_list_and_desc_is_set_to_True(self):

		expectedQuery = "select * from test where id='5' order by s,f desc;"
		sql = self.queryMaker.makeSearchQuery({"id":"5"},orderBy=["s","f"],desc=True)
		self.assertEqual(expectedQuery,sql)
