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


def my_async(func):
    fut = Future()
    def k(v):
        if not isinstance(v, Future):
            fut.resolve(v)
    func(k)
    return fut

def my_await(fut, ok, ik):
    ok(fut.then(ik))


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
    my_await(my_input(), k, k1)

if __name__ == "__main__":
    fut = my_async(lambda k: foo("Hello", k))

    fut.then(lambda v: print("resolved!", v))
    print("resolved: ", fut.is_resolved())
    print("resolve input")
    input_fut.resolve("world")
    print("resolved: ", fut.is_resolved())