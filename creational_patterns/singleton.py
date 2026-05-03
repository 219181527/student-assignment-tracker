"""
singleton.py — Singleton Pattern
Student Assignment Tracker

Pattern:  Singleton
Use Case: NotificationService — a single global dispatcher that queues and
          sends all system notifications. Multiple instances would cause
          duplicate alerts (the same student receiving the same deadline
          reminder twice from two separate service instances).

Justification: Notification dispatch must be centralised to prevent
               duplication. Thread safety is implemented via a lock so the
               pattern holds in a multi-threaded web server context.
"""

import threading
from datetime import datetime
from typing import List, Dict


# ---------------------------------------------------------------------------
# Singleton — NotificationService
# ---------------------------------------------------------------------------

class NotificationService:
    """
    Thread-safe Singleton notification dispatcher.

    Guarantees exactly one instance per process. All calls to
    NotificationService() return the same object.

    Responsibilities:
    - Queue outgoing notifications
    - Dispatch notifications to students
    - Log sent notifications for audit
    - Track delivery statistics
    """

    _instance = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls):
        """
        Double-checked locking ensures thread safety without acquiring
        the lock on every subsequent call after the instance is created.
        """
        if cls._instance is None:
            with cls._lock:
                # Second check inside the lock prevents a race condition
                # where two threads both pass the first None check.
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialise()
        return cls._instance

    def _initialise(self):
        """Called once when the singleton is first created."""
        self._queue: List[dict] = []
        self._sent_log: List[dict] = []
        self._stats: Dict[str, int] = {
            "DEADLINE": 0,
            "SUBMISSION": 0,
            "GRADE": 0,
        }
        print("[NotificationService] Initialised — single instance created.")

    # ------------------------------------------------------------------ #
    # Public methods
    # ------------------------------------------------------------------ #

    def enqueue(self, notification, student) -> None:
        """Add a notification to the outgoing queue."""
        self._queue.append({
            "notification": notification,
            "student": student,
            "queued_at": datetime.now(),
        })

    def dispatch_all(self) -> int:
        """
        Send all queued notifications.
        Returns the count of notifications dispatched.
        """
        dispatched = 0
        while self._queue:
            item = self._queue.pop(0)
            notif = item["notification"]
            student = item["student"]
            notif.send(student.user_id)
            student.add_notification(notif)
            self._sent_log.append({
                "notification_id": notif.notification_id,
                "student_id": student.user_id,
                "trigger_type": notif.trigger_type,
                "sent_at": datetime.now(),
            })
            self._stats[notif.trigger_type] = self._stats.get(notif.trigger_type, 0) + 1
            dispatched += 1
        return dispatched

    def dispatch_to(self, student) -> int:
        """Dispatch only notifications queued for a specific student."""
        target = [i for i in self._queue if i["student"] == student]
        for item in target:
            self._queue.remove(item)
            notif = item["notification"]
            notif.send(student.user_id)
            student.add_notification(notif)
            self._sent_log.append({
                "notification_id": notif.notification_id,
                "student_id": student.user_id,
                "trigger_type": notif.trigger_type,
                "sent_at": datetime.now(),
            })
            self._stats[notif.trigger_type] = self._stats.get(notif.trigger_type, 0) + 1
        return len(target)

    def get_stats(self) -> Dict[str, int]:
        """Return delivery counts per trigger type."""
        return dict(self._stats)

    def get_log(self) -> List[dict]:
        """Return the full audit log of sent notifications."""
        return list(self._sent_log)

    def queue_size(self) -> int:
        """Return the number of notifications currently queued."""
        return len(self._queue)

    def reset_for_testing(self) -> None:
        """
        Reset internal state. FOR TESTING ONLY.
        Does not destroy the singleton instance itself.
        """
        self._queue.clear()
        self._sent_log.clear()
        self._stats = {"DEADLINE": 0, "SUBMISSION": 0, "GRADE": 0}


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    from datetime import date, timedelta
    from src.student import Student
    from src.lecturer import Lecturer
    from src.course import Course
    from src.enrollment import Enrollment
    from src.notification import Notification

    # Prove singleton identity
    svc1 = NotificationService()
    svc2 = NotificationService()
    print(f"Same instance: {svc1 is svc2}")   # True
    print(f"IDs: {id(svc1)} == {id(svc2)}")   # Identical

    # Setup
    lecturer = Lecturer("l1", "Dr Nkosi", "nkosi@uni.ac.za", "pass", "CS", "EMP01")
    lecturer.register()
    student = Student("s1", "Alice", "alice@uni.ac.za", "pass", "STU001", 2)
    student.register()
    course = Course("c1", "Software Engineering", "CS301")
    Enrollment("e1", student, course)

    # Queue notifications via the singleton
    notif1 = Notification("n1", "Assignment published.", "DEADLINE", source=None)
    notif2 = Notification("n2", "Submission received.", "SUBMISSION", source=None)

    svc1.enqueue(notif1, student)
    svc1.enqueue(notif2, student)
    print(f"\nQueued: {svc1.queue_size()} notifications")

    # Dispatch from the same instance
    count = svc2.dispatch_all()
    print(f"Dispatched: {count}")
    print(f"Stats: {svc2.get_stats()}")

    # Thread safety demonstration
    def create_service():
        svc = NotificationService()
        print(f"  Thread got instance id: {id(svc)}")

    threads = [threading.Thread(target=create_service) for _ in range(5)]
    print("\nThread-safety test (all IDs must match):")
    for t in threads:
        t.start()
    for t in threads:
        t.join()