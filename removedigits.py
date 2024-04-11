class Solution(object):
    def removeKdigits(self, num, k):
        """
        :type num: str
        :type k: int
        :rtype: str
        """
        if k == len(num): return ""
        arrnum = [x for x in num]
        int_arrnum = [(int(n)*(len(num)-i-1),num[i],i) for i,n in enumerate(num)]
        int_arrnum.sort(reverse=True)
       
        print(int_arrnum)

        for el in range(k):
            arrnum.pop(int_arrnum[0][2])
        return "".join(arrnum)


x = Solution()

print(x.removeKdigits("1432219",3))
