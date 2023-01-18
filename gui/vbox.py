from gui.component import *

class VBox(Component):
    def __init__(self, game):
        super().__init__(game)

    def layout(self):
        # Calculate size of flexible elements
        flexible_size = self.calculate_flexible_size()

        # Reposition and resize all elements
        pos = self.position[1]
        for c in self.children:
            if not c.visible:
                continue
            c.position = (self.position[0], pos)
            if c.flexible[0]:
                c.size = (self.size[0], c.size[1])
            if c.flexible[1]:
                c.size = (self.size[0], flexible_size)
            pos += c.size[1]

            # Make sure element children are also updated
            c.layout()

    def calculate_flexible_size(self):
        # Flexible element size is equal to all flexible elements after
        # non-flexible elements take up their space
        size = self.size[1]
        count = 0
        for c in self.children:
            if not c.visible:
                continue
            if c.flexible[1]:
                count += 1
            else:
                size -= c.size[1]

        if size <= 0 or count == 0:
            return 0
        return size / count
