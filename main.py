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

    def is_resolved(self):
        return self.__resolved


def my_async(func, *args):
    fut = Future()
    func(*args, fut.resolve)
    return fut

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
def foo(greet, k):
    print("enter!")
    def k1(v):
        print("await!")
        k(f"{greet}, {v}")
    my_await(my_input(), k1)

"""
async fac(n):
    print("enter!", n)
    if n == 0:
        return 1
    v = await fac(n - 1)
    print("await!", n)
    return n * v
"""
def fac(n, k):
    print("enter!", n)
    if n == 0:
        k(1)
        return
    def k1(v):
        print("await!", n)
        k(n * v)
    my_await(my_async(fac, n - 1), k1)

if __name__ == "__main__":
    fut = my_async(foo, "Hello")

    fut.then(lambda v: print("resolved!", v))
    print("resolved: ", fut.is_resolved())
    print("resolve input")
    input_fut.resolve("world")
    print("resolved: ", fut.is_resolved())

    print("-" * 50)

    fut = my_async(fac, 5)
    fut.then(lambda v: print("resolved!", v))