class Segregation:
    def __init__(self, k, m, n):
        self._k = k
        self._m = m
        self._n = n
        self._t = self._k + self._m + self._n
        self._probability = {'AA': 0, 'Aa': 0, 'aa': 0}
        self._segregation_()

    def _segregation_(self):
        self._probability['AA'] = (self._k * self._k - self._k + self._k * self._m +
                                   0.25 * self._m * self._m - 0.25 * self._m) / (self._t * self._t - self._t)
        self._probability['Aa'] = (
                                              0.5 * self._m * self._m - 0.5 * self._m + self._k * self._m + 2 * self._k * self._n + self._m * self._n) /\
                                  (self._t * self._t - self._t)
        self._probability['aa'] = (self._n * self._n - self._n + self._m * self._n +
                                   0.25 * self._m * self._m - 0.25 * self._m) / (self._t * self._t - self._t)

    def get_probability(self):
        return self._probability


if __name__ == '__main__':
    seg = Segregation(2, 0, 2)
    print(seg.get_probability())
