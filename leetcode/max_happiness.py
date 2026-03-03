from typing import List

class Solution:
    def maximumHappinessSum(self, happiness: List[int], k: int) -> int:
        sum = 0
        happiness.sort()
        for i in range(k):
            print(happiness[-1-i])
            if happiness[-1-i] - i > 0: sum += (happiness[-1-i] - i)
            else: break
        return sum



main = Solution()
arr,k = [2,3,4,5],1
print(f"Result is: {main.maximumHappinessSum(arr,k)}")
