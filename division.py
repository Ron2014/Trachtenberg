# -*- coding: GBK -*-
import time
from multiplication import multiply
from utils import *

# 简单除法 ##############################################################################################################
def divide_simple(dividend, divisor):
	len_dividend = len(dividend)
	len_divisor = len(divisor)

	# 1. 生成除数的倍数表（1-9）
	len_substractor = 9
	tbl_substractor = []
	tbl_substractor.append(divisor)
	for i in xrange(2,len_substractor+1):
		num, _, power_ten = multiply(divisor, i)
		tbl_substractor.append(num + [0] * power_ten)

	quotient = []
	remainder = dividend[:len_divisor-1]
	len_remainder = len_divisor -1

	# 2. 将除法换算成阶梯型减法
	for i in xrange(len_divisor-1, len_dividend):
		if len_remainder == 0 and dividend[i] == 0:
			if len(quotient) > 0:
				quotient.append(0)
			continue

		remainder.append(dividend[i])
		subtractor_idx = None

		min_idx = 0
		max_idx = len_substractor-1

		if not is_smaller_or_equal(tbl_substractor[min_idx], remainder):
			if len(quotient) > 0:
				quotient.append(0)
			continue

		if is_smaller_or_equal(tbl_substractor[max_idx], remainder):
			subtractor_idx = max_idx

		else:
			# 二分法查找：比remainder小的最大substractor
			while min_idx<=max_idx:
				mid_idx = (min_idx + max_idx) / 2

				if is_smaller_or_equal(tbl_substractor[mid_idx], remainder):
					min_idx = mid_idx+1
					subtractor_idx = mid_idx
				else:
					max_idx = mid_idx-1

		# if not is_smaller_or_equal(divisor, remainder):
		# 	if len(quotient) > 0:
		# 		quotient.append(0)
		# 	continue
		#
		# for i in xrange(len_substractor):
		# 	if is_smaller_or_equal(tbl_substractor[-1-i], remainder):
		# 		subtractor_idx = -1-i+len_substractor
		# 		break

		if subtractor_idx is None:
			continue

		digit_quotient = subtractor_idx+1
		quotient.append(digit_quotient)

		subtractor = tbl_substractor[subtractor_idx]

		for i, digit_substractor in enumerate(subtractor[::-1]):
			digit_remainder = remainder[-1 - i]

			# 从右往左按位做减法，若不够减向高位借1
			if digit_remainder < digit_substractor:
				remainder[-2 - i] -= 1  # 左边是高位
				remainder[-1 - i] = digit_remainder + 10 - digit_substractor

			else:
				remainder[-1 - i] = digit_remainder - digit_substractor

		# 高位的0去掉
		remainder = list_strip_zero(remainder)

	return quotient, remainder

########################################################################################################################

# 求得一个商，计算它与除数的NT（只算最高位）
def get_new_remainder_from_nt(num_remainder, divisor_number, divisor_neighbor, digit_quotient):
	n = digit_quotient * divisor_number
	t = get_multiply_tens(digit_quotient, divisor_neighbor)

	num_remainder -= (n + t)
	if num_remainder < 0:
		return False

	return correct_number(num_remainder)

# 求得一个商，计算它与除数的UT（阶梯式）
def get_new_remainder_from_ut(num_remainder, divisor, divisor_idx, quotient):
	len_divisor = len(divisor)
	for i, n in enumerate(quotient[::-1]):
		if divisor_idx + i >= len_divisor:
			break

		u_factor = divisor[divisor_idx+i]

		t_factor = 0
		if divisor_idx+i+1 < len_divisor:
			t_factor = divisor[divisor_idx+i+1]

		u = get_multiply_unit(n, u_factor)
		t = get_multiply_tens(n, t_factor)

		num_remainder -= (u + t)

	if num_remainder < 0:
		return False

	return correct_number(num_remainder)

# two-finger 方法 ######################################################################################################
def divide_fast(dividend, divisor, quotient=None, remainder=None, i=0, divisor_idx=1):
	# 注意第一轮运算实际上是求余预算
	# print quotient, remainder
	if quotient is None:
		quotient = []
	if remainder is None:
		remainder = []

	len_divisor = len(divisor)
	calc_remainder = (divisor_idx > 0)

	if calc_remainder:
		# 求余运算
		# 1. 拼接数字
		len_dividend = len(dividend)
		if i >= len_dividend:
			return list_strip_zero(quotient), remainder

		remainder.append(dividend[i])
		num_remainder = get_num_from_list(remainder)
		# n n n n n | n n n    ÷     m m m m   =   x x x x x
		#            r+=n
		#             ↑
		#         r---|

		# 2. 计算UT，求余数
		new_remainder = get_new_remainder_from_ut(num_remainder, divisor, divisor_idx, quotient)
		if new_remainder is False:
			return False

		#
		#                              U T------------------
		#                                U T-------------- |
		#                                  U-----------| | |
		# n n n n n | n n n    ÷     m m m m   =   x x x x x
		#             r
		#             -=
		#         UT1,UT2,UT3
		#

		finish_quotient = i > (len_dividend - len_divisor)
		if finish_quotient:
			# 商都求完了，剩下的数字用来求余，而且除数下标右移
			#
			#             i
			# x x x x x
			# n n n n n | n n n    ÷     m m m m   =   x x x x x
			#
			return divide_fast(dividend, divisor, quotient, new_remainder, i+1, divisor_idx+1)

		else:
			# 在该位上求商
			return divide_fast(dividend, divisor, quotient, new_remainder, i, 0)

	else:
		# 求商运算
		quotient_idx = len(quotient)
		num_remainder = get_num_from_list(remainder)

		divisor_number = divisor[0]
		divisor_neighbor = 0
		if len_divisor > 1:
			divisor_neighbor = divisor[1]

		digit_quotient =  num_remainder / divisor_number
		new_remainder = remainder

		#
		#                            N T--------------------
		#                            | |                   |
		# n n n n n | n n n    ÷     m m m m   =   x x x x ?
		#         r
		#         -=
		#         NT
		#

		if digit_quotient > 0:
			new_remainder = get_new_remainder_from_nt(num_remainder, divisor_number, divisor_neighbor, digit_quotient)

			while new_remainder is False:
				digit_quotient -= 1
				new_remainder = remainder

				if digit_quotient > 0:
					new_remainder = get_new_remainder_from_nt(num_remainder, divisor_number, divisor_neighbor, digit_quotient)

		quotient.append(digit_quotient)

		result = divide_fast(dividend, divisor, quotient, new_remainder, i+1)
		if result is False:
			digit_quotient -= 1
			new_remainder = remainder

			if digit_quotient > 0:
				new_remainder = get_new_remainder_from_nt(num_remainder, divisor_number, divisor_neighbor, digit_quotient)

			quotient[quotient_idx] = digit_quotient
			return divide_fast(dividend, divisor, quotient, new_remainder, i+1)

		return result

def divide(a, b):
	# 0. 序列化（支持大数）
	dividend = correct_number(a)
	divisor = correct_number(b)

	len_dividend = len(dividend)
	len_divisor = len(divisor)

	if len_dividend < len_divisor:
		return (0, dividend)

	# return divide_simple(dividend, divisor)
	return divide_fast(dividend, divisor)

if __name__ == "__main__":
	tm = time.clock()
	print "1. 5678 ÷ 41 =", divide("5678", "41")
	print "2. 4871 ÷ 74 =", divide("4871", "74")
	print "3. 70000 ÷ 52 =", divide("70000", "52")
	print "4. 7389 ÷ 82 =", divide("7389", "82")
	print "5. 9036 ÷ 36 =", divide("9036", "36")
	print "6. 36865 ÷ 73 =", divide("36865", "73")
	print "7. 22644 ÷ 51 =", divide("22644", "51")
	print "8. 28208 ÷ 82 =", divide("28208", "82")
	print "9. 14847 ÷ 49 =", divide("14847", "49")
	print "10. 11556 ÷ 36 =", divide("11556", "36")
	print "11. 18606 ÷ 31 =", divide("18606", "31")
	print "12. 43271 ÷ 72 =", divide("43271", "72")
	print "13. 81035 ÷ 95 =", divide("81035", "95")
	print "14. 63000 ÷ 72 =", divide("63000", "72")
	print "15. 4839 ÷ 64 =", divide("4839", "64")
	print "16. 2014 ÷ 56 =", divide("2014", "56")
	print "17. 5673 ÷ 72 =", divide("5673", "72")
	print "18. 5329 ÷ 95 =", divide("5329", "95")
	print "19. 4768 ÷ 92 =", divide("4768", "92")
	print "20. 5401 ÷ 67 =", divide("5401", "67")
	print "21. 2001 ÷ 45 =", divide("2001", "45")
	print "22. 7302 ÷ 86 =", divide("7302", "86")
	print "23. 9345 ÷ 99 =", divide("9345", "99")
	print "24. 85367 ÷ 26 =", divide("85367", "26")
	print "25. 479535 ÷ 63 =", divide("479535", "63")
	print "26. 236831 ÷ 674 =", divide("236831", "674")
	print "27. 543765 ÷ 823 =", divide("543765", "823")
	print "28. 234876 ÷ 632 =", divide("234876", "632")
	print "29. 204356 ÷ 913 =", divide("204356", "913")
	print "30. 743567 ÷ 256 =", divide("743567", "256")
	print "31. 4536754 ÷ 543 =", divide("4536754", "543")
	print "32. 27483624 ÷ 6211 =", divide("27483624", "6211")
	print "33. 63123257 ÷ 9832 =", divide("63123257", "9832")
	print time.clock() - tm

	tm = time.clock()
	print "1. 5678 ÷ 41 =", 5678 / 41
	print "2. 4871 ÷ 74 =", 4871 / 74
	print "3. 70000 ÷ 52 =", 70000 / 52
	print "4. 7389 ÷ 82 =", 7389 / 82
	print "5. 9036 ÷ 36 =", 9036 / 36
	print "6. 36865 ÷ 73 =", 36865 / 73
	print "7. 22644 ÷ 51 =", 22644 / 51
	print "8. 28208 ÷ 82 =", 28208 / 82
	print "9. 14847 ÷ 49 =", 14847 / 49
	print "10. 11556 ÷ 36 =", 11556 / 36
	print "11. 18606 ÷ 31 =", 18606 / 31
	print "12. 43271 ÷ 72 =", 43271 / 72
	print "13. 81035 ÷ 95 =", 81035 / 95
	print "14. 63000 ÷ 72 =", 63000 / 72
	print "15. 4839 ÷ 64 =", 4839 / 64
	print "16. 2014 ÷ 56 =", 2014 / 56
	print "17. 5673 ÷ 72 =", 5673 / 72
	print "18. 5329 ÷ 95 =", 5329 / 95
	print "19. 4768 ÷ 92 =", 4768 / 92
	print "20. 5401 ÷ 67 =", 5401 / 67
	print "21. 2001 ÷ 45 =", 2001 / 45
	print "22. 7302 ÷ 86 =", 7302 / 86
	print "23. 9345 ÷ 99 =", 9345 / 99
	print "24. 85367 ÷ 26 =", 85367 / 26
	print "25. 479535 ÷ 63 =", 479535 / 63
	print "26. 236831 ÷ 674 =", 236831 / 674
	print "27. 543765 ÷ 823 =", 543765 / 823
	print "28. 234876 ÷ 632 =", 234876 / 632
	print "29. 204356 ÷ 913 =", 204356 / 913
	print "30. 743567 ÷ 256 =", 743567 / 256
	print "31. 4536754 ÷ 543 =", 4536754 / 543
	print "32. 27483624 ÷ 6211 =", 27483624 / 6211
	print "33. 63123257 ÷ 9832 =", 63123257 / 9832
	print time.clock() - tm
