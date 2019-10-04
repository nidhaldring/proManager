

from models.exceptions import *
import pymysql

class Model:

	'''base class for all models'''

	dbManager = None
	queryMaker = None
	table = None

	def __init__(self,data:dict,_id=None):
		self.data = data
		self._id = _id

	@property
	def id(self):
		return self._id

	@id.setter
	def id(self,v):
		raise AttributeError("Can't set id !")

	def insert(self):
		if self._id is not None:
			raise ModelAlreadyInsertedException()

		sql = self.queryMaker.makeInsertQuery(self.data)

		try:
			self.dbManager.execute(sql)
		except pymysql.err.IntegrityError as e:
			if e.args[0] == 1062:
				raise ModelUniqueConstraintException()
		# set the id
		self._id = self.dbManager.execute(f"select max(id) from {self.table};")[0][0]

		return self

	def delete(self):
		if self._id is None:
			raise ModelNotInsertedException()

		sql = self.queryMaker.makeDeleteQuery({"id":self.id})
		self.dbManager.execute(sql)
		self._id = None

		return self


	def update(self,newData:dict):
		if self._id is None:
			raise ModelNotInsertedException()

		# update the current object
		self.__dict__.update(newData)

		sql = self.queryMaker.makeUpdateQuery(newData,{"id":self.id})

		try:
			self.dbManager.execute(sql)
		except pymysql.err.IntegrityError as e:
			if e.args[0] == 1062:
				raise ModelUniqueConstraintException()

		return self

	def __getattr__(self,key):
		return self.data[key]

	def __eq__(self,other):
		return self.data == other.data and self.id == other.id

	@classmethod
	def _search(cls,cond:dict,limit,desc,orderBy):
		return cls.dbManager.execute(cls.queryMaker.makeSearchQuery(cond,limit=limit,orderBy=orderBy,desc=desc))

	@classmethod
	def initWithDefaults(cls,table):
		if cls.dbManager and cls.table and cls.queryMaker:
			return

		from models.utils.dbManager import DbManager
		from models.utils.sqlQueryMaker import SQLQueryMaker

		cls.dbManager = DbManager()
		cls.queryMaker = SQLQueryMaker(table=table)
		cls.table = table
