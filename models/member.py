
from models.model import Model
from models.exceptions import *


class Member(Model):

	# id_ should only be set internally
	def __init__(self,name,surname,phone,birthdate,_id=None):
		if not self.table or not self.dbManager or not self.queryMaker:
			raise ModelMissingConstructorArgumentException()

		data = dict(name=name,surname=surname,phone=phone,birthdate=birthdate)
		super().__init__(data=data,_id=_id)

	@classmethod
	def initWithDefaults(cls):
		from config import CONFIG
		Model.initWithDefaults(CONFIG.MEMBERS_TABLE_NAME)

	@classmethod
	def query(cls,cond:dict,*,limit=None,desc=False,orderBy=[]) -> list:
		return [
			cls(row[1],row[2],row[3],row[4],_id=row[0])
			for row in cls._search(cond,limit=limit,desc=desc,orderBy=orderBy)
		]

	def __repr__(self) -> str:
		return f"{self.username} [{self._id}]"
