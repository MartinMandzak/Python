from typing import List, Optional, Deque, DefaultDict
import math

class Solution:
    def getDescentPeriods(self, prices: List[int]) -> int:
        f,x=1,0
        
        for i in range(1,len(prices)):
            if prices[i-1] - prices[i] == 1:
                f+=1
            else:
                x+=f*(f+1)*0.5;f=1
        x+=f*(f+1)*0.5

        return int(x)


# main

main = Solution()
x = main.getDescentPeriods([3,2,1,4])
print('answer',x)
y = main.getDescentPeriods([12,11,10,9,8,7,6,5,4,3,4,3,10,9,8,7])
print('answer', y)
