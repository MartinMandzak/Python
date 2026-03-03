from typing import List

class Solution:           
    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        
        def minsum(arr: List[int]) -> int:
            if not arr:
                    return 0
                
            min_val = min(arr)
            min_idx = arr.index(min_val)
            
            current_area = min_val * len(arr)
            
            left_area = minsum(arr[:min_idx])
            right_area = minsum(arr[min_idx + 1:])
            
            return max(current_area, left_area, right_area)

        final = [int(el) for el in matrix[0]]
        res = minsum(final)
        for row in range(1,len(matrix)):
            for col in range(len(final)):
                if matrix[row][col] == '1':
                    final[col]+=1
                else:
                    final[col]=0
            if minsum(final) > res:
                res = minsum(final)
        return res


main = Solution()
matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]
print(main.maximalRectangle(matrix))
