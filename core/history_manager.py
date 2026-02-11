# core/history_manager.py
import copy
from typing import Optional


class HistoryManager:
    def __init__(self, max_size: int = 50):
        self.undo_stack: list = []
        self.redo_stack: list = []
        self.max_size = max_size

    def save_state(self, image) -> None:
        """
        Sauvegarde l'état actuel dans la pile undo
        (efface la pile redo car nouvelle action)
        """
        if image is None:
            return

        # Limite la taille pour éviter de consommer trop de mémoire
        if len(self.undo_stack) >= self.max_size:
            self.undo_stack.pop(0)

        self.undo_stack.append(copy.deepcopy(image))
        self.redo_stack.clear()

    def can_undo(self) -> bool:
        return len(self.undo_stack) > 1  # >1 car on garde l'état initial

    def undo(self) -> Optional[np.ndarray]:
        if not self.can_undo():
            return None

        # On met l'état actuel dans redo
        self.redo_stack.append(self.undo_stack.pop())
        
        # Retourne l'état précédent
        if self.undo_stack:
            return copy.deepcopy(self.undo_stack[-1])
        return None

    def can_redo(self) -> bool:
        return len(self.redo_stack) > 0

    def redo(self) -> Optional[np.ndarray]:
        if not self.can_redo():
            return None

        state = self.redo_stack.pop()
        self.undo_stack.append(copy.deepcopy(state))
        return state