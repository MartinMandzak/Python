from typing import List

class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:          

        res=""
        temp = sorted(strs)
        for idx in range(min(len(temp[0]),len(temp[-1]))):
            if temp[0][idx] != temp[-1][idx]: break
            res+=temp[0][idx]
        return res

main = Solution()
strs = ["flower","flow","flight"]
print(main.longestCommonPrefix(strs))
