from datetime import datetime
from collections import deque


class Business:
    """Represents a local business or startup."""

    def __init__(self, name, category, location, description, contact, founded_year=None, website=None, id=None):
        self.id = id
        self.name = name
        self.category = category
        self.location = location
        self.description = description
        self.contact = contact
        self.founded_year = founded_year
        self.website = website
        self.ratings = []
        self.is_open = True
        self.registered_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def add_rating(self, stars):
        if 1 <= stars <= 5:
            self.ratings.append(stars)

    def get_average_rating(self):
        if not self.ratings:
            return 0
        return sum(self.ratings) / len(self.ratings)

    def get_summary(self):
        """Return a short one-line summary of the business."""
        return f"{self.name} ({self.category}) — {self.location}"

    def to_dict(self):
        """Convert the Business object to a dictionary for template rendering."""
        return {
            "id": getattr(self, 'id', None),
            "name": self.name,
            "category": self.category,
            "location": self.location,
            "description": self.description,
            "contact": self.contact,
            "founded_year": self.founded_year,
            "website": self.website,
            "ratings": list(self.ratings),
            "average_rating": self.get_average_rating(),
            "rating_count": len(self.ratings),
            "is_open": self.is_open,
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
        self._next_id = 1

    # ── Core operations ──────────────────────────────────────────────

    def add_business(self, business: Business):
        """Add a new Business and push it onto the recent queue."""
        business.id = self._next_id
        self._next_id += 1
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

    def update_business(self, business_id, name, category, location, description, contact, founded_year, website):
        for b in self._businesses:
            if b.id == business_id:
                b.name = name
                b.category = category
                b.location = location
                b.description = description
                b.contact = contact
                b.founded_year = founded_year
                b.website = website
                return b
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

    def name_exists(self, name):
        return any(b.name.lower() == name.lower() for b in self._businesses)

    def get_recent(self):
        """Return recently added businesses (Queue contents, newest last)."""
        return list(self._recent_queue)

    def get_by_category(self, category: str):
        return [b for b in self._businesses if b.category.lower() == category.lower()]

    def get_by_id(self, business_id):
        for b in self._businesses:
            if b.id == business_id:
                return b
        return None

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

    def get_category_counts(self):
        counts = {}
        for b in self._businesses:
            counts[b.category] = counts.get(b.category, 0) + 1
        return dict(sorted(counts.items()))
