# -*- coding: GBK -*-
import time
from multiplication import multiply
from utils import *

notepad_carry = {}

def add_digit_to_idx(digit, digit_idx, result):
	digit_result = result[digit_idx]

	carry = notepad_carry.get(digit_idx, 0)
	digit_result += (digit + carry)
	notepad_carry[digit_idx] = 0

	carry = digit_result / 10
	notepad_carry[digit_idx-1] = notepad_carry.setdefault(digit_idx-1, 0) + carry

	digit_result = digit_result % 10
	result[digit_idx] = digit_result

def square_loop(num_list, len_num, idx=0):
	if idx == len_num-1:
		u = get_multiply_unit(num_list[idx], num_list[idx])
		t = get_multiply_tens(num_list[idx], num_list[idx])
		return [t, u]

	# 1. ȡ�����λ����
	first_digit = num_list[idx]
	first_power_ten = len_num - idx - 1

	# 2. �����������ֵ�ƽ��
	result = square_loop(num_list, len_num, idx+1)
	len_base = len(result)

	# 3. �����㹻��0��׼�����ӷ�
	len_total = first_power_ten + first_power_ten + 2
	result = [0] * (len_total - len_base) + result

	# 4. �����λ�ֱ�������������˲�������Ȼ������ӵ�result��
	for i in xrange(len_num-1, idx, -1):
		num_power_ten = len_num - 1 - i
		num = 2 * first_digit * num_list[i]

		u_num = num % 10
		t_num = num / 10

		add_digit_to_idx(u_num, -1-num_power_ten-first_power_ten, result)
		add_digit_to_idx(t_num, -2-num_power_ten-first_power_ten, result)

	# 5. ���λƽ���󣬼ӵ�result��
	u_num = get_multiply_unit(first_digit, first_digit)
	t_num = get_multiply_tens(first_digit, first_digit)

	add_digit_to_idx(u_num, -1-first_power_ten-first_power_ten, result)
	add_digit_to_idx(t_num, -2-first_power_ten-first_power_ten, result)

	return result


def square(data):
	num_list = correct_number(data)
	len_num = len(num_list)
	return square_loop(num_list, len_num)

if __name__ == "__main__":
	tm = time.clock()
	print "square of 4432 = ", square("4432")
	print "square of 131223412341234112312312312323412341234 = ", square("131223412341234112312312312323412341234")
	print "square of 131223412341234112312312312323412341234 = ", 131223412341234112312312312323412341234 ** 2
	print time.clock() - tm