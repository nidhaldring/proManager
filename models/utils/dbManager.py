
import pymysql

from config import CONFIG

class DbManager:

	def __init__(self):

		self.connectionSettings = dict(
								db=CONFIG.DB_NAME,
								user=CONFIG.DB_USER,
								password=CONFIG.DB_PASSWORD,
								host=CONFIG.DB_HOST
							)

	def execute(self,sql):
		'''
		executes the given sql
		returning the result or none if none
		'''

		conn = pymysql.connect(**self.connectionSettings)
		cursor = conn.cursor()

		cursor.execute(sql)
		res = cursor.fetchall()

		conn.commit()
		conn.close()

		return res
