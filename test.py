from typing import Counter


myDict = Counter({4: 949, 3: 944, 5: 233, 2: 131, 6: 43, 7: 14, 1: 1})
import collections as c

air = c.OrderedDict(sorted(myDict.items()))
print(air)