class FilterManager:
    def __init__(self, image_manager, history_manager):
        self.image_manager = image_manager
        self.history_manager = history_manager

    def apply_filter(self, filter_obj, params=None):
        if params is None:
            params = filter_obj.get_default_params()

        img = self.image_manager.get_current()
        if img is None:
            return False

        try:
            self.history_manager.save_state(img)
            result = filter_obj.apply(img, params)
            if result is not None:
                self.image_manager.update_current(result)
                return True
            return False
        except Exception as e:
            print(f"Erreur lors de l'application du filtre {filter_obj.name}: {e}")
            return False