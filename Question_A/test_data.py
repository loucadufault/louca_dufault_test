from Question_A import Line

overlapping = (
        (Line(1, 5), Line(2, 6)),
        (Line(5, 7), Line(3, 7)),
        (Line(-3, 6), Line(-7, -1)),
        (Line(2, 3), Line(2.5, 5.5))
        )

overlapping_edge = (
    (Line(-6, -4), Line(-5.5, -4.5)),
    (Line(1, 9), Line(5, 6)),
    (Line(5, 6), Line(1, 9)),
    (Line(1, 5), Line(1, 5)),
    (Line(1, 1), Line(1, 1)),
    (Line(1, 1), Line(2, 1)),
    (Line(0, 4), Line(4, 8)),
    (Line(4, 6.1), Line(5.9, 8)),
    (Line(5, 1), Line(2, 4))
    )
    
not_overlapping_edge = (
    (Line(4, 5.9), Line(6.1, 8)),
    (Line(1, 1), Line(2, 2)),
    (Line(-1, -5), Line(5, 1)),
)


not_overlapping = (
    (Line(1, 5), Line(6, 8)),
    (Line(1, 7), Line(-7, -1))
)