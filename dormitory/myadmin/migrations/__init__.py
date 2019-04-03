class A(object):

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        pass


a = A()
print(id(a))
b = A()
print(id(b))