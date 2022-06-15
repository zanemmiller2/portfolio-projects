# Name: Zane Miller
# OSU Email: millzane@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - Hash Map
# Due Date: 03/11/2022
# Description: HashMap implementation with
#   Open Addressing and Quadratic Probing


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

    def clear(self) -> None:
        """ Clears the contents of the hash map """

        for num in range(self.capacity):

            if self.buckets[num] is not None:
                self.buckets[num].key = None
                self.buckets[num].value = None
                self.buckets[num].is_tombstone = True
                self.size = self.size - 1


    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key.
        Returns None if the key is not in the hash map.
        """

        # compute the hash index
        hash_value = self.hash_function(key)
        initial_hash_index = hash_value % self.capacity
        hash_index = initial_hash_index

        # key is not found in table
        if not self.buckets[hash_index]:
            return None

        # key is found - return value
        hash_index = initial_hash_index
        j = 0
        while self.buckets[hash_index].key != key:

            j = j + 1
            hash_index = initial_hash_index + j ** 2

            if hash_index >= self.capacity:
                hash_index = hash_index % self.capacity

        return self.buckets[hash_index].value


    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash table. If the given key already
        exists in the hash table, its associated value will be replaced with
        the new value. If the given key is not in the hash map, a key/value
        pair will be added. If the load factor is greater than 0.5, the table
        will be resized prior to inserting the new key/value.
        """
        # remember, if the load factor is greater than 0.5,
        # resize the table before putting the new key/value pair
        #
        # quadratic probing required


        # compute the hash index
        hash_value = self.hash_function(key)
        initial_hash_index = hash_value % self.capacity
        hash_index = initial_hash_index

        # table is empty at initial hash index - insert
        if self.buckets[hash_index] is None:

            self.size = self.size + 1
            # Checks table load factor

            if self.table_load() > 0.5:
                new_capacity = 2 * self.capacity
                self.resize_table(new_capacity)

            else:
                self.buckets.set_at_index(hash_index, HashEntry(key, value))

        # key exists in table - overwrite existing value
        elif self.buckets[hash_index].key == key:
            self.buckets[hash_index].value = value
            return

        # table is occupied at initial hash index - find next available
        # index and insert
        else:
            j = 0
            self.size = self.size + 1
            # Checks table load factor
            if self.table_load() > 0.5:
                new_capacity = 2 * self.capacity
                self.resize_table(new_capacity)

            while self.buckets[hash_index] is not None:

                if self.buckets[hash_index].key == key:
                    self.buckets[hash_index].value = value
                    self.size = self.size - 1
                    return

                j = j + 1
                hash_index = initial_hash_index + j ** 2

                if hash_index >= self.capacity:
                    hash_index = hash_index % self.capacity

            self.buckets.set_at_index(hash_index, HashEntry(key, value))

    def remove(self, key: str) -> None:
        """
        TODO: Write this implementation
        """
        # quadratic probing required
        pass

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map. False otherwise.
        """
        # quadratic probing required

        # compute the hash index
        hash_value = self.hash_function(key)
        initial_hash_index = hash_value % self.capacity
        hash_index = initial_hash_index

        if self.buckets[hash_index] is None:
            return False

        while self.buckets[hash_index].key is not None:







    def empty_buckets(self) -> int:
        """ Returns the number of empty buckets in the hash table """

        return self.capacity - self.size

    def table_load(self) -> float:
        """ Returns the current hash table load factor """

        # total number of elements / total number of buckets
        return self.size / self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. All existing key/value
        pairs remain in the new hash map, and all hash table links will be
        rehashed. If the new capacity is less than 1, the method does nothing
        """

        # Function does nothing if new capacity is less than 1
        if new_capacity < 1:
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
        self.capacity = new_capacity

    def get_keys(self) -> DynamicArray:
        """
        Returns a DynamicArray that contains all the keys stored in the hash
        map.
        """

        key_array = DynamicArray()

        for num in range(self.capacity):
            if self.buckets[num]:
                key_array.append(self.buckets[num].key)

        return key_array


if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    # this test assumes that put() has already been correctly implemented
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
