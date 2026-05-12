from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.schema_service import build_service


class PropertySchemaServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = build_service(ROOT)

    def test_summary_shape(self) -> None:
        summary = self.service.summary()
        self.assertEqual(summary["brokerage"], "Northstar Residential Group")
        self.assertGreater(summary["listingCount"], 0)

    def test_best_listing_is_newton_or_cambridge(self) -> None:
        listings = self.service.listings()
        self.assertIn(listings[0]["listingId"], {"lst-3001", "lst-3003"})

    def test_listing_schema_type(self) -> None:
        listing = self.service.listing("lst-3003")
        self.assertIsNotNone(listing)
        self.assertEqual(listing["schema"]["@type"], "RealEstateListing")


if __name__ == "__main__":
    unittest.main()
