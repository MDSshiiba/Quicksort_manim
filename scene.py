from manim import *
import random
from random import seed, uniform
import colorama
from collections import deque

S = []
def qSort(startNum, endNum,seq):
    pivot = seq[(startNum + endNum) // 2]
    left = startNum
    right = endNum

    while True:
        while seq[left] < pivot:
            left += 1
        while pivot < seq[right]:
            right -= 1
        if left >= right:
            break

        seq[left],seq[right] = seq[right],seq[left]
        S.append([left,right])

        left += 1
        right -= 1

    if startNum < left-1:
        qSort(startNum, left-1,seq)
    if right + 1 < endNum:
        qSort(right+1, endNum,seq)

def bubble_sort(seq):
    n = len(seq) - 1
    for i in range(n):
        for j in range(n - i):
            if seq[j] > seq[j+1]:
                seq[j] , seq[j+1] = seq[j+1], seq[j]
                yield (j,j+1)

class SortAnimation(Scene):
    def construct(self):
        g = Group()
        numbers = list(range(1,11))
        random.shuffle(numbers)
        print(numbers)
        for number in numbers:
            g.add(Circle(radius=number/2*0.1))

        self.add(g.arrange_in_grid(rows=1,col_widths=[1]*10))
	# 追加分↓
        qSort(0, len(numbers)-1,numbers)
        A = list(range(11))
        a = []
        for i,j in S:
            A[i],A[j] = A[j],A[i]
            a.append([A[i],A[j]])
        print(*a)
        for i,j in a:
            self.play(Swap(g.submobjects[i], g.submobjects[j]))
            #g.submobjects[i], g.submobjects[i+1] = g.submobjects[i+1], g.submobjects[i]
        print(S)
