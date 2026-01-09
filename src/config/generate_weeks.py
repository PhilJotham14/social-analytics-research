"""
Generate the canonical week list for the project - UPDATED FOR 57 WEEKS

This script generates 57 weeks to satisfy Heavy LLM's interpretation:
"September 2024 – September 2025" = All Mondays in BOTH months

Coverage:
- September 2024: 5 Mondays (2024-09-02 through 2024-09-30)
- September 2025: 5 Mondays (2025-09-01 through 2025-09-29)
- Total: 57 weeks, 171 rows (57 × 3 platforms)

Change History:
- Original: 53 weeks (2024-09-02 to 2025-09-01)
- Updated: 57 weeks (2024-09-02 to 2025-09-29) per Heavy LLM Task 5 requirement
"""

from datetime import datetime, timedelta
import yaml
from pathlib import Path


def generate_week_list():
    """
    Generate 57 Monday dates to cover full September 2024 - September 2025.

    Why 57 weeks?
    - Client specification: "September 2024 – September 2025"
    - Heavy LLM interpretation: Include ALL Mondays in both months
    - September 2024: 5 Mondays (09-02, 09-09, 09-16, 09-23, 09-30)
    - September 2025: 5 Mondays (09-01, 09-08, 09-15, 09-22, 09-29)
    - Total coverage: 2024-09-02 through 2025-09-29 = 57 weeks

    Previous: 53 weeks (ended at 2025-09-01, only 1 Monday in Sep 2025)
    Updated: 57 weeks (ends at 2025-09-29, all 5 Mondays in Sep 2025)
    """
    weeks = []
    start = datetime(2024, 9, 2)  # First Monday of September 2024

    # Generate 57 weeks to include all September 2025 Mondays
    for i in range(57):
        week_start = start + timedelta(weeks=i)
        weeks.append(week_start.strftime("%Y-%m-%d"))

    return weeks


def main():
    weeks = generate_week_list()

    # Verify coverage - UPDATED FOR 57 WEEKS
    assert len(weeks) == 57, f"Expected 57 weeks, got {len(weeks)}"
    assert weeks[0] == "2024-09-02", f"Week 1 should be 2024-09-02, got {weeks[0]}"
    assert weeks[12] == "2024-11-25", f"Week 13 should be 2024-11-25, got {weeks[12]}"
    assert weeks[25] == "2025-02-24", f"Week 26 should be 2025-02-24, got {weeks[25]}"
    assert weeks[52] == "2025-09-01", f"Week 53 should be 2025-09-01, got {weeks[52]}"
    assert weeks[56] == "2025-09-29", f"Week 57 should be 2025-09-29, got {weeks[56]}"

    # Verify September 2024 coverage (5 Mondays)
    sep_2024 = [w for w in weeks if w.startswith("2024-09")]
    assert len(sep_2024) == 5, f"Expected 5 Sep 2024 Mondays, got {len(sep_2024)}"

    # Verify September 2025 coverage (5 Mondays)
    sep_2025 = [w for w in weeks if w.startswith("2025-09")]
    assert len(sep_2025) == 5, f"Expected 5 Sep 2025 Mondays, got {len(sep_2025)}"

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

    print("=" * 70)
    print("WEEK CONFIGURATION UPDATED TO 57 WEEKS")
    print("=" * 70)
    print(f"\nGenerated {len(weeks)} weeks")
    print(f"Coverage: {weeks[0]} to {weeks[-1]}")

    print(f"\nSeptember 2024 Mondays ({len(sep_2024)} weeks):")
    for w in sep_2024:
        print(f"  {w}")

    print(f"\nSeptember 2025 Mondays ({len(sep_2025)} weeks):")
    for w in sep_2025:
        print(f"  {w}")

    print(f"\nPilot weeks:")
    print(f"  Week 1:  {weeks[0]}")
    print(f"  Week 13: {weeks[12]}")
    print(f"  Week 26: {weeks[25]}")
    print(f"  Week 53: {weeks[52]}")
    print(f"  Week 57: {weeks[56]}")

    print(f"\n✅ Files updated:")
    print(f"  - src/config/weeks.yaml (57 weeks)")
    print(f"  - src/config/weeks.csv (57 weeks)")

    print(f"\n⚠️  NEXT STEPS:")
    print(f"  1. Collect GitHub data for 4 new weeks:")
    print(f"     python -m src.pipelines.run_github_week --week 2025-09-08")
    print(f"     python -m src.pipelines.run_github_week --week 2025-09-15")
    print(f"     python -m src.pipelines.run_github_week --week 2025-09-22")
    print(f"     python -m src.pipelines.run_github_week --week 2025-09-29")
    print(f"  2. Re-run full aggregation:")
    print(f"     python -m src.pipelines.run_aggregate_full --full")
    print(f"  3. Update documentation to reflect 57 weeks / 171 rows")


if __name__ == "__main__":
    main()
