
"""
author: Zhengjian Kang
date: 03/22/2021

残酷群每日一题: 03/22/2021; 05/04/2021

https://leetcode.com/problems/maximum-xor-with-an-element-from-array/

1707. Maximum XOR With an Element From Array

note: xor + trie
offline querying的系列题目, 使用TrieNode可能会超时，所以可以使用native dictionary {}来代替

You are given an array nums consisting of non-negative integers.
You are also given a queries array, where queries[i] = [xi, mi].

The answer to the ith query is the maximum bitwise XOR value of xi and any
element of nums that does not exceed mi. In other words, the answer is 
max(nums[j] XOR xi) for all j such that nums[j] <= mi. If all elements in 
nums are larger than mi, then the answer is -1.

Return an integer array answer where answer.length == queries.length and 
answer[i] is the answer to the ith query.

Example 1:
Input: nums = [0,1,2,3,4], queries = [[3,1],[1,3],[5,6]]
Output: [3,3,7]
Explanation:
1) 0 and 1 are the only two integers not greater than 1. 0 XOR 3 = 3 and
1 XOR 3 = 2. The larger of the two is 3.
2) 1 XOR 2 = 3.
3) 5 XOR 2 = 7.

Example 2:
Input: nums = [5,2,4,6,6,3], queries = [[12,4],[8,1],[6,3]]
Output: [15,-1,5]

Constraints:
1 <= nums.length, queries.length <= 10^5
queries[i].length == 2
0 <= nums[j], xi, mi <= 10^9
"""


class TrieNode:
    def __init__(self):
        self.children = [None] * 2  # [0, 1]
        self.val = None


class Solution:
    def maximizeXor(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        nums.sort()
        n = len(queries)
        for idx, q in enumerate(queries):
            q.append(idx)
        res = [None] * n
        queries.sort(key=lambda x: x[1])
        root = TrieNode()
        idx = 0
        #O(q + n)
        for q in queries:  # O(32q)
            x, m, pos = q
            while idx < len(nums) and nums[idx] <= m:  # O(32n)
                self.add_node(root, nums[idx])
                idx += 1
            if idx == 0:
                res[pos] = -1
                continue
            res[pos] = self.find_max(root, x)  # O(1)
        return res

    def add_node(self, root, n):
        node = root
        for i in range(31, -1, -1):
            bit = ((n >> i) & 1)
            if node.children[bit] is None:
                node.children[bit] = TrieNode()
            node = node.children[bit]
        node.val = n

    def find_max(self, root, n):
        node = root
        for i in range(31, -1, -1):
            bit = ((n >> i) & 1)
            search_bit = bit
            if node.children[1-bit]:
                search_bit = 1-bit
            node = node.children[search_bit]
        max_xor_num = node.val

        return n ^ max_xor_num
