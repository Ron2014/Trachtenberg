# -*- coding: GBK -*-
import time
from multiplication import multiply
from utils import *

SQRT = []
SQURE = {}
for i in xrange(9, -1, -1):
	num = i*i
	t, u = num/10, num%10
	SQURE[i] = (num, t, u)
	SQRT.append((num, i, num/10, num%10))

def get_square(num):
	return SQURE.get(num)

def get_root(num):
	for square, root, t, u in SQRT:
		if num >= square:
			return root, square, t, u

# 根的新数字位，与根的最高位的NT（用于验证）
def get_new_remainder_from_nt(num_remainder, root_number, root_neighbor, digit_root):
	n = 2 * digit_root * root_number
	t = get_multiply_tens(2 * digit_root, root_neighbor)

	num_remainder -= (n + t)
	if num_remainder < 0:
		return False

	return correct_number(num_remainder)

# 根的新数字位，与该位（非最高位）上的UT（用于求余）
def get_new_remainder_from_ut(num_remainder, root_number, root_neighbor, digit_root):
	u = get_multiply_unit(2 * digit_root, root_number)
	t = get_multiply_tens(2 * digit_root, root_neighbor)

	num_remainder -= (u + t)
	if num_remainder < 0:
		return False

	return correct_number(num_remainder)

def square_root_loop(square_list, root=None, remainder=None, root_square=None, i=0, root_idx=1):
	if root is None:
		root = []
	if remainder is None:
		remainder = []
	if root_square is None:
		root_square = []

	len_root = len(root)
	len_square = len(square_list)
	len_root_square = len(root_square)
	calc_remainder = (root_idx > 0)

	if calc_remainder:
		# 求余运算
		if i >= len_square:
			return list_strip_zero(root), remainder

		remainder.append(square_list[i])
		new_remainder = remainder

		if len_root > 1:
			num_remainder = get_num_from_list(remainder)

			if i < len_root_square:
				num_remainder -= root_square[i]

			digit_root = root[-1]
			root_number = 0
			root_neighbor = 0
			if root_idx < len_root-1:
				root_number = root[root_idx]
			if root_idx < len_root-2:
				root_neighbor = root[root_idx+1]

			new_remainder = get_new_remainder_from_ut(num_remainder, root_number, root_neighbor, digit_root)
			if new_remainder is False:
				return False

		finish_root = i >= (len_square - len_root) # 平方根已经求出来，现在是求余、验算部分
		if finish_root:
			return square_root_loop(square_list, root, new_remainder, root_square, i+1, root_idx+1)
		else:
			# 继续求平方根
			return square_root_loop(square_list, root, new_remainder, root_square, i, 0)
	else:
		# 求根运算
		num_remainder = get_num_from_list(remainder)

		if len_root > 0:
			root_number = root[0]
			digit_root = min((num_remainder / 2) / root_number, 9)

			root_neighbor = 0
			root_number = root[0]
			if len_root > 1:
				root_neighbor = root[1]

			root.append(digit_root)
			_, t_square, u_square = get_square(digit_root)
			root_square.append(t_square)
			root_square.append(u_square)

			while True:
				# 如果新求的这个的digit_root，它的平方在该i位有值（刚添加进来的）
				if i >= len_root_square:
					num_remainder -= root_square[i]

				new_remainder = get_new_remainder_from_nt(num_remainder, root_number, root_neighbor, digit_root)
				if new_remainder is not False:
					result = square_root_loop(square_list, root, new_remainder, root_square, i + 1)
					if result is not False:
						return result

				digit_root -= 1
				_, t_square, u_square = get_square(digit_root)
				if i >= len_root_square:
					num_remainder += root_square[i]

				root[-1] = digit_root
				root_square[-2] = t_square
				root_square[-1] = u_square
		else:
			if len_square % 2 == 0 and i == 0:
				return square_root_loop(square_list, [], remainder, [], i+1)

			digit_root, digit_square, t_square, u_square = get_root(num_remainder)

			if i > 0:
				root_square.append(t_square)
			root_square.append(u_square)
			root.append(digit_root)

			num_remainder -= digit_square

			result = square_root_loop(square_list, root, correct_number(num_remainder), root_square, i+1)
			if result is False:
				return square_root_loop(square_list, [], remainder, [], i+1)
			return result

def square_root(data):
	square_list = correct_number(data)
	return square_root_loop(square_list)

if __name__ == "__main__":
	tm = time.clock()
	print "root of 1 = ", square_root("1")
	print "root of 81 = ", square_root("81")
	print "root of 25 = ", square_root("25")
	print "root of 225 = ", square_root("225")
	print "root of 46500 = ", square_root("46500")
	print "root of 10323369 = ", square_root("10323369")
	print "root of 872079961 = ", square_root("872079961")
	print "root of 9987634 = ", square_root("9987634")
	print "root of 40094224 = ", square_root("40094224")
	print "root of 103456 = ", square_root("103456")
	print "root of 7695 = ", square_root("7695")
	print "root of 769500 = ", square_root("769500")
	print time.clock() - tm