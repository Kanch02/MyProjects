# def remove_zero_sum_subsets(nums):
#     indices_to_remove = set()
#     for i in range(len(nums)):
#         found = False
#         if i not in indices_to_remove:
#             for j in range(i+1, len(nums)):
#                 if j not in indices_to_remove:
#                     curr_sum = nums[i] + nums[j]
#                     if int(curr_sum) == 0:
#                         indices_to_remove.add(i)
#                         indices_to_remove.add(j)
#                         found = True
#                         break
#                     else:
#                         for k in range(j+1, len(nums)):
#                             curr_sum += nums[k]
#                             if int(curr_sum) == 0:
#                                 indices_to_remove.add(i)
#                                 indices_to_remove.add(j)
#                                 indices_to_remove.add(k)
#                                 found = True
#                                 break
#                 if found:
#                     break
#         else:
#             continue

#     print("Numbers to Remove:")
#     for index in indices_to_remove:
#         print(nums[index])

#     print("Numbers after Removal:")
#     for index in range(len(nums)):
#         if(index not in indices_to_remove):
#             print(nums[index])

# def remove_zero_sum_subsets(nums, tolerance=0.9):
#     def find_zero_sum_subset(nums, start, curr_subset):
#         if abs(sum(curr_subset)) <= tolerance and len(curr_subset) > 1:
#             return curr_subset
#         if start >= len(nums):
#             return None
        
#         # Include the current element and recurse
#         with_curr = find_zero_sum_subset(nums, start + 1, curr_subset + [nums[start]])
#         if with_curr:
#             return with_curr
        
#         # Exclude the current element and recurse
#         return find_zero_sum_subset(nums, start + 1, curr_subset)
    
#     # Collect indices of zero-sum subsets to remove
#     indices_to_remove = set()
#     while True:
#         subset = find_zero_sum_subset(nums, 0, [])
#         if not subset:
#             break
        
#         # Find indices of elements in the zero-sum subset and mark for removal
#         for value in subset:
#             indices_to_remove.add(nums.index(value))
#         # Remove elements from nums
#         nums = [num for i, num in enumerate(nums) if i not in indices_to_remove]
#         indices_to_remove.clear()

#     print("Numbers after Removal:")
#     print(nums)

def remove_zero_sum_subsets(nums, tolerance=0.8):
    def find_zero_sum_subsets(nums):
        cumulative_sum = 0
        sum_indices = {0: -1}  # Initialize with zero sum at index -1 for cases starting from index 0
        subsets_to_remove = set()
        
        for i, num in enumerate(nums):
            cumulative_sum += num
            
            # Find approximate zero-sum subset using tolerance
            for s in list(sum_indices.keys()):
                if abs(cumulative_sum - s) <= tolerance:
                    start_index = sum_indices[s] + 1
                    # Add subset range to be removed
                    subsets_to_remove.update(range(start_index, i + 1))
                    break

            # Track cumulative sum and index
            sum_indices[cumulative_sum] = i

        return sorted(subsets_to_remove)

    # Continuously find and remove zero-sum subsets
    while True:
        indices_to_remove = find_zero_sum_subsets(nums)
        if not indices_to_remove:
            break
        nums = [num for i, num in enumerate(nums) if i not in indices_to_remove]

    print(nums)

nums = [-3356222.30,189021.20,-7473796.90,316201.10,7473796.90,9340450.85,-9340450.85,-64578775.00,64578775.00,-119662197.14,119662197.14,119751351.04,-119751351.04,-413902.16,413902.16,15636638.69,552479.47,3453779.46,-43175726.34,6620379.76,43175726.34,-23412277.38]
result = remove_zero_sum_subsets(nums)
print("List after removing zero-sum subsets:", result)
