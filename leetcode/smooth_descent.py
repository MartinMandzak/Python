from typing import List, Optional, Deque, DefaultDict
import copy

class Solution:
    def getDescentPeriods(self, prices: List[int]) -> int:
        x,i, i_temp = 0,1,1
        while i != len(prices):
            x+=1
            i+=1
            i_old = i
            if prices[i-1] - prices[i] == 1:
                print("got here", i)
                print(prices[i])
                x+=1
                i_temp = copy.deepcopy(i)
                if i - 2 >=0:
                    print("got here too", i_temp)
                    i -= 2
            if i_old == i and i+2 < len(prices):
                print("final")
                i = copy.deepcopy(i_temp) + 2
                print(i)
            else: break
        return x


# main

main = Solution()
x = main.getDescentPeriods([3,2,1,4])
print('answer',x)
