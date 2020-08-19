import inspect

def foo(param=None):
    print("my param is", param)

param = 'test'
foo(param) if param else foo()