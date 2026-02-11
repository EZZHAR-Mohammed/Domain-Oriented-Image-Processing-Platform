import copy

class HistoryManager:
    def __init__(self, max_size=50):
        self.undo_stack = []
        self.redo_stack = []
        self.max_size = max_size

    def save_state(self, image):
        if image is None:
            return
        # On limite la taille pour éviter de consommer trop de mémoire
        if len(self.undo_stack) >= self.max_size:
            self.undo_stack.pop(0)
        self.undo_stack.append(copy.deepcopy(image))
        self.redo_stack.clear()

    def can_undo(self):
        return len(self.undo_stack) > 0

    def undo(self):
        if not self.can_undo():
            return None
        state = self.undo_stack.pop()
        if self.undo_stack:
            current = copy.deepcopy(self.undo_stack[-1])
        else:
            current = None
        self.redo_stack.append(state)
        return current

    def can_redo(self):
        return len(self.redo_stack) > 0

    def redo(self):
        if not self.can_redo():
            return None
        state = self.redo_stack.pop()
        self.undo_stack.append(copy.deepcopy(state))
        return state