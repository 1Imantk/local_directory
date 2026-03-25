"""
Unit tests for the Queue (FIFO) and Stack (LIFO) data structures
used in the BusinessDirectory class.

Run with: python models_test.py
"""

from models import Business, BusinessDirectory


def test_queue_fifo():
    print("\n" + "=" * 60)
    print("TEST: Queue (FIFO) — Recently Added Businesses")
    print("=" * 60)

    directory = BusinessDirectory(recent_limit=3)

    for i in range(1, 5):
        b = Business(f"Business {i}", "Test", "Location", f"Description {i}", "contact@test.com")
        directory.add_business(b)
        print(f"  Added: {b.name}")
        recent = directory.get_recent()
        print(f"  Recent queue: {[r.name for r in recent]}")

    print("\n  Expected behavior:")
    print("  - Queue limit is 3")
    print("  - After adding 4 businesses, only the last 3 should be in the queue")
    print("  - Business 1 should have been dequeued (removed from front)")

    recent = directory.get_recent()
    print(f"\n  Final queue: {[r.name for r in recent]}")

    assert len(recent) == 3, f"Expected 3 items in queue, got {len(recent)}"
    assert recent[0].name == "Business 2", f"Expected 'Business 2' first, got '{recent[0].name}'"
    assert recent[2].name == "Business 4", f"Expected 'Business 4' last, got '{recent[2].name}'"
    print("\n  [PASS] Queue (FIFO) test passed!")


def test_stack_lifo():
    print("\n" + "=" * 60)
    print("TEST: Stack (LIFO) — Undo Delete")
    print("=" * 60)

    directory = BusinessDirectory()

    b1 = Business("Alpha Corp", "Tech", "Kano", "First business", "alpha@test.com")
    b2 = Business("Beta LLC", "Retail", "Abuja", "Second business", "beta@test.com")
    b3 = Business("Gamma Inc", "Finance", "Lagos", "Third business", "gamma@test.com")

    directory.add_business(b1)
    directory.add_business(b2)
    directory.add_business(b3)

    print(f"  Initial businesses: {[b.name for b in directory.get_all()]}")

    print("\n  Deleting 'Beta LLC'...")
    removed = directory.delete_business(1)
    print(f"  Removed: {removed.name}")
    print(f"  Remaining: {[b.name for b in directory.get_all()]}")
    print(f"  Stack contents: {[b.name for b in directory._deleted_stack]}")

    print("\n  Deleting 'Alpha Corp'...")
    removed2 = directory.delete_business(0)
    print(f"  Removed: {removed2.name}")
    print(f"  Remaining: {[b.name for b in directory.get_all()]}")
    print(f"  Stack contents (LIFO): {[b.name for b in directory._deleted_stack]}")

    print("\n  Expected stack order (top to bottom): ['Alpha Corp', 'Beta LLC']")
    print("  LIFO means: Alpha Corp should be popped FIRST (last deleted = first restored)")

    print("\n  Undoing last delete (pop from stack)...")
    restored = directory.undo_delete()
    print(f"  Restored: {restored.name}")
    print(f"  Businesses after undo: {[b.name for b in directory.get_all()]}")

    assert restored.name == "Alpha Corp", f"Expected 'Alpha Corp' restored first, got '{restored.name}'"
    assert directory.get_all()[-1].name == "Alpha Corp", "Restored business should be at the end"
    print("\n  [PASS] Stack (LIFO) test passed!")

    print("\n  Undoing again (should restore Beta LLC)...")
    restored2 = directory.undo_delete()
    print(f"  Restored: {restored2.name}")
    print(f"  Businesses after undo: {[b.name for b in directory.get_all()]}")

    assert restored2.name == "Beta LLC", f"Expected 'Beta LLC' restored, got '{restored2.name}'"
    print("\n  [PASS] Second undo (LIFO) test passed!")


def test_queue_order_after_delete():
    print("\n" + "=" * 60)
    print("TEST: Queue Rebuild After Delete")
    print("=" * 60)

    directory = BusinessDirectory(recent_limit=3)

    for name in ["First", "Second", "Third"]:
        b = Business(name, "Test", "Loc", "Desc", "contact@test.com")
        directory.add_business(b)

    print(f"  Businesses: {[b.name for b in directory.get_all()]}")
    print(f"  Recent queue: {[b.name for b in directory.get_recent()]}")

    print("\n  Deleting 'Second' (index 1)...")
    directory.delete_business(1)
    print(f"  Recent queue after delete: {[b.name for b in directory.get_recent()]}")

    assert len(directory.get_recent()) == 2, "Queue should have 2 items after one business deleted"
    assert directory.get_recent()[0].name == "First", "First should still be in queue"
    assert directory.get_recent()[1].name == "Third", "Third should still be in queue"
    print("\n  [PASS] Queue rebuild after delete test passed!")


def test_empty_stack_undo():
    print("\n" + "=" * 60)
    print("TEST: Undo on Empty Stack")
    print("=" * 60)

    directory = BusinessDirectory()
    print("  Stack is empty, attempting undo...")

    result = directory.undo_delete()
    print(f"  Result: {result}")

    assert result is None, "Undo on empty stack should return None"
    print("  [PASS] Empty stack undo test passed!")


def test_can_undo():
    print("\n" + "=" * 60)
    print("TEST: can_undo() Method")
    print("=" * 60)

    directory = BusinessDirectory()
    print(f"  Initial can_undo: {directory.can_undo()}")

    b = Business("Test Business", "Test", "Loc", "Desc", "contact@test.com")
    directory.add_business(b)
    print(f"  After adding (no delete): can_undo = {directory.can_undo()}")

    directory.delete_business(0)
    print(f"  After deleting: can_undo = {directory.can_undo()}")

    assert directory.can_undo() == True, "can_undo should be True after delete"
    print("  [PASS] can_undo() test passed!")


if __name__ == "__main__":
    print("\n" + "#" * 60)
    print("#  BizDirectory NG — Queue & Stack Unit Tests")
    print("#" * 60)

    test_queue_fifo()
    test_stack_lifo()
    test_queue_order_after_delete()
    test_empty_stack_undo()
    test_can_undo()

    print("\n" + "#" * 60)
    print("#  ALL TESTS PASSED!")
    print("#" * 60 + "\n")
