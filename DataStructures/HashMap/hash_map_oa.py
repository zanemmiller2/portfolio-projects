# Name:
# OSU Email:
# Course: CS261 - Data Structures
# Assignment:
# Due Date:
# Description:


from a6_include import *


class HashEntry:

    def __init__(self, key: str, value: object):
        """
        Initializes an entry for use in a hash map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.key = key
        self.value = value
        self.is_tombstone = False

    def __str__(self):
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return f"K: {self.key} V: {self.value} TS: {self.is_tombstone}"


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses Quadratic Probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()

        for _ in range(capacity):
            self.buckets.append(None)

        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            out += str(i) + ': ' + str(self.buckets[i]) + '\n'
        return out

    def compute_hash_index(self, key):
        """
        Computes and returns the initial hash_index and modifiable
        hash_index for probing
        """

        # compute the hash index
        hash_value = self.hash_function(key)

        # calculate the initial hash index to be used as immutable for probing
        initial_hash_index = hash_value % self.capacity

        # use hash_index as the mutable value for probing
        hash_index = initial_hash_index

        return hash_index, initial_hash_index

    def compute_next_hash_index(self, j, initial_hash_index):
        """
        Calculates the next index in the quadratic probe. Returns incremented
        j value, and the next hash_index
        """

        j = j + 1
        hash_index = (initial_hash_index + j ** 2) % self.capacity

        return hash_index, j

    def clear(self) -> None:
        """ Clears the contents of the hash map """

        for num in range(self.capacity):
            # set occupied buckets to None and decrement size
            if self.buckets[num] is not None:
                self.buckets[num] = None
                self.size = self.size - 1

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key.
        Returns None if the key is not in the hash map.
        """

        # compute the initial_hash_index and hash_index for probing
        hash_index, initial_hash_index = self.compute_hash_index(key)

        # key is not found in table
        if not self.contains_key(key):
            return None

        # key is in table
        j = 0
        while self.buckets[hash_index].key != key:
            # probe for the given key
            hash_index, j = self.compute_next_hash_index(j, initial_hash_index)

        # Returns the value associated with the given key
        return self.buckets[hash_index].value

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash table. If the given key already
        exists in the hash table, its associated value will be replaced with
        the new value. If the given key is not in the hash map, a key/value
        pair will be added. If the load factor is greater than 0.5, the table
        will be resized prior to inserting the new key/value.
        """

        # calculate table load and resize if necessary
        if self.table_load() >= 0.5:
            # set new_capacity to 2x current capacity
            new_capacity = self.capacity * 2
            # resize
            self.resize_table(new_capacity)

        # compute the initial_hash_index and hash_index for probing
        hash_index, initial_hash_index = self.compute_hash_index(key)

        # key already exists
        if self.contains_key(key):
            # key
            if self.buckets[hash_index].key == key:
                # overwrite existing value
                self.buckets[hash_index].value = value

            else:
                # probe for the next available index
                j = 0
                while self.buckets[hash_index].key != key:
                    # probe for the given key
                    hash_index, j = \
                        self.compute_next_hash_index(j, initial_hash_index)

                # overwrite existing value
                self.buckets[hash_index].value = value

        # key is not already in table
        else:

            # probe for the next available index
            j = 0
            while self.buckets[hash_index] is not None:

                # bucket is occupied by a tombstone
                if self.buckets[hash_index].is_tombstone is True:
                    self.buckets.set_at_index(hash_index, HashEntry(key, value))
                    return

                # probe for the given key
                hash_index, j = \
                    self.compute_next_hash_index(j, initial_hash_index)

            # Add key/value to hash table
            self.buckets.set_at_index(hash_index, HashEntry(key, value))

            # increment size
            self.size = self.size + 1

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        If the key is not in the hash map, the method does nothing
        """

        # key is not in hash map, method does nothing
        if not self.contains_key(key):
            return None

        # compute the initial_hash_index and hash_index for probing
        hash_index, initial_hash_index = self.compute_hash_index(key)

        # probe for the given key
        j = 0
        while self.buckets[hash_index].key != key:
            # probe for the given key
            hash_index, j = self.compute_next_hash_index(j, initial_hash_index)

        # set bucket to tombstone and decrement the size
        self.buckets[hash_index].is_tombstone = True
        self.size = self.size - 1

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map. False otherwise.
        """

        # compute the initial_hash_index and hash_index for probing
        hash_index, initial_hash_index = self.compute_hash_index(key)

        j = 0           # initializes the j counter for quadratic probing
        counter = 0     # counts the number of elements already searched

        # Probe the DA until the key is found, or the entire table is searched
        while (self.buckets[hash_index]) and (counter < self.capacity):

            # key is found
            if ((self.buckets[hash_index].is_tombstone is False)
                    and (self.buckets[hash_index].key == key)):

                return True

            # key not found yet - probe for the key
            elif ((self.buckets[hash_index].key != key)
                  or (self.buckets[hash_index].is_tombstone is True)):

                # probe for the given key
                hash_index, j = \
                    self.compute_next_hash_index(j, initial_hash_index)
                counter = counter + 1

        # key is not in table
        return False

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table
        (total buckets - filled buckets)
        """

        return self.capacity - self.size

    def table_load(self) -> float:
        """ Returns the current hash table load factor (elements / buckets) """

        return self.size / self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. All existing key/value
        pairs remain in the new hash map, and all hash table links will be
        rehashed. If the new capacity is less than 1 or less than the current
        size, the method does nothing
        """

        # Function does nothing if new capacity is < 1 or < current size
        if (new_capacity < 1) or (new_capacity < self.size):
            return None

        # initialize new HashMap with the new capacity & existing hash_function
        new_hashMap = HashMap(new_capacity, self.hash_function)

        # Generate a list of keys in the hash map for rehashing
        key_array = self.get_keys()

        # Re-hash the keys in the new hash map
        for num in range(key_array.length()):
            key = key_array[num]
            value = self.get(key)
            new_hashMap.put(key, value)

        # point global buckets to the new buckets
        self.buckets = new_hashMap.buckets
        # Update capacity to new_capacity
        self.capacity = new_hashMap.capacity

    def get_keys(self) -> DynamicArray:
        """
        Returns a DynamicArray that contains all the keys stored in the hash
        map.
        """

        key_array = DynamicArray()

        # traverse the array and append the keys to key_array
        for num in range(self.capacity):

            # An bucket is occupied by a valid object
            if ((self.buckets[num] is not None)
                    and (self.buckets[num].is_tombstone is False)):

                # Append the key to key_array
                key_array.append(self.buckets[num].key)

        return key_array

if __name__ == "__main__":

    m = HashMap(100, hash_function_1)
    m.put('key1', 11)
    print(m)
    m.remove('key1')
    print(m)
    print(m.get('key1'))
    m.put('key1', 12)
    print(m)
    print(m.get_keys())

    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.size, m.capacity)
    #
    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # # this test assumes that put() has already been correctly implemented
    # m = HashMap(50, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.size, m.capacity)
    #
    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.table_load())
    # m.put('key1', 10)
    # print(m.table_load())
    # m.put('key2', 20)
    # print(m.table_load())
    # m.put('key1', 30)
    # print(m.table_load())
    #
    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(50, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(m.table_load(), m.size, m.capacity)
    #
    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.size, m.capacity)
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.size, m.capacity)
    # m.clear()
    # print(m.size, m.capacity)
    #
    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(50, hash_function_1)
    # print(m.size, m.capacity)
    # m.put('key1', 10)
    # print(m.size, m.capacity)
    # m.put('key2', 20)
    # print(m.size, m.capacity)
    # m.resize_table(100)
    # print(m.size, m.capacity)
    # m.clear()
    # print(m.size, m.capacity)
    #
    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(50, hash_function_1)
    # for i in range(150):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         print(m.empty_buckets(), m.table_load(), m.size, m.capacity)
    #
    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(40, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), m.table_load(), m.size, m.capacity)
    #
    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(10, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))
    #
    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(75, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.size, m.capacity)
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)
    #
    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(30, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    #
    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(150, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.size, m.capacity)
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)
    #
    # print("\nPDF - remove example 1")
    # print("----------------------")
    # m = HashMap(50, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # m.remove('key4')
    #
    # print("\nPDF - resize example 1")
    # print("----------------------")
    # m = HashMap(20, hash_function_1)
    # m.put('key1', 10)
    # print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    # m.resize_table(30)
    # print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    #
    # print("\nPDF - resize example 2")
    # print("----------------------")
    # m = HashMap(75, hash_function_2)
    # keys = [i for i in range(1, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.size, m.capacity)
    #
    # for capacity in range(111, 1000, 117):
    #     m.resize_table(capacity)
    #
    #     m.put('some key', 'some value')
    #     result = m.contains_key('some key')
    #     m.remove('some key')
    #
    #     for key in keys:
    #         result &= m.contains_key(str(key))
    #         result &= not m.contains_key(str(key + 1))
    #     print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))
    #
    # print("\nPDF - get_keys example 1")
    # print("------------------------")
    # m = HashMap(10, hash_function_2)
    # for i in range(100, 200, 10):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys())
    #
    # m.resize_table(1)
    # print(m.get_keys())
    #
    # m.put('200', '2000')
    # m.remove('100')
    # m.resize_table(2)
    # print(m.get_keys())
