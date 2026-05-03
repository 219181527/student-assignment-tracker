"""
tests/test_singleton.py
Tests for the Singleton pattern — NotificationService
Includes thread-safety verification.
"""

import pytest
import threading
from src.notification import Notification
from src.student import Student
from creational_patterns.singleton import NotificationService


@pytest.fixture
def service():
    svc = NotificationService()
    svc.reset_for_testing()
    return svc


@pytest.fixture
def sample_student():
    s = Student("s_svc", "Test Student", "test@uni.ac.za", "pass", "STU_SVC", 1)
    s.register()
    return s


@pytest.fixture
def deadline_notification():
    return Notification("n_test", "Test deadline alert.", "DEADLINE", source=None)


@pytest.fixture
def submission_notification():
    return Notification("n_sub", "Submission confirmed.", "SUBMISSION", source=None)


@pytest.fixture
def grade_notification():
    return Notification("n_grade", "You have been graded.", "GRADE", source=None)


class TestSingletonIdentity:

    def test_two_instances_are_same_object(self, service):
        svc2 = NotificationService()
        assert service is svc2

    def test_ids_are_identical(self, service):
        svc2 = NotificationService()
        assert id(service) == id(svc2)

    def test_state_shared_across_instances(self, service, sample_student, deadline_notification):
        svc2 = NotificationService()
        service.enqueue(deadline_notification, sample_student)
        # svc2 sees the queue updated via service
        assert svc2.queue_size() == 1

    def test_reset_affects_both_references(self, service):
        svc2 = NotificationService()
        service.reset_for_testing()
        assert svc2.queue_size() == 0


class TestNotificationQueueing:

    def test_enqueue_increases_queue_size(self, service, sample_student, deadline_notification):
        service.enqueue(deadline_notification, sample_student)
        assert service.queue_size() == 1

    def test_multiple_enqueues_accumulate(self, service, sample_student,
                                           deadline_notification, submission_notification):
        service.enqueue(deadline_notification, sample_student)
        service.enqueue(submission_notification, sample_student)
        assert service.queue_size() == 2

    def test_enqueue_does_not_dispatch_immediately(self, service, sample_student, deadline_notification):
        before = len(sample_student.notifications)
        service.enqueue(deadline_notification, sample_student)
        assert len(sample_student.notifications) == before  # Not yet dispatched


class TestDispatch:

    def test_dispatch_all_clears_queue(self, service, sample_student, deadline_notification):
        service.enqueue(deadline_notification, sample_student)
        service.dispatch_all()
        assert service.queue_size() == 0

    def test_dispatch_all_returns_count(self, service, sample_student,
                                         deadline_notification, submission_notification):
        service.enqueue(deadline_notification, sample_student)
        service.enqueue(submission_notification, sample_student)
        count = service.dispatch_all()
        assert count == 2

    def test_dispatch_all_adds_to_student(self, service, sample_student, deadline_notification):
        before = len(sample_student.notifications)
        service.enqueue(deadline_notification, sample_student)
        service.dispatch_all()
        assert len(sample_student.notifications) == before + 1

    def test_dispatch_to_specific_student(self, service, sample_student, student_b,
                                           deadline_notification, submission_notification):
        service.enqueue(deadline_notification, sample_student)
        service.enqueue(submission_notification, student_b)
        dispatched = service.dispatch_to(sample_student)
        assert dispatched == 1
        assert service.queue_size() == 1  # student_b's notification still queued

    def test_dispatch_all_on_empty_queue_returns_zero(self, service):
        assert service.dispatch_all() == 0

    def test_dispatched_items_appear_in_log(self, service, sample_student, deadline_notification):
        service.enqueue(deadline_notification, sample_student)
        service.dispatch_all()
        log = service.get_log()
        assert len(log) == 1
        assert log[0]["notification_id"] == "n_test"

    def test_log_contains_correct_student_id(self, service, sample_student, deadline_notification):
        service.enqueue(deadline_notification, sample_student)
        service.dispatch_all()
        assert service.get_log()[0]["student_id"] == sample_student.user_id


class TestStatistics:

    def test_stats_increment_on_dispatch(self, service, sample_student, deadline_notification):
        service.enqueue(deadline_notification, sample_student)
        service.dispatch_all()
        assert service.get_stats()["DEADLINE"] == 1

    def test_stats_track_each_trigger_type(self, service, sample_student,
                                            deadline_notification, submission_notification, grade_notification):
        service.enqueue(deadline_notification, sample_student)
        service.enqueue(submission_notification, sample_student)
        service.enqueue(grade_notification, sample_student)
        service.dispatch_all()
        stats = service.get_stats()
        assert stats["DEADLINE"] == 1
        assert stats["SUBMISSION"] == 1
        assert stats["GRADE"] == 1

    def test_stats_reset_clears_counts(self, service, sample_student, deadline_notification):
        service.enqueue(deadline_notification, sample_student)
        service.dispatch_all()
        service.reset_for_testing()
        assert service.get_stats()["DEADLINE"] == 0


class TestThreadSafety:

    def test_concurrent_instantiation_returns_same_instance(self):
        """
        Spawn 20 threads each calling NotificationService().
        All must receive the same instance (identical id()).
        """
        instances = []
        lock = threading.Lock()

        def get_instance():
            svc = NotificationService()
            with lock:
                instances.append(id(svc))

        threads = [threading.Thread(target=get_instance) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(set(instances)) == 1, (
            f"Expected 1 unique instance id, got {len(set(instances))}: {set(instances)}"
        )

    def test_concurrent_enqueue_is_safe(self):
        """
        10 threads each enqueue 5 notifications.
        Total queued must equal 50 — no race-condition drops or duplicates.
        """
        svc = NotificationService()
        svc.reset_for_testing()
        student = Student("s_thread", "T", "t@t.com", "p", "STU_T", 1)
        student.register()

        def enqueue_five():
            for i in range(5):
                n = Notification(
                    f"n_thread_{threading.get_ident()}_{i}",
                    "Thread test.", "DEADLINE", source=None,
                )
                svc.enqueue(n, student)

        threads = [threading.Thread(target=enqueue_five) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert svc.queue_size() == 50