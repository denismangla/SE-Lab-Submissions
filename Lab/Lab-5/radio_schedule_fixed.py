"""Manage a radio station's programme schedule."""

import sqlite3


class RadioSchedule:
    """Store and manage programme slots in an in-memory database."""

    def __init__(self) -> None:
        """Create the schedule database and its slots table."""
        self._connection = sqlite3.connect(":memory:")
        self._connection.execute(
            """
            CREATE TABLE slots (
                id INTEGER PRIMARY KEY,
                show TEXT NOT NULL,
                host TEXT NOT NULL,
                start_hour INTEGER NOT NULL,
                minutes INTEGER NOT NULL
            )
            """
        )

    def add_slot(
        self, show_name: str, host_name: str, start_hour: int, minutes: int
    ) -> None:
        """Add a valid programme slot that does not overlap another slot."""
        if not isinstance(show_name, str) or not show_name.strip():
            raise ValueError("Show name must not be empty.")
        if not isinstance(host_name, str) or not host_name.strip():
            raise ValueError("Host name must not be empty.")
        if (
            isinstance(start_hour, bool)
            or not isinstance(start_hour, int)
            or not 0 <= start_hour <= 23
        ):
            raise ValueError("Start hour must be an integer between 0 and 23.")
        if (
            isinstance(minutes, bool)
            or not isinstance(minutes, int)
            or minutes <= 0
        ):
            raise ValueError(
                "Duration must be a positive integer number of minutes."
            )

        start_minute = start_hour * 60
        end_minute = start_minute + minutes
        if end_minute > 24 * 60:
            raise ValueError("A programme slot must end by midnight.")

        existing_slots = self._connection.execute(
            "SELECT start_hour, minutes FROM slots"
        )
        for existing_hour, existing_minutes in existing_slots:
            existing_start = existing_hour * 60
            existing_end = existing_start + existing_minutes
            if start_minute < existing_end and existing_start < end_minute:
                raise ValueError("Programme slots must not overlap.")

        self._connection.execute(
            """
            INSERT INTO slots (show, host, start_hour, minutes)
            VALUES (?, ?, ?, ?)
            """,
            (show_name.strip(), host_name.strip(), start_hour, minutes),
        )

    def morning_shows(self) -> list[str]:
        """Return programme names that start before noon."""
        rows = self._connection.execute(
            """
            SELECT show
            FROM slots
            WHERE start_hour < 12
            ORDER BY start_hour, id
            """
        )
        return [row[0] for row in rows]

    def remove_slot(self, slot_id: int) -> None:
        """Remove a programme slot by its positive database ID."""
        if (
            isinstance(slot_id, bool)
            or not isinstance(slot_id, int)
            or slot_id <= 0
        ):
            raise ValueError("Slot ID must be a positive integer.")
        self._connection.execute("DELETE FROM slots WHERE id = ?", (slot_id,))

    def close(self) -> None:
        """Close the connection to the schedule database."""
        self._connection.close()


def slot_label(show_name: str, host_name: str) -> str:
    """Format a programme name and its host as a readable label."""
    return f"{show_name} hosted by {host_name}"


def overlap_free(end_hour: int, next_start_hour: int) -> bool:
    """Return whether a programme can end before the next one starts."""
    if (
        isinstance(end_hour, bool)
        or not isinstance(end_hour, int)
        or not 0 <= end_hour <= 24
    ):
        raise ValueError("End hour must be an integer between 0 and 24.")
    if (
        isinstance(next_start_hour, bool)
        or not isinstance(next_start_hour, int)
        or not 0 <= next_start_hour <= 23
    ):
        raise ValueError(
            "Next start hour must be an integer between 0 and 23."
        )
    return end_hour <= next_start_hour


def main() -> None:
    """Run the radio schedule demonstration."""
    schedule = RadioSchedule()
    try:
        schedule.add_slot("Sunrise Beats", "Vik", 7, 60)
        schedule.add_slot("Midday Talk", "Anu", 13, 45)
        print(slot_label("Sunrise Beats", "Vik"))
        print(overlap_free(8, 13), schedule.morning_shows())
        schedule.remove_slot(2)
    finally:
        schedule.close()


if __name__ == "__main__":
    main()
