valid_version_strings = ("1", "1.0", "0.1" "1.2.9", "0.11", "9.5b", "4.21.6ALPHA")
invalid_version_strings = ("1.5.", ".450.4", "3.4..56", "1.2_081", "1.5BETAv2.91")

greater = (
    ("1.0.4", "1.0.3"),
    ("4", "1"),
    ("2.4.12", "2.4.9"),
)

greater_edge = (
    ("1.34.3.2.121.64.78.667.999", "1.34.3.2.121.64.78.667.111"),
    ("2.34", "2"),
    ("2.9", "2.0"),
)
equal = ()
equal_edge = (
    ("12.081", "12.81"),
    ("8.4.0", "8.4"),
    ("17.3mac", "17.3MAC"),
    ("12b", "12B"),
)
lesser_edge = ()
lesser = ()
