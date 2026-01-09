from typing import List

class Solution:
    def generateMatrix(self, n: int) -> List[List[int]]:
        res = [[0 for el in range(n)] for row in range(n)]

        vector_r = (0,1,0,-1)
        vector_c = (1,0,-1,0)

        row, col, direction_idx = 0, 0, 0
        for i in range(1,n**2+1):
            
            res[row][col]=i

            next_r = row + vector_r[direction_idx]
            next_c = col + vector_c[direction_idx]

            if not (0<=next_r<n and 0<=next_c<n and res[next_r][next_c] == 0):
                direction_idx = (direction_idx + 1) % 4 # takes care of 5
                next_r = row + vector_r[direction_idx]
                next_c = col + vector_c[direction_idx]

            row,col = next_r,next_c


        return res




main = Solution()

print(main.generateMatrix(3))
