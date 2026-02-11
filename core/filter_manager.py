# core/filter_manager.py
class FilterManager:
    def __init__(self, image_manager, history_manager):
        self.image_manager = image_manager
        self.history_manager = history_manager

    def apply_filter(self, filter_instance, params=None):
        """Applique un filtre et met à jour l'image"""
        if params is None:
            params = filter_instance.get_default_params()

        image = self.image_manager.get_current()
        if image is None:
            print("Aucune image chargée pour appliquer le filtre")
            return False

        try:
            # Sauvegarde l'état actuel AVANT modification
            self.history_manager.save_state(image)

            # Application du filtre
            processed = filter_instance.apply(image, params)

            if processed is None:
                print("Le filtre a retourné None")
                return False

            # Mise à jour (ICI est la ligne qui plantait)
            self.image_manager.set_current(processed)          # ← ou .update_current si tu ajoutes la méthode

            return True

        except Exception as e:
            print(f"Erreur lors de l'application du filtre {filter_instance.name}: {e}")
            return False