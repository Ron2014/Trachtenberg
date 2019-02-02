# -*- coding: GBK -*-
import time
from utils import *
from addition import sum_list

# 1. pair method
def multiply_direct_method(number_idx, multiplicand, multiplicator, carry_digit, len_multiplicator):

	#         ---------------------
	#         | ----------------- |
	#         | |               | |
	#   n n n n n n n     x     m m

	multiplicand_idx = number_idx
	multiplicator_idx = number_idx - multiplicand_idx

	digit_list = []
	if carry_digit > 0:
		digit_list.append(carry_digit)

	while multiplicand_idx>=0 and multiplicator_idx<len_multiplicator:
		digit_multiplicand = multiplicand[-1-multiplicand_idx]
		digit_multiplicator = multiplicator[-1-multiplicator_idx]

		if digit_multiplicand > 0 and  digit_multiplicator > 0:
			digit_list.append(digit_multiplicand * digit_multiplicator)

		multiplicand_idx -= 1
		multiplicator_idx = number_idx - multiplicand_idx

	# 这里用了累加技巧，当然也算出数字位直接相加
	return sum_list(digit_list)[0]

# 2. two-finger method
def multiply_speed_method(number_idx, multiplicand, multiplicator, carry_digit, len_multiplicator):

	#         U T------------------
	#         | U T-------------- |
	#         | | |             | |
	#   n n n n n n n     x     m m

	digit_list = []
	if carry_digit > 0:
		digit_list.append(carry_digit)

	multiplicand_idx = number_idx
	multiplicator_idx = number_idx - multiplicand_idx

	while multiplicand_idx>-1 and multiplicator_idx<len_multiplicator:
		digit_multiplicand_number = multiplicand[-1-multiplicand_idx]

		digit_multiplicand_neighbor = 0
		if multiplicand_idx>0:
			digit_multiplicand_neighbor = multiplicand[-multiplicand_idx]

		digit_multiplicator = multiplicator[-1-multiplicator_idx]

		# 备忘录获取乘法表的U-T，效率反而会慢一点，不过更接近心算流程
		new_carry = get_multiply_tens(digit_multiplicand_number, digit_multiplicator)
		u = get_multiply_unit(digit_multiplicand_number, digit_multiplicator)
		t = get_multiply_tens(digit_multiplicand_neighbor, digit_multiplicator)

		# u = (digit_multiplicand_number * digit_multiplicator) % 10
		# t = (digit_multiplicand_neighbor * digit_multiplicator) / 10

		if u > 0:
			digit_list.append(u)
		if t > 0:
			digit_list.append(t)

		multiplicand_idx -= 1
		multiplicator_idx = number_idx - multiplicand_idx

	# 这里用了累加技巧，当然也算出数字位直接相加
	return sum_list(digit_list)[0], new_carry

# 大数乘法
def multiply(a, b):
	# 0. 序列化（支持大数）
	multiplicand, multiplicand_power_ten = correct_number(a, True)
	multiplicator, multiplicator_power_ten = correct_number(b, True)

	# 1. 保证乘数长度比被乘数小
	len_multiplicand = len(multiplicand)
	len_multiplicator = len(multiplicator)

	if len_multiplicand < len_multiplicator:
		multiplicand, multiplicator = multiplicator, multiplicand
		len_multiplicand, len_multiplicator = len_multiplicator, len_multiplicand
		multiplicand_power_ten, multiplicator_power_ten = multiplicator_power_ten, multiplicand_power_ten

	# 2. 被乘数左侧补零
	multiplicand = [0] * len_multiplicator + multiplicand
	len_multiplicand += len_multiplicator

	result_list = []
	len_result = 0

	for i in xrange(len_multiplicand):
		# 3. 从右往左依次计算结果的每个数字位
		carry = 0
		if len_result > i:
			carry = result_list[i]      # 前一次操作的进位

		len_multiplicand_digit = i + 1
		len_multiplicator_digit = min(len_multiplicator, len_multiplicand_digit)

		# 两个方法，第二个方法是第一个方法基础上的改进
		# digit_sum = multiply_direct_method(i, multiplicand, multiplicator, carry, len_multiplicator_digit)
		# new_carry = 0
		#
		# # 4. 当数字位为零时表示计算结束
		# if not digit_sum or (len(digit_sum)==1 and digit_sum[0]==0):
		# 	break

		digit_sum, new_carry = multiply_speed_method(i, multiplicand, multiplicator, carry, len_multiplicator_digit)

		# 4. 当数字位为零且（U计算）没有进位时表示计算结束
		if (not digit_sum or (len(digit_sum)==1 and digit_sum[0]==0)) and new_carry == 0:
			break

		# 5. 最右位是结果的数字位
		digit_result = digit_sum[-1]
		if len_result > i:
			result_list[i] = digit_result
		else:
			result_list.append(digit_result)
			len_result += 1

		# 6. 其他位是进位
		if len(digit_sum) > 1:
			result_list.append(get_num_from_list(digit_sum[:-1]))
			len_result += 1

	return result_list[::-1], len_result, multiplicand_power_ten + multiplicator_power_ten

if __name__ == "__main__":
	tm = time.clock()
	print multiply("901341234556134801237123123", "90832709823490824524291275234")
	print time.clock() - tm

	tm = time.clock()
	print 901341234556134801237123123 * 90832709823490824524291275234
	print time.clock() - tm

	tm = time.clock()
	print multiply("256", "5")
	print time.clock() - tm

	tm = time.clock()
	print 256 * 5
	print time.clock() - tm
