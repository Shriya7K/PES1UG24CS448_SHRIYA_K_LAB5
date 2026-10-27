"""Unit tests for telecom tower maintenance tracker."""
import unittest
import tower_maintenance as tm


class TestTowerMaintenance(unittest.TestCase):
    """Test cases for tower_maintenance functions."""

    def test_add_and_snapshot(self):
        """Verify adding towers and taking snapshots."""
        initial_count = len(tm.snapshot())
        tm.add_tower("Test-Tower-North", 2020, 2)
        records = tm.snapshot()
        self.assertEqual(len(records), initial_count + 1)
        latest = records[-1]
        self.assertEqual(latest[1], "Test-Tower-North")
        self.assertEqual(latest[2], 2020)
        self.assertEqual(latest[3], 2)

    def test_overdue_detection(self):
        """Verify overdue logic detects towers unserviced for >= 2 years."""
        tm.add_tower("Test-Overdue-Site", 2021, 0)
        tm.add_tower("Test-Recent-Site", 2025, 0)
        overdue_sites = tm.overdue(2025)
        self.assertIn("Test-Overdue-Site", overdue_sites)
        self.assertNotIn("Test-Recent-Site", overdue_sites)

    def test_risk_level(self):
        """Verify risk levels based on fault threshold (> 3 is high)."""
        tm.add_tower("High-Risk-Site", 2023, 4)
        tm.add_tower("Normal-Risk-Site", 2023, 2)
        records = tm.snapshot()
        high_id = [r[0] for r in records if r[1] == "High-Risk-Site"][0]
        normal_id = [r[0] for r in records if r[1] == "Normal-Risk-Site"][0]

        self.assertEqual(tm.risk_level(high_id), "high")
        self.assertEqual(tm.risk_level(normal_id), "normal")
        self.assertEqual(tm.risk_level(99999), "normal")

    def test_service_tower(self):
        """Verify servicing resets faults, updates year, and increments.

        Checks that servicing updates records and counter properly.
        """
        tm.add_tower("Service-Target", 2019, 5)
        records = tm.snapshot()
        target_id = [r[0] for r in records if r[1] == "Service-Target"][0]

        initial_services = tm.SERVICE_TRACKER["count"]
        tm.service_tower(target_id, 2025)
        self.assertEqual(tm.SERVICE_TRACKER["count"], initial_services + 1)

        updated_records = tm.snapshot()
        target = [r for r in updated_records if r[0] == target_id][0]
        self.assertEqual(target[2], 2025)
        self.assertEqual(target[3], 0)


if __name__ == "__main__":
    unittest.main()
