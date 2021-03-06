valid_version_strings = ("1", "1.0", "0.1" "1.2.9", "0.11", "9.5b", "4.21.6ALPHA")
invalid_version_strings = ("1.5.", ".450.4", "3.4..56", "1.2_081", "1.5BETAv2.91", "4.67.macversion")

greater = (
    ("1.0.4", "1.0.3"),
    ("4", "1"),
    ("2.4.12", "2.4.9"),
    ("12b", "12a"),
)

greater_edge = (
    ("1.34.3.2.121.64.78.667.999", "1.34.3.2.121.64.78.667.111"),
    ("2.34", "2"),
    ("2.9", "2.0"),
    ("12b", "12A"),
    ("0.0.0.0009", "0.0.0.0001"),
    ("2.16", "2.16BETA"),
)

equal = (
    ("2.4.1", "2.4.1"),
    ("0.12b", "0.12b"),
    ("0.0", "0.0"),
    ("1.0.0", "1.0.0")
)

equal_edge = (
    ("12.081", "12.81"),
    ("1.2.3.4", "1.2.3.4.000.999"),
    ("2.700osx", "2.7osx"),
    ("8.4.0", "8.4"),
    ("17.3mac", "17.3MAC"),
    ("12b", "12B"),
)

lesser_edge = (
    ("1.2.3.4.000", "1.2.3.4.000.999"),
    ("1.2.3.4", "1.2.3.4.001.999"),
)
lesser = ()


# ("", ""),