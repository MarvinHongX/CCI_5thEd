# magic_index.py
#########################################################################################
# Author  : Hong
# Created : 28/11/2017
# Modified: 28/11/2017
# Notes   : [9.3] A magic index in an array A[0...n-1] is defined to be an index such that
#                 A[i] = i. Given a sorted array of distinct integers, write a method to find a
#                 magic index, if one exists, in array A.
#                 FOLLOW UP
#                 What if the values are not distinct?
#########################################################################################
import unittest, os, functools


def magic_index(seq, start=None, end=None):
    """ Return the magic index, or -1 if it does not exist. """

    if start is None:
        start = 0

    if end is None:
        end = len(seq) - 1

    if start > end:
        return -1

    # This is very similar to the binary search problem: we check whether the
    # middle index is a magic one, and if it is not we repeat the same action
    # on the sub-array to its left or to its right. Which side? It depends on
    # the value on the index and its corresponding element:
    #
    # The fact that the elements of the sequence are distinct integers allows
    # us to draw a conclusion if index > seq[index]: the magic index, in case
    # it exists, cannot be on the left side. The index decreases one by one and
    # the (unique) elements by at least one, so (index - n) is guaranteed to be
    # larger than seq[index - n]. In other words: if we reach a point where the
    # index is larger than the corresponding element, we can only hope that the
    # element eventually catches up, since the index increases one by one while
    # the elements can make larger leaps, so to speak.

    index = (start + end) // 2
    if index == seq[index]:
        return index

    if index > seq[index]:
        return magic_index(seq, start=index + 1, end=end)
    else:
        return magic_index(seq, start=start, end=index - 1)


def magic_index_duplicates(seq, start=None, end=None):
    """ Return the magic index, or -1 if it does not exist. """

    if start is None:
        start = 0

    if end is None:
        end = len(seq) - 1

    if start > end:
        return -1

    # If there can be duplicate elements, we cannot determine on which side,
    # left or right, the magic index is. Even if index > seq[index], the same
    # element could be repeated many times, allowing the index to decrease one
    # by one, as we moved to the left, until it eventually caught up with the
    # corresponding element. And the magic index could be on the right, as the
    # index increases one by one while the elements can make larger leaps. We
    # must look, therefore, on both sides. We will start on the left, trying
    # the right side only if the magic index is not found there.
    #
    # But there is a small optimization that we can do here. The first index
    # that, to the right, could be a magic one is seq[index] (as the array is
    # sorted), so we can skip all the elements in positions between index and
    # seq[index] if the latter happens to be larger than the former. In the
    # same way, in case seq[index] is smaller than index we can ignore those
    # elements whose position is larger than seq[index].

    index = (start + end) // 2
    value = seq[index]

    if index == value:
        return index

    # Left sub-array
    left_end = min(index - 1, value)
    left_index = magic_index_duplicates(seq, start=start, end=left_end)
    if left_index != -1:
        return left_index

    # Right sub-array
    right_start = max(index + 1, value)
    return magic_index_duplicates(seq, start=right_start, end=end)


class MagicIndexTest(unittest.TestCase):

    def test_magic_index(self):
        f = magic_index
        self.assertEqual(1, f([0, 1, 2]))
        self.assertEqual(1, f([-2, 1, 3]))
        self.assertEqual(-1, f([-2, 0, 1]))
        self.assertEqual(-1, f([-2, -1, 1]))
        self.assertEqual(-1, f([-3, -1, 1]))
        self.assertEqual(-1, f([-3, -2, -1]))
        self.assertEqual(3, f([-4, 0, 1, 3]))
        self.assertEqual(1, f([-1, 1, 2, 4]))
        self.assertEqual(-1, f([-1, 0, 1, 4]))
        self.assertEqual(-1, f([-2, -1, 0, 4]))
        self.assertEqual(-1, f([-3, -1, 0, 2]))
        self.assertEqual(-1, f([1, 2, 3, 5, 6]))
        self.assertEqual(2, f([-5, 1, 2, 3, 5]))
        self.assertEqual(3, f([-4, -3, 0, 3, 5]))
        self.assertEqual(-1, f([-5, -4, -1, 1, 2]))
        self.assertEqual(4, f([-3, 0, 1, 2, 4, 6]))
        self.assertEqual(-1, f([-3, -2, -1, 0, 1, 4]))
        self.assertEqual(-1, f([-4, -3, -2, 2, 3, 4]))
        self.assertEqual(-1, f([-3, -2, 1, 4, 5, 6, 7]))
        self.assertEqual(-1, f([-7, -2, 3, 5, 6, 7, 8]))
        self.assertEqual(-1, f([-6, -5, -1, 2, 3, 4, 5]))
        self.assertEqual(-1, f([-5, -3, -1, 1, 6, 7, 8]))
        self.assertEqual(-1, f([-3, -2, -1, 1, 3, 4, 5]))
        self.assertEqual(-1, f([-5, -4, -3, 4, 5, 7, 8, 9]))
        self.assertEqual(-1, f([-7, -3, -2, -1, 1, 6, 7, 8]))
        self.assertEqual(-1, f([-7, -6, 0, 1, 3, 4, 5, 6, 7]))
        self.assertEqual(5, f([-5, -4, -3, -2, 2, 5, 7, 8, 9]))
        self.assertEqual(-1, f([-7, -6, -5, -4, 2, 3, 4, 5, 6]))
        self.assertEqual(5, f([-7, -6, -4, -1, 1, 5, 7, 8, 9, 10]))
        self.assertEqual(10, f([-9, -7, -4, 0, 1, 2, 3, 6, 7, 8, 10]))
        self.assertEqual(8, f([-10, -9, -8, -7, -6, -5, 1, 2, 8, 10]))
        self.assertEqual(-1, f([-10, -9, -8, -7, -5, -1, 0, 1, 5, 6, 9]))
        self.assertEqual(-1, f([-11, -10, -9, -8, -7, -5, -1, 0, 1, 2, 8]))
        self.assertEqual(-1, f([-11, -7, -6, -5, -2, -1, 8, 9, 10, 11, 12]))
        self.assertEqual(-1, f([-12, -9, -4, -3, -2, 1, 2, 3, 4, 7, 8, 12]))
        self.assertEqual(8, f([-8, -7, -5, -4, -3, -1, 0, 7, 8, 9, 10, 11]))
        self.assertEqual(11, f([-8, -7, -2, -1, 2, 3, 5, 6, 7, 8, 9, 11, 12]))
        self.assertEqual(10, f([-11, -7, -6, -4, 0, 1, 2, 6, 7, 8, 10, 12, 13]))
        self.assertEqual(12, f([-12, -11, -10, -9, -8, -7, 1, 2, 3, 4, 7, 9, 12]))
        self.assertEqual(6, f([-8, -7, -3, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]))
        self.assertEqual(9, f([-10, -6, -4, -3, -2, -1, 2, 4, 8, 9, 10, 11, 12]))
        self.assertEqual(11, f([-12, -11, -6, -5, -4, -3, -2, 0, 1, 3, 5, 11, 12]))
        self.assertEqual(11, f([-12, -11, -10, -9, -8, -7, -1, 0, 4, 5, 10, 11, 13]))
        self.assertEqual(12, f([-13, -12, -8, -6, -5, -4, 2, 3, 4, 6, 7, 8, 12, 14]))
        self.assertEqual(-1, f([-10, -8, -7, -4, -3, -1, 0, 1, 2, 3, 4, 5, 6, 9, 12]))
        self.assertEqual(-1, f([-8, -7, -6, -4, -3, 0, 2, 3, 4, 6, 7, 12, 13, 14, 15]))
        self.assertEqual(12, f([-12, -11, -10, -9, -8, -7, -6, -5, -4, 3, 8, 9, 12, 13]))
        self.assertEqual(14, f([-15, -11, -7, -5, -3, 0, 1, 4, 5, 8, 9, 10, 11, 12, 14]))
        self.assertEqual(14, f([-12, -10, -9, -8, -7, -1, 0, 4, 5, 6, 7, 8, 10, 11, 14]))
        self.assertEqual(13, f([-14, -13, -10, -9, -8, -4, -2, -1, 0, 1, 2, 5, 12, 13, 15]))

        f = magic_index_duplicates
        self.assertEqual(1, f([-3, 1, 2]))
        self.assertEqual(-1, f([-1, 0, 3]))
        self.assertEqual(2, f([-3, 0, 2]))
        self.assertEqual(-1, f([-3, 0, 0]))
        self.assertEqual(-1, f([-3, 0, 1]))
        self.assertEqual(1, f([-3, 1, 1]))
        self.assertEqual(-1, f([-3, -3, -2]))
        self.assertEqual(0, f([0, 2, 2, 3]))
        self.assertEqual(0, f([0, 3, 4, 4]))
        self.assertEqual(-1, f([-2, -1, 0, 1]))
        self.assertEqual(-1, f([-5, -5, 1, 2, 2]))
        self.assertEqual(3, f([-4, -1, 3, 3, 4]))
        self.assertEqual(-1, f([-4, -1, 0, 4, 5]))
        self.assertEqual(1, f([-6, 1, 1, 3, 4, 5]))
        self.assertEqual(2, f([-3, 1, 2, 4, 5, 5]))
        self.assertEqual(3, f([-4, -3, -2, 3, 3, 4]))
        self.assertEqual(-1, f([-6, -4, -4, -4, 0, 2]))
        self.assertEqual(3, f([-6, -4, 2, 3, 4, 5, 7]))
        self.assertEqual(-1, f([-4, -3, -3, -2, -2, -2]))
        self.assertEqual(5, f([-7, -6, -4, 0, 2, 5, 5]))
        self.assertEqual(4, f([-6, -4, -2, 4, 4, 4, 5]))
        self.assertEqual(-1, f([-7, -6, -6, -6, -1, 4, 5]))
        self.assertEqual(-1, f([-5, -4, -3, 0, 1, 2, 3, 6]))
        self.assertEqual(5, f([-6, -2, -1, 5, 5, 5, 5, 6]))
        self.assertEqual(3, f([-5, -3, -2, 3, 6, 7, 7, 7]))
        self.assertEqual(6, f([-8, -4, -3, -2, 1, 4, 6, 8]))
        self.assertEqual(-1, f([-8, -3, 0, 1, 2, 3, 5, 5, 6]))
        self.assertEqual(6, f([-9, -5, 0, 2, 5, 6, 6, 6, 7]))
        self.assertEqual(6, f([-8, -7, -4, -4, -3, -2, 6, 7]))
        self.assertEqual(-1, f([-9, -7, -6, -5, 0, 1, 4, 6, 7]))
        self.assertEqual(-1, f([-8, -7, -7, -6, -5, -4, -1, 2, 7]))
        self.assertEqual(-1, f([-8, -8, -7, -7, -7, 0, 1, 1, 7, 8]))
        self.assertEqual(8, f([-10, -7, -2, 0, 1, 1, 1, 2, 8, 10]))
        self.assertEqual(-1, f([-2, -1, 1, 1, 2, 2, 4, 4, 5, 6, 9]))
        self.assertEqual(-1, f([-10, -10, -8, -6, -1, 1, 3, 3, 5, 8]))
        self.assertEqual(-1, f([-11, -9, -7, -6, 1, 2, 2, 4, 6, 6, 7]))
        self.assertEqual(-1, f([-5, -4, -3, -3, -2, 1, 3, 4, 5, 8, 9]))
        self.assertEqual(-1, f([-10, -10, -7, -3, -1, 1, 3, 9, 10, 10]))
        self.assertEqual(5, f([-11, -11, -9, 0, 5, 5, 7, 8, 9, 9, 10]))
        self.assertEqual(10, f([-10, -8, -7, -2, -2, -1, 0, 3, 5, 6, 10]))
        self.assertEqual(8, f([-9, -7, -4, -2, 0, 4, 7, 8, 8, 8, 9, 11]))
        self.assertEqual(12, f([-9, -9, -7, -5, -4, 3, 5, 5, 7, 7, 8, 9, 12]))
        self.assertEqual(11, f([-12, -10, -9, -6, -4, -4, -3, -1, 0, 0, 9, 11]))
        self.assertEqual(-1, f([-14, -10, -7, -4, 0, 2, 2, 5, 6, 8, 9, 10, 11, 11, 13]))
        self.assertEqual(13, f([-14, -13, -9, -9, -8, -7, -7, -7, 1, 5, 9, 10, 13, 13]))
        self.assertEqual(14, f([-9, -8, -6, -6, -5, -4, -4, -3, 1, 3, 5, 6, 13, 14, 14]))
        self.assertEqual(-1, f([-12, -11, -11, -9, -9, -8, -6, -6, -3, -1, 0, 8, 9, 12, 12]))
        self.assertEqual(-1, f([-13, -12, -11, -11, -10, -6, -4, -3, -1, 1, 7, 8, 9, 9, 15]))
        self.assertEqual(12, f([-13, -13, -13, -12, -11, -10, 0, 0, 0, 5, 6, 6, 12, 14, 15]))
        self.assertEqual(13, f([-13, -12, -10, -8, -7, -5, -1, 8, 10, 11, 12, 12, 13, 13, 14]))


if __name__ == "__main__":
    unittest.main()
