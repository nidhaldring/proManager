

class SQLQueryMaker:

	def __init__(self,table):
		self.table = table

	def makeInsertQuery(self,data:dict) -> str:
		sql = f"insert into {self.table}"
		sql += f"({','.join(data.keys())})"
		sql += " values(" + ",".join([f"'{i}'" for i in data.values()]) + ");"

		return sql

	def makeDeleteQuery(self,cond) -> str:
		return f"delete from {self.table} where {self._createCond(cond)};"

	def makeUpdateQuery(self,data:dict,cond:dict) -> str:
		cond = self._createCond(cond)
		sql = f"update {self.table} set "
		sql +=  ",".join(["{}='{}'".format(i,j) for i,j in data.items()])
		sql += f" where {cond};"

		return sql

	def makeSearchQuery(self,cond:dict,orderBy=[],limit=None,desc=False) -> str:
		if desc and not orderBy:
			raise Exception("desc can't be set true when no orderBy list is given")

		limit = f" limit {limit}" if limit else ""
		order = f" order by {','.join(orderBy)}" if orderBy else ""
		order += " desc" if desc else ""
		return f"select * from {self.table} where {self._createCond(cond)}{limit}{order};"

	def _createCond(self,cond:dict):
		'''returns the conditional part of sql statement - where'''
		return " and ".join(["{}='{}'".format(i,j) for i,j in cond.items()])
