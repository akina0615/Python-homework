class Fib:
    def __init__(self, tup: tuple[int, int] = (5, 3), method=1):
        self.__fib_list = []
        self.__fib_num = 0
        self.__n = tup[0]
        self.__k = tup[1]
        if method == 1:
            self.__fib_method_1__()
        elif method == 2:
            self.__fib_num = self.__fib_method_2__(self.__n - 1, self.__k)

    def __fib_method_1__(self):
        i = 0
        start_num = 1
        self.__fib_list.append(start_num)
        self.__fib_list.append(start_num)
        while i + 2 < self.__n:
            self.__fib_list.append(self.__k * self.__fib_list[i] + self.__fib_list[i + 1])
            i += 1
        self.__fib_num = self.__fib_list[-1]

    def __fib_method_2__(self, i, j):
        if i == 0 or i == 1:
            return 1
        else:
            return j * self.__fib_method_2__(i - 2, j) + self.__fib_method_2__(i - 1, j)

    @property
    def get_feb_list(self):
        return self.__fib_list

    @property
    def get_fib_num(self):
        return self.__fib_num


test = Fib((5, 3), 2)
print(test.get_fib_num)
