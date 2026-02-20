from typing import Dict, List, Optional
import re

# LeetCode-style practice questions bank
PRACTICE_QUESTIONS = {
    "easy": [
        {
            "id": 1,
            "title": "Two Sum",
            "difficulty": "Easy",
            "description": """Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

**Example 1:**
```
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
```

**Example 2:**
```
Input: nums = [3,2,4], target = 6
Output: [1,2]
```

**Example 3:**
```
Input: nums = [3,3], target = 6
Output: [0,1]
```""",
            "starter_code": """def twoSum(nums, target):
    # Write your solution here
    pass

# Test your solution
print(twoSum([2,7,11,15], 9))  # Expected: [0, 1]
print(twoSum([3,2,4], 6))      # Expected: [1, 2]
print(twoSum([3,3], 6))        # Expected: [0, 1]""",
            "solution": """def twoSum(nums, target):
    # Use a hash map to store complements
    num_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    return []

# Time Complexity: O(n)
# Space Complexity: O(n)""",
            "hints": [
                "Think about what value you need to find for each number",
                "Can you use a hash map to store numbers you've seen?",
                "For each number, check if (target - number) exists in the map"
            ],
            "test_cases": [
                {"input": {"nums": [2,7,11,15], "target": 9}, "expected": [0, 1]},
                {"input": {"nums": [3,2,4], "target": 6}, "expected": [1, 2]},
                {"input": {"nums": [3,3], "target": 6}, "expected": [0, 1]}
            ],
            "topics": ["Array", "Hash Table"]
        },
        {
            "id": 2,
            "title": "Palindrome Number",
            "difficulty": "Easy",
            "description": """Given an integer `x`, return `true` if `x` is a palindrome, and `false` otherwise.

An integer is a palindrome when it reads the same backward as forward.

**Example 1:**
```
Input: x = 121
Output: true
Explanation: 121 reads as 121 from left to right and from right to left.
```

**Example 2:**
```
Input: x = -121
Output: false
Explanation: From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.
```

**Example 3:**
```
Input: x = 10
Output: false
Explanation: Reads 01 from right to left. Therefore it is not a palindrome.
```""",
            "starter_code": """def isPalindrome(x):
    # Write your solution here
    pass

# Test your solution
print(isPalindrome(121))   # Expected: True
print(isPalindrome(-121))  # Expected: False
print(isPalindrome(10))    # Expected: False""",
            "solution": """def isPalindrome(x):
    # Negative numbers are not palindromes
    if x < 0:
        return False
    
    # Convert to string and compare with reverse
    return str(x) == str(x)[::-1]

# Alternative solution without string conversion:
def isPalindromeNumeric(x):
    if x < 0 or (x % 10 == 0 and x != 0):
        return False
    
    reversed_half = 0
    while x > reversed_half:
        reversed_half = reversed_half * 10 + x % 10
        x //= 10
    
    return x == reversed_half or x == reversed_half // 10

# Time Complexity: O(log n)
# Space Complexity: O(1)""",
            "hints": [
                "Negative numbers cannot be palindromes",
                "You can convert to string and compare with its reverse",
                "Or reverse half of the number and compare"
            ],
            "test_cases": [
                {"input": {"x": 121}, "expected": True},
                {"input": {"x": -121}, "expected": False},
                {"input": {"x": 10}, "expected": False},
                {"input": {"x": 12321}, "expected": True}
            ],
            "topics": ["Math"]
        },
        {
            "id": 3,
            "title": "Valid Parentheses",
            "difficulty": "Easy",
            "description": """Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

**Example 1:**
```
Input: s = "()"
Output: true
```

**Example 2:**
```
Input: s = "()[]{}"
Output: true
```

**Example 3:**
```
Input: s = "(]"
Output: false
```""",
            "starter_code": """def isValid(s):
    # Write your solution here
    pass

# Test your solution
print(isValid("()"))      # Expected: True
print(isValid("()[]{}"))  # Expected: True
print(isValid("(]"))      # Expected: False""",
            "solution": """def isValid(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            # It's a closing bracket
            if not stack or stack[-1] != mapping[char]:
                return False
            stack.pop()
        else:
            # It's an opening bracket
            stack.append(char)
    
    return len(stack) == 0

# Time Complexity: O(n)
# Space Complexity: O(n)""",
            "hints": [
                "Use a stack data structure",
                "Push opening brackets onto the stack",
                "For closing brackets, check if it matches the top of stack"
            ],
            "test_cases": [
                {"input": {"s": "()"}, "expected": True},
                {"input": {"s": "()[]{}"}, "expected": True},
                {"input": {"s": "(]"}, "expected": False},
                {"input": {"s": "([)]"}, "expected": False},
                {"input": {"s": "{[]}"}, "expected": True}
            ],
            "topics": ["String", "Stack"]
        },
        {
            "id": 4,
            "title": "Reverse String",
            "difficulty": "Easy",
            "description": """Write a function that reverses a string. The input string is given as an array of characters `s`.

You must do this by modifying the input array in-place with O(1) extra memory.

**Example 1:**
```
Input: s = ["h","e","l","l","o"]
Output: ["o","l","l","e","h"]
```

**Example 2:**
```
Input: s = ["H","a","n","n","a","h"]
Output: ["h","a","n","n","a","H"]
```""",
            "starter_code": """def reverseString(s):
    # Write your solution here - modify s in-place
    pass

# Test your solution
s1 = ["h","e","l","l","o"]
reverseString(s1)
print(s1)  # Expected: ["o","l","l","e","h"]

s2 = ["H","a","n","n","a","h"]
reverseString(s2)
print(s2)  # Expected: ["h","a","n","n","a","H"]""",
            "solution": """def reverseString(s):
    # Two pointer approach
    left, right = 0, len(s) - 1
    
    while left < right:
        # Swap characters
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1
    
    # No return needed - modified in-place

# Time Complexity: O(n)
# Space Complexity: O(1)""",
            "hints": [
                "Use two pointers - one at start, one at end",
                "Swap characters at both pointers",
                "Move pointers towards the center"
            ],
            "test_cases": [
                {"input": {"s": ["h","e","l","l","o"]}, "expected": ["o","l","l","e","h"]},
                {"input": {"s": ["H","a","n","n","a","h"]}, "expected": ["h","a","n","n","a","H"]}
            ],
            "topics": ["Two Pointers", "String"]
        },
        {
            "id": 5,
            "title": "FizzBuzz",
            "difficulty": "Easy",
            "description": """Given an integer `n`, return a string array `answer` (1-indexed) where:

- `answer[i] == "FizzBuzz"` if `i` is divisible by 3 and 5.
- `answer[i] == "Fizz"` if `i` is divisible by 3.
- `answer[i] == "Buzz"` if `i` is divisible by 5.
- `answer[i] == i` (as a string) if none of the above conditions are true.

**Example 1:**
```
Input: n = 3
Output: ["1","2","Fizz"]
```

**Example 2:**
```
Input: n = 5
Output: ["1","2","Fizz","4","Buzz"]
```

**Example 3:**
```
Input: n = 15
Output: ["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz","11","Fizz","13","14","FizzBuzz"]
```""",
            "starter_code": """def fizzBuzz(n):
    # Write your solution here
    pass

# Test your solution
print(fizzBuzz(3))   # Expected: ["1","2","Fizz"]
print(fizzBuzz(5))   # Expected: ["1","2","Fizz","4","Buzz"]
print(fizzBuzz(15))  # Expected: ["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz","11","Fizz","13","14","FizzBuzz"]""",
            "solution": """def fizzBuzz(n):
    result = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))
    return result

# Time Complexity: O(n)
# Space Complexity: O(n) for the output""",
            "hints": [
                "Check divisibility by 15 first (both 3 and 5)",
                "Then check divisibility by 3 and 5 separately",
                "Use modulo operator % to check divisibility"
            ],
            "test_cases": [
                {"input": {"n": 3}, "expected": ["1","2","Fizz"]},
                {"input": {"n": 5}, "expected": ["1","2","Fizz","4","Buzz"]},
                {"input": {"n": 15}, "expected": ["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz","11","Fizz","13","14","FizzBuzz"]}
            ],
            "topics": ["Math", "String"]
        }
    ],
    "medium": [
        {
            "id": 6,
            "title": "Longest Substring Without Repeating Characters",
            "difficulty": "Medium",
            "description": """Given a string `s`, find the length of the longest substring without repeating characters.

**Example 1:**
```
Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.
```

**Example 2:**
```
Input: s = "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.
```

**Example 3:**
```
Input: s = "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3.
```""",
            "starter_code": """def lengthOfLongestSubstring(s):
    # Write your solution here
    pass

# Test your solution
print(lengthOfLongestSubstring("abcabcbb"))  # Expected: 3
print(lengthOfLongestSubstring("bbbbb"))     # Expected: 1
print(lengthOfLongestSubstring("pwwkew"))    # Expected: 3""",
            "solution": """def lengthOfLongestSubstring(s):
    char_index = {}  # Store last index of each character
    max_length = 0
    start = 0  # Start of current window
    
    for end, char in enumerate(s):
        if char in char_index and char_index[char] >= start:
            # Move start past the duplicate
            start = char_index[char] + 1
        
        char_index[char] = end
        max_length = max(max_length, end - start + 1)
    
    return max_length

# Time Complexity: O(n)
# Space Complexity: O(min(m, n)) where m is the charset size""",
            "hints": [
                "Use sliding window technique",
                "Keep track of character positions with a hash map",
                "When you find a duplicate, move the window start"
            ],
            "test_cases": [
                {"input": {"s": "abcabcbb"}, "expected": 3},
                {"input": {"s": "bbbbb"}, "expected": 1},
                {"input": {"s": "pwwkew"}, "expected": 3},
                {"input": {"s": ""}, "expected": 0}
            ],
            "topics": ["Hash Table", "String", "Sliding Window"]
        },
        {
            "id": 7,
            "title": "Container With Most Water",
            "difficulty": "Medium",
            "description": """You are given an integer array `height` of length `n`. There are `n` vertical lines where the two endpoints of the ith line are `(i, 0)` and `(i, height[i])`.

Find two lines that together with the x-axis form a container, such that the container contains the most water.

Return the maximum amount of water a container can store.

**Example 1:**
```
Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: The max area is between index 1 (height=8) and index 8 (height=7).
             Area = min(8,7) * (8-1) = 7 * 7 = 49
```

**Example 2:**
```
Input: height = [1,1]
Output: 1
```""",
            "starter_code": """def maxArea(height):
    # Write your solution here
    pass

# Test your solution
print(maxArea([1,8,6,2,5,4,8,3,7]))  # Expected: 49
print(maxArea([1,1]))                # Expected: 1""",
            "solution": """def maxArea(height):
    left, right = 0, len(height) - 1
    max_water = 0
    
    while left < right:
        # Calculate current area
        width = right - left
        h = min(height[left], height[right])
        max_water = max(max_water, width * h)
        
        # Move the pointer with smaller height
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_water

# Time Complexity: O(n)
# Space Complexity: O(1)""",
            "hints": [
                "Use two pointers at the start and end",
                "The area depends on the minimum height and width",
                "Move the pointer with the smaller height towards center"
            ],
            "test_cases": [
                {"input": {"height": [1,8,6,2,5,4,8,3,7]}, "expected": 49},
                {"input": {"height": [1,1]}, "expected": 1},
                {"input": {"height": [4,3,2,1,4]}, "expected": 16}
            ],
            "topics": ["Array", "Two Pointers", "Greedy"]
        },
        {
            "id": 8,
            "title": "3Sum",
            "difficulty": "Medium",
            "description": """Given an integer array `nums`, return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.

Notice that the solution set must not contain duplicate triplets.

**Example 1:**
```
Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]
```

**Example 2:**
```
Input: nums = [0,1,1]
Output: []
```

**Example 3:**
```
Input: nums = [0,0,0]
Output: [[0,0,0]]
```""",
            "starter_code": """def threeSum(nums):
    # Write your solution here
    pass

# Test your solution
print(threeSum([-1,0,1,2,-1,-4]))  # Expected: [[-1,-1,2],[-1,0,1]]
print(threeSum([0,1,1]))           # Expected: []
print(threeSum([0,0,0]))           # Expected: [[0,0,0]]""",
            "solution": """def threeSum(nums):
    nums.sort()
    result = []
    
    for i in range(len(nums) - 2):
        # Skip duplicates for first element
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        # Two pointer approach for remaining elements
        left, right = i + 1, len(nums) - 1
        
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            
            if total < 0:
                left += 1
            elif total > 0:
                right -= 1
            else:
                result.append([nums[i], nums[left], nums[right]])
                
                # Skip duplicates
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
    
    return result

# Time Complexity: O(n²)
# Space Complexity: O(log n) for sorting""",
            "hints": [
                "Sort the array first to avoid duplicates easily",
                "Fix one element and use two pointers for the other two",
                "Skip duplicate elements to avoid duplicate triplets"
            ],
            "test_cases": [
                {"input": {"nums": [-1,0,1,2,-1,-4]}, "expected": [[-1,-1,2],[-1,0,1]]},
                {"input": {"nums": [0,1,1]}, "expected": []},
                {"input": {"nums": [0,0,0]}, "expected": [[0,0,0]]}
            ],
            "topics": ["Array", "Two Pointers", "Sorting"]
        },
        {
            "id": 9,
            "title": "Binary Search",
            "difficulty": "Medium",
            "description": """Given an array of integers `nums` which is sorted in ascending order, and an integer `target`, write a function to search `target` in nums. If target exists, then return its index. Otherwise, return -1.

You must write an algorithm with O(log n) runtime complexity.

**Example 1:**
```
Input: nums = [-1,0,3,5,9,12], target = 9
Output: 4
Explanation: 9 exists in nums and its index is 4
```

**Example 2:**
```
Input: nums = [-1,0,3,5,9,12], target = 2
Output: -1
Explanation: 2 does not exist in nums so return -1
```""",
            "starter_code": """def search(nums, target):
    # Write your solution here
    pass

# Test your solution
print(search([-1,0,3,5,9,12], 9))   # Expected: 4
print(search([-1,0,3,5,9,12], 2))   # Expected: -1""",
            "solution": """def search(nums, target):
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

# Time Complexity: O(log n)
# Space Complexity: O(1)""",
            "hints": [
                "Use binary search - divide the search space in half each time",
                "Compare the middle element with target",
                "Adjust left or right boundary based on comparison"
            ],
            "test_cases": [
                {"input": {"nums": [-1,0,3,5,9,12], "target": 9}, "expected": 4},
                {"input": {"nums": [-1,0,3,5,9,12], "target": 2}, "expected": -1},
                {"input": {"nums": [5], "target": 5}, "expected": 0}
            ],
            "topics": ["Array", "Binary Search"]
        },
        {
            "id": 10,
            "title": "Merge Intervals",
            "difficulty": "Medium",
            "description": """Given an array of `intervals` where `intervals[i] = [starti, endi]`, merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.

**Example 1:**
```
Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].
```

**Example 2:**
```
Input: intervals = [[1,4],[4,5]]
Output: [[1,5]]
Explanation: Intervals [1,4] and [4,5] are considered overlapping.
```""",
            "starter_code": """def merge(intervals):
    # Write your solution here
    pass

# Test your solution
print(merge([[1,3],[2,6],[8,10],[15,18]]))  # Expected: [[1,6],[8,10],[15,18]]
print(merge([[1,4],[4,5]]))                  # Expected: [[1,5]]""",
            "solution": """def merge(intervals):
    if not intervals:
        return []
    
    # Sort by start time
    intervals.sort(key=lambda x: x[0])
    
    merged = [intervals[0]]
    
    for current in intervals[1:]:
        last = merged[-1]
        
        if current[0] <= last[1]:
            # Overlapping - extend the end
            last[1] = max(last[1], current[1])
        else:
            # Non-overlapping - add new interval
            merged.append(current)
    
    return merged

# Time Complexity: O(n log n) for sorting
# Space Complexity: O(n) for output""",
            "hints": [
                "Sort intervals by their start time first",
                "Compare each interval with the last merged interval",
                "If they overlap, extend the end time; otherwise add new interval"
            ],
            "test_cases": [
                {"input": {"intervals": [[1,3],[2,6],[8,10],[15,18]]}, "expected": [[1,6],[8,10],[15,18]]},
                {"input": {"intervals": [[1,4],[4,5]]}, "expected": [[1,5]]},
                {"input": {"intervals": [[1,4],[0,4]]}, "expected": [[0,4]]}
            ],
            "topics": ["Array", "Sorting"]
        }
    ],
    "hard": [
        {
            "id": 11,
            "title": "Median of Two Sorted Arrays",
            "difficulty": "Hard",
            "description": """Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively, return the median of the two sorted arrays.

The overall run time complexity should be O(log (m+n)).

**Example 1:**
```
Input: nums1 = [1,3], nums2 = [2]
Output: 2.00000
Explanation: merged array = [1,2,3] and median is 2.
```

**Example 2:**
```
Input: nums1 = [1,2], nums2 = [3,4]
Output: 2.50000
Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.
```""",
            "starter_code": """def findMedianSortedArrays(nums1, nums2):
    # Write your solution here
    pass

# Test your solution
print(findMedianSortedArrays([1,3], [2]))     # Expected: 2.0
print(findMedianSortedArrays([1,2], [3,4]))   # Expected: 2.5""",
            "solution": """def findMedianSortedArrays(nums1, nums2):
    # Ensure nums1 is the smaller array
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    
    m, n = len(nums1), len(nums2)
    left, right = 0, m
    
    while left <= right:
        partition1 = (left + right) // 2
        partition2 = (m + n + 1) // 2 - partition1
        
        maxLeft1 = float('-inf') if partition1 == 0 else nums1[partition1 - 1]
        minRight1 = float('inf') if partition1 == m else nums1[partition1]
        
        maxLeft2 = float('-inf') if partition2 == 0 else nums2[partition2 - 1]
        minRight2 = float('inf') if partition2 == n else nums2[partition2]
        
        if maxLeft1 <= minRight2 and maxLeft2 <= minRight1:
            # Found the correct partition
            if (m + n) % 2 == 0:
                return (max(maxLeft1, maxLeft2) + min(minRight1, minRight2)) / 2
            else:
                return float(max(maxLeft1, maxLeft2))
        elif maxLeft1 > minRight2:
            right = partition1 - 1
        else:
            left = partition1 + 1
    
    return 0.0

# Time Complexity: O(log(min(m, n)))
# Space Complexity: O(1)""",
            "hints": [
                "Use binary search on the smaller array",
                "Partition both arrays such that left elements <= right elements",
                "The median is derived from elements around the partition"
            ],
            "test_cases": [
                {"input": {"nums1": [1,3], "nums2": [2]}, "expected": 2.0},
                {"input": {"nums1": [1,2], "nums2": [3,4]}, "expected": 2.5},
                {"input": {"nums1": [], "nums2": [1]}, "expected": 1.0}
            ],
            "topics": ["Array", "Binary Search", "Divide and Conquer"]
        },
        {
            "id": 12,
            "title": "Trapping Rain Water",
            "difficulty": "Hard",
            "description": """Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

**Example 1:**
```
Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
Explanation: The elevation map [0,1,0,2,1,0,1,3,2,1,2,1] can trap 6 units of rain water.
```

**Example 2:**
```
Input: height = [4,2,0,3,2,5]
Output: 9
```""",
            "starter_code": """def trap(height):
    # Write your solution here
    pass

# Test your solution
print(trap([0,1,0,2,1,0,1,3,2,1,2,1]))  # Expected: 6
print(trap([4,2,0,3,2,5]))              # Expected: 9""",
            "solution": """def trap(height):
    if not height:
        return 0
    
    left, right = 0, len(height) - 1
    left_max, right_max = 0, 0
    water = 0
    
    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1
    
    return water

# Time Complexity: O(n)
# Space Complexity: O(1)""",
            "hints": [
                "Water at each position = min(max_left, max_right) - height",
                "Use two pointers from both ends",
                "Track the maximum height seen from each side"
            ],
            "test_cases": [
                {"input": {"height": [0,1,0,2,1,0,1,3,2,1,2,1]}, "expected": 6},
                {"input": {"height": [4,2,0,3,2,5]}, "expected": 9},
                {"input": {"height": [1,2,1]}, "expected": 0}
            ],
            "topics": ["Array", "Two Pointers", "Stack", "Dynamic Programming"]
        }
    ]
}


def get_all_questions() -> List[Dict]:
    """Get all practice questions."""
    all_questions = []
    for difficulty in ["easy", "medium", "hard"]:
        for q in PRACTICE_QUESTIONS[difficulty]:
            all_questions.append({
                "id": q["id"],
                "title": q["title"],
                "difficulty": q["difficulty"],
                "topics": q["topics"]
            })
    return all_questions


def get_question_by_id(question_id: int) -> Optional[Dict]:
    """Get a specific question by ID."""
    for difficulty in ["easy", "medium", "hard"]:
        for q in PRACTICE_QUESTIONS[difficulty]:
            if q["id"] == question_id:
                return q
    return None


def get_questions_by_difficulty(difficulty: str) -> List[Dict]:
    """Get questions by difficulty level."""
    return PRACTICE_QUESTIONS.get(difficulty.lower(), [])


def get_hint(question_id: int, hint_index: int) -> Optional[str]:
    """Get a specific hint for a question."""
    question = get_question_by_id(question_id)
    if question and 0 <= hint_index < len(question["hints"]):
        return question["hints"][hint_index]
    return None


def check_solution(question_id: int, user_output: str) -> Dict:
    """
    Basic solution checker - compares user output format.
    In a real implementation, this would execute the code safely.
    """
    question = get_question_by_id(question_id)
    if not question:
        return {"correct": False, "message": "Question not found"}
    
    # For now, return the solution with explanation
    return {
        "correct": False,  # Would need code execution to verify
        "solution": question["solution"],
        "hints": question["hints"],
        "test_cases": question["test_cases"]
    }
