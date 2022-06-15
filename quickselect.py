"""
Author: Zane Miller
Date: 06/14/2022
Email: millzanem@gmail.com
Description: Quickselect algorithm
"""

import random


class Quickselect:
    """
    Creates an Quickselect class select the 'k-th' smallest item or sort the
    elements in ascending order
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

    def median_median(self):
        """
        Temp
        """



if __name__ == '__main__':

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
