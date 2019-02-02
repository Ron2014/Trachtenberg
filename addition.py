# -*- coding: GBK -*-
import time
from utils import *

# �����ۼ�
def sum_list(num_list):
	# 0. ���л���֧�ִ�����
	correct_list = []

	max_positive_digit = 0
	max_negative_digit = 0

	for num in num_list:
		n_list, power_ten = correct_number(num, True)

		len_num = len(n_list)
		positive_digit = len_num + power_ten
		negative_digit = -power_ten

		if positive_digit > max_positive_digit:
			max_positive_digit = positive_digit
		if negative_digit > max_negative_digit:
			max_negative_digit = negative_digit

		correct_list.append((n_list, len_num, power_ten))

	eleven_dict = {}
	sum_dict = {}

	for n_list, len_num, power_ten in correct_list:

		# 1. ��С����Ϊ��㣬�������μ����������ֵĺ�
		for i in xrange(max_positive_digit):
			idx = len_num + power_ten - i - 1
			result_idx = i
			sum_dict.setdefault(result_idx, 0)

			if 0 <= idx < len_num:
				sum_dict[result_idx] += n_list[idx]

				# ����11���¼
				if sum_dict[result_idx] >= 11:
					sum_dict[result_idx] -= 11
					eleven_dict[result_idx] = eleven_dict.setdefault(result_idx, 0) + 1

		# 2. ��С����Ϊ��㣬�������μ���С�����ֵĺ�
		for i in xrange(max_negative_digit):
			idx = len_num + power_ten + i
			result_idx = -1-i
			sum_dict.setdefault(result_idx, 0)

			if -len_num < idx < len_num:
				sum_dict[result_idx] += n_list[idx]

				# ����11���¼
				if sum_dict[result_idx] >= 11:
					sum_dict[result_idx] -= 11
					eleven_dict[result_idx] = eleven_dict.setdefault(result_idx, 0) + 1

	# 3. L�����
	result_digit = {}

	# �����˺�Ϊ0�����
	result_digit[0] = 0

	max_idx = 0
	for idx in sorted(sum_dict.keys()):
		max_idx = idx
		result_digit[idx] = result_digit.get(idx, 0) + sum_dict[idx] + eleven_dict.get(idx, 0) + eleven_dict.get(idx-1, 0)

		# �����λ
		if result_digit[idx] > 9:
			result_digit[idx+1] = result_digit[idx] / 10

		result_digit[idx] = result_digit[idx] % 10

	# 4. ��������λ
	if max_idx in eleven_dict:
		result_digit[max_idx+1] = eleven_dict.get(max_idx)

	return map(lambda k: k[1], sorted(result_digit.iteritems(), key=lambda x:x[0], reverse=True)), -max_negative_digit


if __name__ == "__main__":
	tm = time.clock()
	print sum_list(["4.7856","0.00013","0.4"])
	print sum_list(["4785600","0.00013","0.4"])
	print sum_list(["4785600","00013","4"])
	print sum_list(["0", "0"])
	print sum_list(["1", "8", "9"])
	print time.clock() - tm