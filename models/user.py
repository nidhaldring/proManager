
from models.model import Model
from models.exceptions import *


class User(Model):

	# id_ should only be set internally
	def __init__(self,username,password,email,_id=None):
		if not self.table or not self.dbManager or not self.queryMaker:
			raise ModelMissingConstructorArgumentException()

		data = dict(username=username,password=password,email=email)
		super().__init__(data=data,_id=_id)

	@classmethod
	def initWithDefaults(cls):
		from config import CONFIG
		Model.initWithDefaults(CONFIG.USERS_TABLE_NAME)

	@classmethod
	def query(cls,cond:dict,*,limit=None,desc=False,orderBy=[]) -> list:
		return [
			cls(row[1],row[2],row[3],_id=row[0])
			for row in cls._search(cond,limit=limit,desc=desc,orderBy=orderBy)
		]

	def __repr__(self) -> str:
		return f"{self.username} [{self._id}]"
