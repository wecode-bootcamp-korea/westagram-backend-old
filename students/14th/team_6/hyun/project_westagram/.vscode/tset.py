# * 문제
# 숫자로 이루어진 배열인 nums를 인자로 전달합니다.
# 숫자중에서 과반수(majority, more than a half)가 넘은 숫자를 반환해주세요.
# 예를 들어,
# nums = [3,2,3]
# return 3
# nums = [2,2,1,1,1,2,2]    2 : 
# return 2
# * 가정
# nums 배열의 길이는 무조건 2개 이상
from collections import Counter


def majority(nums) :
    count = Counter(nums)
    print (count)
    lenth = len(nums)
    for i , j in count.items() :
        if j 

        
    
            
            #  제일 높은 벨류 출력
             # 1 ~ 7 / 2
                    # 4,  3



print(majority([2,2,1,1,1,2,2]))