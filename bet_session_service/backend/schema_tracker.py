from collections import defaultdict

class SchemaTracker:
    def __init__(self):
        self.field_map = defaultdict(set)

    def update(self, bet):
        for k, v in bet.items():
            self.field_map[k].add(type(v).__name__)

    def get_schema(self):
        return {k: list(v) for k, v in self.field_map.items()}

schema_tracker = SchemaTracker()
