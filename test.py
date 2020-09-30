def function(nums):
    if nums==0 or nums==1:
        return nums
    return function(nums-2)+function(nums-1)
for i in range(5):
    print(function(i))