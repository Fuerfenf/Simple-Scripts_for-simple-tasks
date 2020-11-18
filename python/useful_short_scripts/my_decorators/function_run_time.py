import functools
import time


class RuntimeFunctionDecorator:
    """
        This decorator return run time function.
        It can output result in console or file. For this used attribute output:
                                                        True - console out,
                                                        False - write to output file.
                                                              output file locate in directory where script locate
    """
    def __init__(self, output=True):
        self.output = output

    def __call__(self, func):
        @functools.wraps(func)  # use for get name and doc run function
        def inner(*args, **kwargs):
            try:                        # use this block for except variable for save func(*args, **kwargs)
                time_start = time.time()
                return func(*args, **kwargs)
            finally:
                result = "Function: {}, performed {:.2f}(ms)".format(func.__name__, 1000 * (time.time() - time_start))
                if self.output:
                    print(result)
                else:
                    with open("func_runtime_out_log.txt", "w") as file:
                        file.write(result)
        return inner


# example script run
@RuntimeFunctionDecorator()
def f(t):
    while t < 4000:
        a = t
        print(a + (a-20) * 100)
        t += 1
f(4)

