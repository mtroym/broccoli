class BaseOp(object):
    def __init__(self, name) -> None:
        self.name = name
        pass

    def before(self):
        raise NotImplementedError()
    
    def run(self):
        raise NotImplementedError()
    
    def after(self):
        raise NotImplementedError()
    
    def __call__(self):
        self.before()
        self.run()
        self.after()

class ExampleOp(BaseOp):
    def __init__(self, name) -> None:
        super().__init__(name)

    def before(self):
        print("before call, will check pre-requisite")

    def run(self):
        print("executing op")

    def after(self):
        print("after call, store state")

if __name__ == "__main__":
    op = ExampleOp("example")
    op()