'''
Author: kuanwei
Data: 2017/12/14
Descipbe: Simple unittest
'''

class Calculator():

	def __init__(self, a, b):
		self.a = int(a)
		self.b = int(b)

	def add(self):
		return self.a + self.b

	def sub(self):
		return self.a - self.b

	def mul(self):
		return self.a * self.b

	def div(self):
		return self.a / self.b