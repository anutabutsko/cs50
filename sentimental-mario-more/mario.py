num = 0
while num < 1 or num > 8:
    try:
        num = int(input('Input a positive integer between 1 and 8: '))
    except:
        print('That is not an integer. Try again.')
temp = num
for i in range(1, num + 1):
    temp -= 1
    print(' ' * temp + '#' * i + '  ' + i * '#')
