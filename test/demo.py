from contextlib import AbstractContextManager, ContextDecorator


class content(object):
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

class content2(ContextDecorator):

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(exc_type, exc_val, exc_tb)
        return False




@content2()
def function():
    print(1//2)

# with open("s.", 'rb') as e:
#     e.read()

# try:
#     function()
# except Exception as e:
#     print(e)
# finally:
#     print("结束")
function()
# with content2():
#     function()

# print(123)
