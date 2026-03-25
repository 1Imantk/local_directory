from datetime import datetime
from collections import deque


class Business:
    """Represents a local business or startup."""

    def __init__(self, name, category, location, description, contact, founded_year=None):
        self.name = name
        self.category = category
        self.location = location
        self.description = description
        self.contact = contact
        self.founded_year = founded_year
        self.registered_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_summary(self):
        """Return a short one-line summary of the business."""
        return f"{self.name} ({self.category}) — {self.location}"

    def to_dict(self):
        """Convert the Business object to a dictionary for template rendering."""
        return {
            "name": self.name,
            "category": self.category,
            "location": self.location,
            "description": self.description,
            "contact": self.contact,
            "founded_year": self.founded_year,
            "registered_at": self.registered_at,
        }


class BusinessDirectory:
    """
    Manages all businesses using:
      - A list as the main store (all businesses)
      - A deque (Queue, FIFO) to track recently added businesses
      - A list used as a Stack (LIFO) for undo-delete functionality
    """

    def __init__(self, recent_limit=5):
        self._businesses = []          # main store
        self._recent_queue = deque()   # FIFO — recently added (Queue)
        self._deleted_stack = []       # LIFO — undo delete (Stack)
        self._recent_limit = recent_limit

    # ── Core operations ──────────────────────────────────────────────

    def add_business(self, business: Business):
        """Add a new Business and push it onto the recent queue."""
        self._businesses.append(business)

        # Queue: enqueue new business; dequeue oldest if limit exceeded
        self._recent_queue.append(business)
        if len(self._recent_queue) > self._recent_limit:
            self._recent_queue.popleft()   # FIFO — remove oldest

    def delete_business(self, index: int):
        """Remove a business by index and push it onto the undo stack."""
        if 0 <= index < len(self._businesses):
            removed = self._businesses.pop(index)
            self._deleted_stack.append(removed)   # Stack: LIFO push
            # Rebuild recent queue from remaining businesses
            self._rebuild_recent()
            return removed
        return None

    def undo_delete(self):
        """Pop the last deleted business off the stack and restore it."""
        if self._deleted_stack:
            business = self._deleted_stack.pop()   # Stack: LIFO pop
            self._businesses.append(business)
            self._recent_queue.append(business)
            if len(self._recent_queue) > self._recent_limit:
                self._recent_queue.popleft()
            return business
        return None

    # ── Queries ──────────────────────────────────────────────────────

    def get_all(self):
        return list(self._businesses)

    def get_recent(self):
        """Return recently added businesses (Queue contents, newest last)."""
        return list(self._recent_queue)

    def get_by_category(self, category: str):
        return [b for b in self._businesses if b.category.lower() == category.lower()]

    def total_count(self):
        return len(self._businesses)

    def can_undo(self):
        return len(self._deleted_stack) > 0

    # ── Helpers ──────────────────────────────────────────────────────

    def _rebuild_recent(self):
        """Rebuild the recent queue from the last N businesses."""
        self._recent_queue = deque(
            self._businesses[-self._recent_limit:],
            maxlen=self._recent_limit
        )

    def get_categories(self):
        return sorted(set(b.category for b in self._businesses))


# ── Pre-load sample data ──────────────────────────────────────────────────────

directory = BusinessDirectory()

sample_data = [
    Business("Kano Tech Hub", "Technology", "Kano, Nigeria",
             "A co-working space and incubator for tech startups in northern Nigeria.",
             "kanotechhub@gmail.com", 2020),
    Business("FarmConnect NG", "Agriculture", "Zaria, Nigeria",
             "Connecting smallholder farmers directly to urban markets via mobile.",
             "+234-801-000-0001", 2021),
    Business("MediQuick Pharmacy", "Healthcare", "Kaduna, Nigeria",
             "Fast-delivery pharmacy serving residential estates across Kaduna.",
             "mediquick@ng.com", 2019),
    Business("EduBridge Tutorials", "Education", "Kano, Nigeria",
             "Affordable JAMB and WAEC preparation centre for secondary school students.",
             "+234-802-000-0002", 2018),
    Business("GreenBuild Materials", "Construction", "Abuja, Nigeria",
             "Supplier of eco-friendly building materials for modern construction projects.",
             "greenbuild@abuja.ng", 2022),
]

for b in sample_data:
    directory.add_business(b)
