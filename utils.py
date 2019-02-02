# -*- coding: GBK -*-
import time

def correct_number_from_string(raw_data, use_power):
	num = raw_data
	num = num.strip()
	num = num.replace(",", "")      # �������ŷָ���
	num = num.lstrip("0")           # ��ಹ��������

	power_ten = num.rfind("e+")
	if power_ten < 0:
		power_ten = 0
	else:
		num, power_ten = num[:power_ten], num[power_ten+2:]
		power_ten = int(power_ten)

	assert num.find("e+")<0, "%s is error number!" % (raw_data)

	num.strip(".")
	dot_pos = num.find(".")

	if dot_pos < 0:
		tmp = num.rstrip("0")
		power_ten += len(num) - len(tmp)
		num = tmp
	else:
		decimals_part = num[dot_pos+1:].rstrip("0")
		integer_part = num[:dot_pos]

		if len(decimals_part) > 0:
			num = integer_part + decimals_part
			power_ten -= len(decimals_part)
		else:
			tmp = integer_part.rstrip("0")
			power_ten += len(num) - len(tmp)
			num = tmp

	assert num.find(".")<0, "%s is error number!" % (raw_data)

	if use_power:
		return map(int, num), power_ten
	else:
		return map(int, num) + [0] * power_ten

# �����۵����֣��۵�������λΪ��λ��
# �� [45, 30, 21] -> [4,(5,3),(0,2),1] -> [4, 8, 2, 1]
def correct_number_from_list(raw_data, use_power):
	raw_list = raw_data
	len_raw = len(raw_list)

	num_list = []
	len_num = 0
	power_ten = 0

	is_integer = True

	carrys = {}
	for i in xrange(len_raw):
		idx = -1-i
		item = raw_list[idx]

		if item == '.':
			assert is_integer, "%s is error number!" % (raw_data)
			is_integer = False
			power_ten = -len(num_list)

		else:
			num = int(item)
			if idx in carrys:
				num += carrys.pop(idx)

			carry = num / 10
			if carry > 0:
				carrys[idx-1] = carrys.setdefault(idx-1, 0) + carry

			digit = (num) % 10
			if digit > 0:
				num_list.append(digit)
				len_num += 1
			else:
				if len(num_list) == 0:
					# �����������Ҳ�0���������У�ֻ����Ϊ10�ı���
					power_ten += 1
				else:
					num_list.append(digit)
					len_num += 1

	while carrys:
		key_list =  carrys.keys()

		for idx in sorted(key_list, reverse=True):
			num = carrys.pop(idx)
			if idx >= -len_num:
				num += num_list[idx]

			carry = num / 10
			if carry > 0:
				carrys[idx-1] = carrys.setdefault(idx-1, 0) + carry

			digit = (num) % 10
			if idx < -len_num:
				num_list.append(digit)
				len_num += 1
			else:
				num_list[idx] = digit

	if use_power:
		return num_list[::-1], power_ten
	else:
		return num_list[::-1] + [0] * power_ten

def correct_number_from_number(raw_data, use_power):
	if raw_data == 0:
		if use_power:
			return [0], 0
		else:
			return [0]

	num = raw_data
	power_ten = 0

	while num - int(num) > 0:
		power_ten -= 1
		num *= 10

	num = int(num)

	while num % 10 == 0:
		power_ten += 1
		num = num / 10

	if use_power:
		return map(int, str(num)), power_ten
	else:
		return map(int, str(num)) + [0] * power_ten

# ������������0-9��������ʾ�����ǵ���10������С���ļ򻯣������õ�10����
def correct_number(raw_data, use_power=False):
	if type(raw_data) is str:
		return correct_number_from_string(raw_data, use_power)

	if type(raw_data) is list or type(raw_data) is tuple:
		return correct_number_from_list(raw_data, use_power)

	if type(raw_data) is int or type(raw_data) is float:
		return correct_number_from_number(raw_data, use_power)

# �˻�����¼ ############################################################################################################

notepad_multiply = {}
notepad_addition = {}

# ������ֳ˻��ĸ�λ��
def get_multiply_unit(a, b):
	if a == 0 or b == 0:
		return 0

	if a > b:
		a, b = b, a
	key = (a, b)

	node = notepad_multiply.get(key)
	if node is None:
		num = a * b
		node = (num / 10, num % 10)
		notepad_multiply[key] = node

	return node[-1]

# ������ֳ˻���ʮλ��
def get_multiply_tens(a, b):
	if a == 0 or b == 0:
		return 0

	if a > b:
		a, b = b, a
	key = (a, b)

	node = notepad_multiply.get(key)
	if node is None:
		num = a * b
		node = (num / 10, num % 10)
		notepad_multiply[key] = node

	return node[0]

# ������ֵ������˻�
def get_multiply_num(a, b):
	if a == 0 or b == 0:
		return 0

	if a > b:
		a, b = b, a
	key = (a, b)

	node = notepad_multiply.get(key)
	if node is None:
		num = a * b
		node = (num / 10, num % 10)
		notepad_multiply[key] = node

	return node

# ������ּӷ��ĸ�λ��
def get_addition_unit(a, b):
	if a == 0:
		return b

	if b == 0:
		return a

	if a > b:
		a, b = b, a
	key = (a, b)

	node = notepad_addition.get(key)
	if node is None:
		num = a + b
		node = (num / 10, num % 10)
		notepad_addition[key] = node

	return node[-1]

# ������ּӷ���ʮλ��
def get_addition_tens(a, b):
	if a == 0 or b == 0:
		return 0

	if a > b:
		a, b = b, a
	key = (a, b)

	node = notepad_addition.get(key)
	if node is None:
		num = a + b
		node = (num / 10, num % 10)
		notepad_addition[key] = node

	return node[0]

########################################################################################################################

# ��һ�����ֵ����ֺ�
def digit_sum(num):
	# 0. ���л���֧�ִ�����
	num_list, multiplicand_power_ten = correct_number(num, True)

	result = 0
	for digit in num_list:

		# ��9����
		if digit == 9 or digit == 0:
			continue

		u = get_addition_unit(result, digit)
		t = get_addition_tens(result, digit)

		result = u + t

	return result

# �����б�ʾ�����ϳ�һ��������λ�������֪��
def get_num_from_list(ls):
	return int("".join(map(lambda k: str(k), ls)))

# ���˵������б�ʾ����������0
def list_strip_zero(ls):
	result = []
	len_result = 0

	for n in ls:
		if n > 0 or len_result > 0:
			result.append(n)
			len_result += 1

	return result

# num_b�Ƿ���Լ�ȥnum_a
def is_smaller_or_equal(num_a, num_b):
	len_a = len(num_a)
	len_b = len(num_b)

	if len_a != len_b:
		return len_a < len_b

	for i in xrange(len_a):
		if num_b[i] < num_a[i]:
			return False
		if num_b[i] > num_a[i]:
			return True
	return True

if __name__ == "__main__":
	tm = time.clock()
	print get_multiply_unit(10, 1)
	print digit_sum("901341234556134801237123123")
	print "[40,23,45] ->", correct_number([40,23,45])
	print "[26,48,65] ->", correct_number([26,48,65])
	print "[440,23,'.',45] ->", correct_number([440,23,'.',45],True)
	print time.clock() - tm
