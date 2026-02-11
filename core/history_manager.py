import copy


class HistoryManager:
    def __init__(self, max_items=40):
        self.undo_stack = []
        self.redo_stack = []
        self.max_items = max_items

    def save(self, img):
        if img is None:
            return
        self.undo_stack.append(copy.deepcopy(img))
        if len(self.undo_stack) > self.max_items:
            self.undo_stack.pop(0)
        self.redo_stack.clear()

    def undo(self):
        if len(self.undo_stack) < 2:
            return None
        self.redo_stack.append(self.undo_stack.pop())
        return copy.deepcopy(self.undo_stack[-1])

    def redo(self):
        if not self.redo_stack:
            return None
        state = self.redo_stack.pop()
        self.undo_stack.append(copy.deepcopy(state))
        return state

    def can_undo(self) -> bool:
        return len(self.undo_stack) > 1

    def can_redo(self) -> bool:
        return len(self.redo_stack) > 0