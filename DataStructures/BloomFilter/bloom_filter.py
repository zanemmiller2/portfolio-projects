# Author: Zane Miller
# Date: 04/13/2022
# Email: millzane@oregonstate.edu
# Description: Bloom filter implementation for detecting weak password
#       selection.

# Notes:
#   - Include bad_password_dictionary.txt in same directory as
#       bloom_filter.py

#   - Install py modules :
#       - pip install bitarray
#       - pip install pycryptodomex
#            - Note on pycryptodomex: I have had difficulty getting the Crypto.Hash modules to load.
#              At times, I have had to pip uninstall pycrypto, pycryptodome, and pycryptodomex and
#              then re-install pycryptodomex

# Command line execution:
#   - python3 bloom_filter.py [bad_password_dictionary] [test_file]

# Resources:
#   - https://en.wikipedia.org/wiki/Bloom_filter#Optimal_number_of_hash_functions
#   - https://www.geeksforgeeks.org/bloom-filters-introduction-and-python-implementation/
#   - https://corte.si/posts/code/bloom-filter-rules-of-thumb/
#   - https://pages.cs.wisc.edu/~cao/papers/summary-cache/node8.html
#   - https://stackoverflow.com/questions/658439/how-many-hash-functions-does-my-bloom-filter-need


import math
import random
import sys

from bitarray import bitarray
from Cryptodome.Hash import SHA224, SHA256, SHA384, SHA512, SHA3_256, \
    SHA3_224, SHA3_384, SHA3_512, BLAKE2b, BLAKE2s


# Calculate size of bad bad_password_dictionary list (B)
class BloomFilter:
    """
    Represents a Bloom Filter of a bad_password_list for used to check passwords in a test_file
    with a default false positive probability of 1%.
    """

    def __init__(self, input_dictionary, test_file, fp=0.01):
        """
        Creates a bloom filter from a bad_password_list with a provided false
        positive probability rate and desired number of hash functions
        """

        # bad_password_dictionary file descriptor of bad passwords
        self.bp_dictionary = input_dictionary
        self.password_check_dictionary = test_file

        # false positive probability rate
        self.fp = fp

        # Initialize/create array of bad passwords from file
        self.bp_list = []
        self.create_bp_list()

        # Initialize/create array of passwords to check from file
        self.password_check_list = []
        self.create_password_check_list()

        # Create a bit array of optimal size (N = B * ln(2) / ln^2(2)) and set all bits to 0
        self.N = int(self.get_optimal_bit_array_size())
        self.bit_array = bitarray(self.N)
        self.bit_array.setall(0)

        # set the number of hash functions (k) to use in range [0, 10] based on defined fp
        self.k = self.get_optimal_k()

        # Define available hash functions list
        self.hash_functions_available = [SHA224, SHA256, SHA384, SHA512,
                                         SHA3_256, SHA3_224, SHA3_384,
                                         SHA3_512, BLAKE2b, BLAKE2s]

        # Initialize hash objects for bloom creation and password check
        self.hash_functions_bloom = []
        self.hash_functions_check = []
        self.set_hash_functions()

        # Size ratio m/n
        self.size_ratio = self.get_size_ratio()

    def create_bp_list(self):
        """ Creates a list of bad_passwords from file """
        with open(self.bp_dictionary, 'rb') as bp_file:
            for line in bp_file:
                self.bp_list.append(line.strip())

    def create_password_check_list(self):
        """ Creates a list of passwords from input file """
        # Get list of passwords to test
        with open(self.password_check_dictionary, 'rb') as pc_file:
            for line in pc_file:
                self.password_check_list.append(line.strip())

    def set_hash_functions(self):
        """
        Dynamically set list of random hash functions from list of available
        hash functions
        """
        num = 0
        while num < self.k:
            hash_func = random.choice(self.hash_functions_available).new()
            if hash_func not in self.hash_functions_bloom:
                self.hash_functions_bloom.append(hash_func)
                self.hash_functions_check.append(hash_func)
                num += 1

    def build_bloom_filter(self):
        """ Hash the list of bad passwords into the bit array """
        print("Building Bloom Filter ... please wait")
        for bp in self.bp_list:
            for num in range(self.k):
                # Compute and set 1st hash index
                hash_func = self.hash_functions_bloom[num].new()
                hash_func.update(bp)
                set_bit = int(hash_func.hexdigest(), 16) % len(self.bit_array)
                self.bit_array[set_bit] = 1

    def is_bad_password(self):
        """ Checks if supplied password is a bad password or no """
        # Test if each password in input is bad password
        print("Checking for bad passwords ...")
        for new_password in self.password_check_list:
            bits_set = []

            # Compute each hash index per password check
            for num in range(self.k):
                hash_func_check = self.hash_functions_check[num].new()
                hash_func_check.update(new_password)
                set_bit = int(hash_func_check.hexdigest(), 16) % len(
                    self.bit_array)
                bits_set.append(set_bit)

            counter = -1
            for index in bits_set:
                counter += 1

                # Found a bit not set to 1
                if self.bit_array[index] == 0:
                    # Error checking - password is in bp list but bloom filter said it wasn't
                    if new_password in self.bp_list:
                        print_temp = "error: false negative"

                    # Password was not in bp list and bloom filter said it wasn't
                    else:
                        print_temp = "correct"

                    print(new_password, " - no: ", print_temp)
                    counter = -1
                    break

                # All bits are 1 and last bit was checked
                if counter == len(bits_set) - 1:
                    # password not in bp list but hashed to value that was
                    if new_password not in self.bp_list:
                        print_temp_2 = "false positive"

                    # password is in bp list and was hashed to value that was
                    else:
                        print_temp_2 = "correct"

                    print(new_password, " - maybe: ", print_temp_2)
                    counter = -1

    def get_num_bp(self):
        """ Get the number of bad passwords (B) in bad_password_list"""
        return len(self.bp_list)

    def get_optimal_bit_array_size(self):
        """
        Calculates the optimal number of bits (N = B * ln(2) / ln^2(2) based on
        the requested false positive probability (fp)
        """
        return abs(self.get_num_bp() * math.log(self.fp) / (math.log(2) ** 2))

    def get_optimal_k(self):
        """ Calculate the optimal number of hash functions to use """
        self.k = math.log(2) * self.N / self.get_num_bp()

        if self.k > 10:
            self.k = 10

        return int(self.k)

    def get_fp_probability(self):
        """ Get the false positive probability rate """
        return self.fp

    def get_size_ratio(self):
        """ Get the ratio of size_bit_array / size_input """
        return len(self.bit_array) / len(self.bp_list)

    def print_diagnostics(self):
        """ Prints variable initializations """
        title = "----------------------------Initializations----------------------------"
        print(f"{title:^}")
        # print k
        print(f"* There are {self.k:n} hash functions being used.")
        # print number of inputs
        print(
            f"* There were {self.get_num_bp():n} bad passwords in {self.bp_dictionary}.")
        # print size of the bit array
        print(f"* The created bit array is {len(self.bit_array):n} bits long.")
        # print size ratio
        print(f"* There are {self.size_ratio:.2f} bits per input.")
        # print fp
        print(
            f"* The expected false positive probability rate is {(self.fp):.3%}")
        print(
            "-----------------------------------------------------------------------")


def main():
    args = sys.argv[1:]
    input_dictionary = args[0]
    password_test_file = args[1]
    if len(args) > 2:
      fp = float(args[2])
      bf = BloomFilter(input_dictionary, password_test_file, fp=fp)
    else:
      bf = BloomFilter(input_dictionary, password_test_file)
    bf.print_diagnostics()
    bf.build_bloom_filter()
    bf.is_bad_password()


if __name__ == '__main__':
    main()
