import queue


class PriorityQueue(queue.PriorityQueue):
    def __init__(self):
        super().__init__()

    def is_element(self, element, key=id):
        for entry in self.queue:
            if key(entry) == element:
                return True
        return False
