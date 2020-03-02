invalid_keys = (
    [1, 2, 3],
    {'a': 1, 'b': 2}
)

valid_keys = (
    (1, 4.6, 7),
    (4),
    1,
    123456,
    'abcdef',
    'a',
    '123'
)

valid_values = (
    (1, 2, 3),
    'data',
    '123',
    123456,
    {'a': 1, 'b': 2},
    [1, 2, 3],
    ['part1', 'part2']
)

valid_max_ages = (
    1,
    10,
    60,
    3600
)

invalid_max_ages = (
    200.46,
    -60,
    0,
    -45.6
)

valid_max_sizes = (
    5,
    20,
    256,
    1024
)

invalid_max_sizes = (
    256.5,
    -89,
    0,
    -34.9
)