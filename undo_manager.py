class UndoManager:
    def __init__(self, max_history=50):
        self._undo_stack = []
        self._redo_stack = []
        self._max_history = max_history

    def record_action(self, action_name, undo_func, redo_func, undo_args=(), redo_args=(), undo_kwargs=None, redo_kwargs=None):
        if undo_kwargs is None:
            undo_kwargs = {}
        if redo_kwargs is None:
            redo_kwargs = {}
        self._undo_stack.append({
            'name': action_name,
            'undo_func': undo_func,
            'redo_func': redo_func,
            'undo_args': undo_args,
            'redo_args': redo_args,
            'undo_kwargs': undo_kwargs,
            'redo_kwargs': redo_kwargs
        })
        if len(self._undo_stack) > self._max_history:
            self._undo_stack.pop(0)
        self._redo_stack.clear()

    def undo(self):
        if not self._undo_stack:
            return None
        action = self._undo_stack.pop()
        try:
            action['undo_func'](*action['undo_args'], **action['undo_kwargs'])
        except Exception as e:
            self._undo_stack.append(action)
            raise e
        self._redo_stack.append(action)
        return action['name']

    def redo(self):
        if not self._redo_stack:
            return None
        action = self._redo_stack.pop()
        try:
            action['redo_func'](*action['redo_args'], **action['redo_kwargs'])
        except Exception as e:
            self._redo_stack.append(action)
            raise e
        self._undo_stack.append(action)
        return action['name']

    def can_undo(self):
        return len(self._undo_stack) > 0

    def can_redo(self):
        return len(self._redo_stack) > 0

    def clear(self):
        self._undo_stack.clear()
        self._redo_stack.clear()

    def get_undo_name(self):
        if self._undo_stack:
            return self._undo_stack[-1]['name']
        return None

    def get_redo_name(self):
        if self._redo_stack:
            return self._redo_stack[-1]['name']
        return None