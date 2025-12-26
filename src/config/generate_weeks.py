# """Generate the canonical 52-week list for the project"""

# from datetime import datetime, timedelta
# import yaml
# from pathlib import Path


# def generate_week_list():
#     """Generate 52 Monday dates from 2024-09-02 to 2025-09-01"""
#     weeks = []
#     start = datetime(2024, 9, 2)  # First Monday

#     for i in range(52):
#         week_start = start + timedelta(weeks=i)
#         weeks.append(week_start.strftime("%Y-%m-%d"))

#     return weeks


# def main():
#     weeks = generate_week_list()

#     # Verify
#     assert len(weeks) == 52
#     assert weeks[0] == "2024-09-02"  # Week 1
#     assert weeks[12] == "2024-11-25"  # Week 13
#     assert weeks[25] == "2025-02-24"  # Week 26
#     assert weeks[51] == "2025-08-25"  # Week 52 (52 weeks = 364 days from start)

#     # Write YAML
#     output = {"weeks": weeks}
#     yaml_path = Path("src/config/weeks.yaml")
#     yaml_path.parent.mkdir(parents=True, exist_ok=True)

#     with open(yaml_path, "w") as f:
#         yaml.dump(output, f, default_flow_style=False)

#     # Write CSV
#     csv_path = Path("src/config/weeks.csv")
#     with open(csv_path, "w") as f:
#         f.write("week_start\n")
#         for w in weeks:
#             f.write(f"{w}\n")

#     print(f"Generated {len(weeks)} weeks")
#     print(f"Pilot weeks: {weeks[0]}, {weeks[12]}, {weeks[25]}, {weeks[51]}")


# if __name__ == "__main__":
#     main()
"""Generate the canonical week list for the project - CORRECTED VERSION"""
from datetime import datetime, timedelta
import yaml
from pathlib import Path


def generate_week_list():
    """
    Generate 53 Monday dates to cover Sep 2024 - Sep 2025.

    Why 53 weeks?
    - Coverage period: Sep 2, 2024 to Sep 1, 2025 (full year)
    - 52 weeks = 364 days (ends Aug 25, 2025 - 1 week short!)
    - 53 weeks = 371 days (ends Sep 1, 2025 - covers full period)
    """
    weeks = []
    start = datetime(2024, 9, 2)  # First Monday (Week 1)

    # Generate 53 weeks to cover the full Sep 2024 - Sep 2025 period
    for i in range(53):
        week_start = start + timedelta(weeks=i)
        weeks.append(week_start.strftime("%Y-%m-%d"))

    return weeks


def main():
    weeks = generate_week_list()

    # Verify pilot weeks and coverage
    assert len(weeks) == 53, f"Expected 53 weeks, got {len(weeks)}"
    assert weeks[0] == "2024-09-02", f"Week 1 should be 2024-09-02, got {weeks[0]}"
    assert weeks[12] == "2024-11-25", f"Week 13 should be 2024-11-25, got {weeks[12]}"
    assert weeks[25] == "2025-02-24", f"Week 26 should be 2025-02-24, got {weeks[25]}"
    assert weeks[52] == "2025-09-01", f"Week 53 should be 2025-09-01, got {weeks[52]}"

    # Write YAML
    output = {"weeks": weeks}
    yaml_path = Path("src/config/weeks.yaml")
    yaml_path.parent.mkdir(parents=True, exist_ok=True)

    with open(yaml_path, "w") as f:
        yaml.dump(output, f, default_flow_style=False)

    # Write CSV
    csv_path = Path("src/config/weeks.csv")
    with open(csv_path, "w") as f:
        f.write("week_start\n")
        for w in weeks:
            f.write(f"{w}\n")

    print(f"Generated {len(weeks)} weeks")
    print(f"Coverage: {weeks[0]} to {weeks[-1]}")
    print(f"Pilot weeks:")
    print(f"  Week 1:  {weeks[0]}")
    print(f"  Week 13: {weeks[12]}")
    print(f"  Week 26: {weeks[25]}")
    print(f"  Week 53: {weeks[52]}")


if __name__ == "__main__":
    main()
