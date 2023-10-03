def is_digits(num):
    if num.isdigit():
        return True
    else:
        return False


def is_valid(num):
    num = num[::-1]
    temp1 = 0
    temp2 = 0
    for i in range(len(num)):
        if i % 2 == 0:
            temp1 += int(num[i])
        else:
            n = int(num[i]) * 2
            if len(str(n)) > 1:
                temp2 += int(str(n)[0]) + int(str(n)[1])
            else:
                temp2 += n
    if (temp1 + temp2) % 10 == 0:
        return True
    else:
        return False


def check_len(num):
    if len(num) in (13, 15, 16):
        return True
    else:
        return False


num = input('Enter your credit card number: ')

if is_digits(num) and check_len(num) and is_valid(num):
    if num[:2] in ('34', '37'):
        print('AMEX')
    elif num[0] == '4':
        print('VISA')
    elif num[:2] in ('51', '52', '53', '54', '55'):
        print('MASTERCARD')
    else:
        print('INVALID')
else:
    print('INVALID')
