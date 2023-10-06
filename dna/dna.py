import csv
import sys


def main():
    # Check for command-line usage
    if len(sys.argv) < 2:
        print('Provide two command-line arguments')

    data_dict = {}
    # Read database file into a variable
    filename = sys.argv[1]
    with open(filename) as file:
        first_line = file.readline().rstrip().split(',')[1:]
        reader = csv.reader(file)
        for file in reader:
            user_dict = {}
            for i in range(len(first_line)):
                user_dict[first_line[i]] = file[1:][i]
            data_dict[file[0]] = user_dict

    DNA_file = sys.argv[2]
    # Read DNA sequence file into a variable
    with open(DNA_file) as filename:
        DNA_sequence = filename.read()

    # Find the longest match of each STR in DNA sequence
    dna_dict = {}
    for dna in first_line:
        largest = longest_match(DNA_sequence, dna)
        if largest > 0:
            dna_dict[dna] = largest

    # n = len(DNA_sequence)
    # counter = 0
    # while counter < n:
    #     first = find_first_DNA(first_line, DNA_sequence, counter)
    #     if not first:
    #         break
    #     first_dna = first[0]
    #     counter = first[1]
    #     count_dna = 0
    #     m = len(first_dna)
    #     while counter + m <= n and first_dna == DNA_sequence[counter:counter + m]:
    #         count_dna += 1
    #         counter += m
    #     if first_dna in dna_dict:
    #         if dna_dict[first_dna] < count_dna:
    #             dna_dict[first_dna] = count_dna
    #     else:
    #         dna_dict[first_dna] = count_dna

    for dna in first_line:
        if dna not in dna_dict:
            print('No match')
            return 1

    # Check database for matching profiles
    for key, value in data_dict.items():
        flag = True
        for dna in first_line:
            if int(value[dna]) != int(dna_dict[dna]):
                flag = False
                break
        if flag is True:
            print(key)
            return 0

    print('No match')

    return


# def find_first_DNA(DNA, s, counter):
#     n = len(s)
#     while counter < n:
#         for dna in DNA:
#             m = len(dna)
#             if s[counter:counter+m] == dna:
#                 return [dna, counter]
#         counter += 1


def longest_match(sequence, subsequence):
    """Returns length of the longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in sequence, return longest run found
    return longest_run


main()
