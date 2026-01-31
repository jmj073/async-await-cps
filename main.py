class Future:
    def __init__(self):
        self.__callbacks = []
        self.__resolved = False
        self.__value = None

    def then(self, k):
        if self.is_resolved():
            k(self.__value)
        else:
            self.__callbacks.append(k)

        return self

    def resolve(self, v):
        if self.is_resolved():
            return
        self.__resolved = True
        self.__value = v

        for k in self.__callbacks:
            k(v)

        return self

    def is_resolved(self):
        return self.__resolved


def my_async(func):
    def async_func(*args):
        fut = Future()
        func(*args, fut.resolve)
        return fut
    return async_func

def my_await(fut, k):
    fut.then(k)


input_fut = Future()
def my_input():
    return input_fut

"""
async foo(greet):
    print("enter!")
    v = await my_input()
    print("await!")
    return f"{greet}, {v}"
"""
@my_async
def foo(greet, k):
    print("enter!")
    def k1(v):
        print("await!")
        return k(f"{greet}, {v}")
    return my_await(my_input(), k1)

"""
async fac(n):
    print("enter!", n)
    if n == 0:
        return 1
    v = await fac(n - 1)
    print("await!", n)
    return n * v
"""
@my_async
def fac(n, k):
    print("enter!", n)
    if n == 0:
        return k(1)
    def k1(v):
        print("await!", n)
        return k(n * v)
    return my_await(fac(n - 1), k1)

if __name__ == "__main__":
    fut = foo("Hello")

    fut.then(lambda v: print("resolved!", v))
    print("resolved: ", fut.is_resolved())
    print("resolve input")
    input_fut.resolve("world")
    print("resolved: ", fut.is_resolved())

    print("-" * 50)

    fut = fac(5)
    fut.then(lambda v: print("resolved!", v))