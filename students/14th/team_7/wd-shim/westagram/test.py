import sys

# for key, value in sys.modules.items():
#     print(key, end="")
#     print(value, end="")
#     print()

# def roman_to_num(s):
#     if not s:
#         return 0
#     # - roman_dic[s[index + 1]]
#     roman_key = ("I", "V", "X", "L", "C", "D", "M")
#     roman_val = (1, 5, 10, 50, 100, 500, 1000)
#     roman_dic = dict(zip(roman_key, roman_val))
#     result = 0
#
#     for index in range(len(s)):
#         if index < len(s)-1 and roman_dic[s[index]] > roman_dic[s[index+1]]:
#             result += roman_dic[s[index]]
#         else:
#             result += roman_dic[s[index]]
#
#     return result

# print(roman_to_num("CCCXXXIII"))

# def num_to_roman(num):
#     roman_key = (1, 5, 10, 50, 100, 500, 1000)
#     roman_val = ("I", "V", "X", "L", "C", "D", "M")
#     roman_dic = dict(zip(roman_key, roman_val))
#     temp_num = num
#     result = ""
    
    # while True:
    #     for val in roman_key:
    #         if num < val:
    #             pass

# print(num_to_roman(800))

# 코드카타 2주차 1
# def roman_to_num(s):
#     if not s:
#         return 0
#     roman_key = ("I", "V", "X", "L", "C", "D", "M")
#     roman_val = (1, 5, 10, 50, 100, 500, 1000)
#     roman_dic = dict(zip(roman_key, roman_val))
#     result = 0
#     temp = s
#     while temp:
#         count = 0
#         if count < len(temp)-1 and roman_dic[temp[count]] < \
#             roman_dic[temp[count+1]]:
#             result += roman_dic[temp[count+1]] - roman_dic[temp[count]]
#             temp = temp[count+2:]
#         else:
#             result += roman_dic[temp[count]]
#             temp = temp[count+1:]
#
#     return result
#
# print(roman_to_num("CM"))

# def get_majority(nums):
#     c = int(len(nums) / 2) + 1
#
#     for i in nums:
#         if nums.count(i) >= c:
#             return i
#
# print(get_majority([0,1,2,3,0,0,0,0]))


# def is_valid(string):
#     if not string or len(string) == 1:
#         return False
#
#     a_dic = {"(": 1, "[": 1, "{": 1, ")": 0, "]": 0, "}": 0}
#     b_dic = {")": "(", "}": "{", "]": "["}
#     temp = []
#
#     for index in range(len(string)):
#         if index == 0 and a_dic[string[index]] == 0:
#             return False
#
#         if a_dic[string[index]] != 0:
#             temp.append(string[index])
#         else:
#             if temp[-1] != b_dic[string[index]]:
#                 return False
#             else:
#                 temp.pop()
#
#     return True
#
# print(is_valid("()[]{}"))


"""
#코드타카 10일차
nums는 숫자로 이루어진 배열이다.
가장 자주 등장한 숫자를 k 개수만큼 return 해라.

nums = [1,1,1,2,2,3],
k = 2
return [1,2]
"""
# from collections import Counter
# def top_k(nums, k):
#     cnt = Counter(nums)
#     top = cnt.most_common()
#     result = []
#     for n in range(k):
#         result.append(top[n][0])
#
#     return result
#
# nums = [1, 1, 1, 2, 2, 3]
# k = 2
# top_k(nums, k)

"""
모델 솔루션
"""
# def top_k(nums, k):
#     # for n in nums:
#     #     count[n] = count.get(n, 0) + 1
#     bucket = [[] for _ in range(len(nums)+1)]
#
#     # for n, freq in count.items():
#     #     bucket[freq].append(n)
#     #
#     # ret = []
#     # for n_list in bucket[::-1]:
#     #     if n_list:
#     #         ret.extend(n_list)
#     #         if len(ret) == k:
#     #             return ret
#
# nums = [1, 1, 1, 2, 2, 3]
# k = 2
# top_k(nums, k)

# class MAC:
#     name = "swd"
#
#     def __init__(self):
#         print(self.name)
#
# a = MAC()
# a.age = 12
#
# print(a.age)
#
# b = MAC()
# print(b.name)

import re
REGEX_EMAIL   = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

def is_valid_email(email):
    return re.search(REGEX_EMAIL, email)

if is_valid_email("alsdfj@test.com"):
    print("1")
else:
    print("2")


