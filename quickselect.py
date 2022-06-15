"""
Author: Zane Miller
Date: 06/14/2022
Email: millzanem@gmail.com
Description: Quickselect algorithm
"""

import random, math
import statistics


class Quickselect:
    """
    Creates an Quickselect class select the 'k-th' smallest item or sort the
    elements in ascending order
    TODO integrate median of medians with quickselect for selecting pivot
    """

    def __init__(self, arr):
        """
        Defines the Quickselect object with an array to be sorted or to find
        the 'k-th' smallest object
        :param arr: unsorted list of k elements
        :return: 'k-th' smallest value or error if k out of range
        """
        self.arr = arr
        self.left_index = 0
        self.right_index = len(arr) - 1

    def quickselect(self, k):
        """
        Helper function for selecting the 'k-th' smallest value
        :param k:
        :return:
        """
        return self.find(self.left_index, self.right_index, k - 1)

    def find(self, first_index, last_index, k):
        """

        :param first_index: the first index to be considered in the selection
        :param last_index: the last index to be considered in the selection
        :param k: the 'k-th' smallest item
        :return: the 'k-th' smallest item
        """
        # While k is within range of 1st smallest to largest within size of array

        # re-arrange the array so that smaller values are to left of pivot and
        # larger values are to right of pivot

        pivot_index = self.partition(first_index, last_index)

        #  The 'k-th' smallest element found
        if pivot_index < k:
            # The 'k-th' smallest item on the right side of the pivot
            return self.find(pivot_index + 1, last_index, k)

        # The 'k-th' smallest item is on the left side of the pivot
        elif pivot_index > k:
            # call quickselect on the left subarray until k == pivot
            return self.find(first_index, pivot_index - 1, k)

        return self.arr[pivot_index]

    def partition(self, first_index, last_index):
        """
        Defines a pivot_index and then partitions the array with smaller values
        to the left of the pivot and larger values to the right of the pivot
        :param first_index: the first index to be considered in the partition
        :param last_index: the last index to be considered in the partition
        :return: pivot index after pivot in correct spot
        """
        pivot_index = random.randint(first_index, last_index)

        # Move the pivot to the end
        self.swap(pivot_index, last_index)

        # Traverse the list
        for index in range(first_index, last_index):

            # Swap the low_index and trail_index when low < pivot
            if self.arr[index] < self.arr[last_index]:
                self.swap(index, first_index)

                first_index += 1

        # Swap pivot to its corrct position
        self.swap(last_index, first_index)

        return first_index

    def swap(self, a, b):
        """
        Swaps two values in an array given their indices
        :param a: index a to swap with index b
        :param b: index b to swap with index a
        :return: none
        """
        self.arr[a], self.arr[b] = \
            self.arr[b], self.arr[a]

    def quick_sort(self):
        """
        Sorts (ascending) an unsorted array using quickselect
        :return: sorted array
        """
        sorted_arr = []

        for index in range(1, len(self.arr) + 1):
            sorted_arr.append(self.quickselect(index))

        return sorted_arr


def insertion_sort(start_index, end_index, arr):
    """
    Insertion sort algorithm
    """

    for index in range(start_index, end_index + 1):
        key = arr[index]

        j = index - 1
        while j >= start_index and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


class QuickselectMedian:
    """
    Quickselect class using median of medias algorithm.
    """

    def __init__(self, arr, k):
        """
        creates an object with an array and k-th smallest item to find.
        """
        self.arr = arr
        self.k = k

        self.median_median_helper()

    def median_median(self, arr, k):
        """
        Finds the median of medians of sub-arrays of defined group size.
        Returns the value of the median of medians
        """

        group_size = 5
        groups = int(math.ceil(len(arr) / group_size))
        group_num = 1
        medians = []

        # sorts each sub-arry of size 5
        while group_num < groups:
            first_index = group_num * group_size - group_size
            last_index = group_num * group_size
            chunk = sorted(arr[first_index:last_index])
            chunk.sort()
            group_num += 1

            # adds the median of group to medians
            median_index = len(chunk) // 2
            medians.append(chunk[median_index])

        # sorts the last group
        if group_num == groups:
            first_index = group_num * group_size - group_size
            last_index = len(arr)
            chunk = arr[first_index:last_index]
            chunk.sort()

            # adds the median of group to medians
            median_index = len(chunk) // 2
            medians.append(chunk[median_index])

        # sort the medians to find the median of medians
        medians.sort()
        median_index = len(medians) // 2
        pivot_value = medians[median_index]

        left_array = [n for n in arr if n < pivot_value]
        right_array = [m for m in arr if m > pivot_value]
        pivot_index = len(left_array)

        if k < pivot_index:
            return self.median_median(left_array, k)

        elif k > pivot_index:
            return self.median_median(right_array, k - len(left_array) - 1)

        return pivot_value

    def median_median_helper(self):
        """
        Temp
        """
        return self.median_median(self.arr, self.k - 1)


if __name__ == '__main__':

    print("Test -- Quickselect with Median of Medians")
    print("-----------------------------------------")

    my_arr00 = [1, -2, 5, 8, 7, 6, 10, 4, 18, 2, -3, -4, 55, 0, 11]
    quick_select_median = QuickselectMedian(my_arr00, 1)
    print("median of medians smallest:",
          quick_select_median.median_median_helper())

    my_arr01 = [1, -2, 5, 8, 7, 6, 10, 4, 18, 2, -3, -4, 55, 0, 11]
    quick_select_median = QuickselectMedian(my_arr01, len(my_arr01))
    print("median of medians largest:",
          quick_select_median.median_median_helper())
    print("\n")


    print("Test -- Insertion sort test")
    print("---------------------------")
    insertion_sort(0, len(my_arr00) - 1, my_arr00)
    print("Insertion sort test:", my_arr00)
    print("\n")


    print("Test 1 - Small fixed array")
    print("--------------------------")
    my_arr = [1, 2, -5, 10, 100, -7, 3, 4]
    quick_select = Quickselect(my_arr)
    # find the smallest item
    print("smallest:", quick_select.quickselect(1))
    # find the largest item
    print("largest:", quick_select.quickselect(len(my_arr)))
    # sort the array
    print("sorted:", quick_select.quick_sort())
    print("\n")

    print("Test 2 - Larger random array")
    print("----------------------------")
    my_arr2 = []
    for num in range(50):
        random_int = random.randint(-1000, 1000)
        my_arr2.append(random_int)
    quick_select2 = Quickselect(my_arr2)
    # find the smallest item
    print("smallest:", quick_select2.quickselect(1))
    # find the largest item
    print("largest:", quick_select2.quickselect(len(my_arr2)))
    # sort the array
    print("sorted:", quick_select2.quick_sort())
