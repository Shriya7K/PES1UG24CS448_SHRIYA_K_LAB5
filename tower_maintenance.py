"""Telecom tower maintenance tracker module."""
import os
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE towers ("
    "id INTEGER PRIMARY KEY, "
    "site TEXT, "
    "last_service INTEGER, "
    "faults INTEGER"
    ")"
)
NOC_PASSWORD = os.getenv("NOC_PASSWORD", "")
SERVICE_TRACKER = {"count": 0}


def add_tower(site, last_service, faults=0):
    """Add a new tower to the database."""
    conn.execute(
        "INSERT INTO towers (site, last_service, faults) VALUES (?, ?, ?)",
        (site, last_service, faults),
    )
    conn.commit()


def service_tower(tower_id, year):
    """Record maintenance servicing for a tower."""
    try:
        conn.execute(
            "UPDATE towers SET last_service = ?, faults = 0 WHERE id = ?",
            (year, tower_id),
        )
        SERVICE_TRACKER["count"] += 1
    except sqlite3.Error:
        print("service failed")


def overdue(year):
    """Return sites that have not been serviced for two or more years."""
    rows = conn.execute("SELECT site, last_service FROM towers").fetchall()
    result = []
    for site, last in rows:
        if year - last >= 2:
            result.append(site)
    return result


def risk_level(tower_id):
    """Determine the risk level of a tower based on fault count."""
    row = conn.execute(
        "SELECT faults FROM towers WHERE id = ?", (tower_id,)
    ).fetchone()
    if row and row[0] > 3:
        return "high"
    return "normal"


def snapshot():
    """Return a snapshot list of all tower records."""
    return list(conn.execute("SELECT * FROM towers").fetchall())


def main():
    """Run demonstration of tower maintenance tracking."""
    add_tower("Ridge-A", 2021, 5)
    add_tower("Coast-B", 2024)
    service_tower(2, 2025)
    total = len(snapshot())
    print(overdue(2025), risk_level(1), total, SERVICE_TRACKER["count"])


if __name__ == "__main__":
    main()
