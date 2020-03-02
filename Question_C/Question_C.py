from LRUCache import LRUCache
from test_data import valid_max_sizes, valid_max_ages, invalid_max_sizes, invalid_max_ages, valid_keys, valid_values

import time

def create_mock_cache(max_size : int, max_age : int):
    return LRUCache(max_size, max_age)

def create_and_fill_mock_cache(max_size : int, max_age : int):
    cache = LRUCache(max_size, max_age)
    for i in range(max_size):
        cache.put(i, 'value{}'.format(i))
    return cache

def test_create_LRUCache():
    print("Test name:\ntest create LRUCache\n")
    test_cases = [valid_pair for valid_pair in zip(valid_max_sizes, valid_max_ages)]
    test_cases += [invalid_pair for invalid_pair in zip(invalid_max_sizes, valid_max_ages)]
    test_cases += [invalid_pair for invalid_pair in zip(valid_max_sizes, invalid_max_ages)]
    test_oracles = (LRUCache,) * len(valid_max_sizes) + (ValueError,) * (len(invalid_max_sizes) * 2)
    test_results = {"pass": 0, "fail": 0}

    for i, test_case in enumerate(test_cases):
        oracle = test_oracles[i]
        valid_max_size, valid_max_age = test_case
        result = None

        print("\nTest case {}:\nChecking whether {} and {} are valid arguments to initialize a LRUCache instance".format(i+1, *test_case), end=' ')

        try:
            result = LRUCache(valid_max_size, valid_max_age)
        except ValueError as e:
            result = e
        
        if (type(result) == oracle):
            print("passed", end=' ')
            test_results["pass"] += 1
        else:
            print("failed", end=' ')
            test_results["fail"] += 1

        print("(expected {}).".format(oracle))

    assert test_results["pass"] + test_results["fail"] == len(test_cases) # ensure all tests have been completed
    print("\nTest results:\n{} completed, {} failed".format(len(test_cases), test_results["fail"])) # display results

def test_IO_LRUCache():
    print("Test name:\ntest IO LRUCache\n")
    start = time.monotonic()
    assert len(valid_keys) == len(valid_values)
    max_size = len(valid_keys) + 1
    max_age = 86400

    num_test_cases = len(valid_keys) + 1
    test_results = {"pass": 0, "fail": 0}

    print("Creating a mock cache with max size {} and max age {}.".format(max_size, max_age))
    cache = create_mock_cache(max_size, max_age)
    assert cache.cache_info().max_size == max_size
    assert cache.cache_info().max_age == max_age
    assert cache.size() == 0

    print("Checking whether we can put mock data in the cache", end=' ')
    for valid_key, valid_value in zip(valid_keys, valid_values):
        cache.put(valid_key, valid_value)

    try:
        assert cache.cache_info().curr_size == len(valid_keys)
        print("passed", end=' ')
        test_results['pass'] += 1
    except AssertionError:
        print("failed", end=' ')
        test_results['fail'] += 1
    print("(expected the size of the cache to be {}).".format(len(valid_keys)))

    i=0
    for valid_key, valid_value in zip(valid_keys, valid_values):
        i+=1
        print("\nTest case {}:\nChecking whether we can get the mock data indexed by its key '{}' from the cache".format(i, valid_key), end=' ')
        try:
            assert cache.get(valid_key) == valid_value
            print("passed", end=' ')
            test_results['pass'] += 1
        except (KeyError, AssertionError):
            print("failed", end=' ')
            test_results['fail'] += 1
        print("(expected the data indexed by key '{}' to be in the cache and to have value '{}').".format(valid_key, valid_value))

    assert (time.monotonic() - start) < max_age
    assert test_results["pass"] + test_results["fail"] == num_test_cases # ensure all tests have been completed
    print("\nTest results:\n{} completed, {} failed".format(num_test_cases, test_results["fail"])) # display results

def test_MRU_LRUCache():
    pass

def test_eviction_LRUCache():
    pass

def test_capacity_LRUCache():
    print("Test name:\ntest capacity LRUCache\n")
    start = time.monotonic()
    max_size = 5
    max_age = 86400

    num_test_cases = 1
    test_results = {"pass": 0, "fail": 0}

    print("Creating a mock cache with max size {} and max age {} and filling it to capacity with mock data.".format(max_size, max_age))
    cache = create_and_fill_mock_cache(max_size, max_age)
    assert cache.cache_info().max_size == max_size
    assert cache.size() == max_size
    
    print("Checking whether the size of the cache remains {} even after putting more data in the cache".format(max_size), end=' ')
    for valid_key, valid_value in zip(valid_keys, valid_values):
        cache.put(valid_key, valid_value)

    try:
        assert cache.cache_info().max_size == max_size
        assert cache.size() == max_size
        print("passed", end=' ')
        test_results['pass'] += 1
    except AssertionError:
        print("failed", end=' ')
        test_results['fail'] += 1

    assert (time.monotonic() - start) < max_age

    print("(expected size of cache to remain {}).".format(max_size))
    assert test_results["pass"] + test_results["fail"] == num_test_cases # ensure all tests have been completed
    print("\nTest results:\n{} completed, {} failed".format(num_test_cases, test_results["fail"])) # display results

def test_expiry_LRUCache():
    print("Test name:\ntest expiry LRUCache\n")
    max_size = 5
    max_age = 5

    num_test_cases = 2
    test_results = {"pass": 0, "fail": 0}

    print("Creating a mock cache with max size {} and max age {} and filling it to capacity with mock data.".format(max_size, max_age))
    cache = create_and_fill_mock_cache(max_size, max_age)
    # cache does not have a miss_callback set
    start = time.monotonic()
    assert cache.cache_info().max_size == max_size
    assert cache.cache_info().max_age == max_age
    assert cache.size() == max_size

    print("Waiting {} seconds for all data in the cache to expire.\n...".format(max_age))
    time.sleep(max_age)

    end = time.monotonic()
    assert (end - start) > max_age

    print("Checking whether we are able to get any of the data in the cache after it has expired", end=' ')
    misses = 0
    for i in range(max_size):
        try:
            cache.get(i)
        except KeyError:
            misses += 1

    try:
        assert misses == max_size
        print("passed",end=' ')
        test_results['pass'] += 1
    except AssertionError:
        print("failed", end=' ')
        test_results['fail'] += 1
    print("(expected all {} get requests on the cache to raised KeyError as cache misses).".format(max_size))

    print("Checking whether the cache was emptied by the successive calls to get each item in the cache, since expired items should be removed from cache upon cache miss", end=' ')
    try:
        assert cache.size() == 0
        print("passed", end=' ')
        test_results['pass'] += 1
    except AssertionError:
        print("failed", end=' ')
        test_results['fail'] += 1
    print("(expected the cache to have size 0)")

    assert test_results["pass"] + test_results["fail"] == num_test_cases # ensure all tests have been completed
    print("\nTest results:\n{} completed, {} failed".format(num_test_cases, test_results["fail"])) # display results

def test():
    test_create_LRUCache()
    print('\n')
    test_IO_LRUCache()
    print('\n')
    test_MRU_LRUCache()
    print('\n')
    test_eviction_LRUCache()
    print('\n')
    test_capacity_LRUCache()
    print('\n')
    test_expiry_LRUCache()

def main():
    test()

if __name__=="__main__":
    main()