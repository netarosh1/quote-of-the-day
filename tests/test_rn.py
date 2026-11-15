import calendar
import json
import runpy
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
generate_data = runpy.run_path(
    str(ROOT / "scripts" / "bin" / "rn")
)["generate_data"]


class GenerateDataTests(unittest.TestCase):
    def test_checked_in_quote_data_is_valid_and_reachable(self):
        quotes = json.loads((ROOT / "quotes.json").read_text(encoding="utf-8"))
        mapped_indices = set()

        for month in range(1, 13):
            data = json.loads((ROOT / "quotes" / f"{month}.json").read_text())
            expected_days = {
                str(day) for day in range(1, calendar.monthrange(2000, month)[1] + 1)
            }
            self.assertEqual(set(data), expected_days)
            mapped_indices.update(data.values())

        self.assertEqual(mapped_indices, set(range(len(quotes))))

    def test_maps_every_calendar_day_including_leap_day(self):
        data = generate_data(47)

        for month in range(1, 13):
            expected_days = {
                str(day) for day in range(1, calendar.monthrange(2000, month)[1] + 1)
            }
            self.assertEqual(set(data[month]), expected_days)

    def test_maps_every_quote_index(self):
        data = generate_data(47)

        self.assertEqual(
            {index for month in data.values() for index in month.values()},
            set(range(47)),
        )


if __name__ == "__main__":
    unittest.main()
