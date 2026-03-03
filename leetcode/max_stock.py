from typing import List
from math import floor
class Node:
    def __init__(self, val: int, pres: int, fut: int):
        self.val = val
        self.pres = pres
        self.fut = fut
        self.visited = False
        self.children: List['Node'] = []

class Solution:
    def maxProfit(self, n: int, present: List[int], future: List[int], hierarchy: List[List[int]], budget: int) -> int:
        max_profit=0
        '''
        quick conversion to a tree
        '''
        nodes = {}
        for parent,child in hierarchy:
            if parent not in nodes:nodes[parent] = Node(parent, present[parent-1], future[parent-1])
            if child not in nodes:nodes[child] = Node(child, present[child-1], future[child-1])
            nodes[parent].children.append(nodes[child])

        cost = 0
        profit = 0
        for node in nodes.values():
            while cost <= budget and not node.visited:
                print(f"node: {node.val} w/ cost {cost}")

                cost += node.pres
                profit += node.fut
                node.visited = True
                node.children.sort(key=lambda child: child.fut - floor(child.pres/2), reverse = True)
                for child in node.children:
                    if cost + floor(child.pres/2) <= budget:
                        cost+=floor(child.pres/2)
                        print(cost)
                        profit+=child.fut
                        if max_profit < profit-cost:max_profit = profit-cost

        return max_profit


main = Solution()
n = 3
'''
present = [5,2,3]
future = [8,5,6]
hierarchy = [[1,2], [2,3]]
budget = 7
'''
present = [4,6,8]
future=[7,9,11]
hierarchy=[[1,2],[1,3]]
budget = 10
print(main.maxProfit(n, present, future, hierarchy, budget))
