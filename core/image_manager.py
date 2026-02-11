import cv2


class ImageManager:
    def __init__(self):
        self.original = None
        self.current  = None

    def load(self, path: str) -> bool:
        img = cv2.imread(path)
        if img is None:
            return False
        self.original = img.copy()
        self.current  = img.copy()
        return True

    def get_current(self):
        return self.current

    def get_original(self):
        return self.original

    def update(self, new_img):
        self.current = new_img

    def reset(self):
        if self.original is not None:
            self.current = self.original.copy()

    def save(self, path: str) -> bool:
        if self.current is None:
            return False
        return cv2.imwrite(path, self.current)