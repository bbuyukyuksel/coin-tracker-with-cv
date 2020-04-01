def test():
    '''
    hello world
    '''
    print(test.__doc__)
    return 5

def handler_func(handler):
    print("Handler")
    handler()


handler_func(eval("test"))