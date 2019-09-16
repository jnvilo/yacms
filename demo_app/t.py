class Test(object):

	@classmethod
	def cm(cls, x):
		cls.x = cls.x + 1
		print(x)

	@staticmethod
	def sm(x):
		print(x)


	x = 1

a = Test()

Test.cm(1)
Test.cm(2)
a.sm(1)

