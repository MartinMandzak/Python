class Solution(object):
    def exist(self, board, word):
        arrayidx, elidx = 0,0
        while True:
    

    def find_adjacent(self, arrayidx,elidx, next_letter): # -> bool
        answer = False
        if(board[arrayidx][elidx-1] != next_letter or
           board[arrayidx][elidx+1] != next_letter or
           board[arrayidx-1][elidx] != next_letter or
           board[arrayidx+1][elidx] != next_letter):        answer = False
        return answer



#class end


board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
word = "SEE"
