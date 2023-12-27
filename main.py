import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Box():
    def __init__(self, anchor_x, anchor_y, size):
        self.top_right = Point(anchor_x + size, anchor_y + size)
        self.top_left = Point(anchor_x, anchor_y + size)
        self.bottom_right = Point(anchor_x + size, anchor_y)
        self.bottom_left = Point(anchor_x, anchor_y)


def find_location(anchors, x_max, y_max, size, granularity):
    def anchor_available(test_x, test_y):
        test_box = Box(test_x, test_y, size)

        for anchor in anchors:
            existing_box = Box(anchor[0], anchor[1], size)
            if not (
                test_box.top_left.x >= existing_box.bottom_right.x or
                test_box.bottom_right.x <= existing_box.top_left.x or
                test_box.bottom_right.y >= existing_box.top_left.y or
                test_box.top_left.y <= existing_box.bottom_right.y
            ):
                return False
        
        return True

    max_y_anchor = y_max - size
    max_x_anchor = x_max - size

    x = random.randrange(0, max_x_anchor, granularity)
    y = random.randrange(0, max_y_anchor, granularity)

    if not anchor_available(x, y):
        x, y = find_location(anchors, x_max, y_max, size, granularity)
    
    return x, y

def generate_layout(ax, box_count, wall_width, wall_height, box_size, spacing_granularity):
    ax.clear()
    
    ax.set_ylim([0,wall_height])
    ax.set_xlim([0,wall_width])

    boxes = []
    for i in range(box_count):
        x, y = find_location(boxes, wall_width, wall_height, box_size, spacing_granularity)
        boxes.append((x, y))
        box = patches.Rectangle((x, y), box_size, box_size, linewidth=1, edgecolor='black')
        ax.add_patch(box)
    return boxes

if __name__ == "__main__":
    wall_width = int(input("Width (inches): "))
    wall_height = int(input("Height (inches): "))
    box_size = int(input("Box Size (inches): "))
    box_count = int(input("Box Count: "))
    spacing_granularity = int(input("Spacing Granularity (inches): "))

    fig_ratio = wall_height / wall_width

    fig_width = 10 if fig_ratio >= 1 else fig_ratio * 10
    fig_height = 10 if fig_ratio <= 1 else 1/fig_ratio * 10

    fig, ax = plt.subplots(figsize=(fig_height, fig_width))

    while True:
        try:
            boxes = generate_layout(ax, box_count, wall_width, wall_height, box_size, spacing_granularity)
        except RecursionError:
            print("Unable to solve. Retrying...")
            continue

        plt.show(block=False)

        input("Press Enter to refresh layout...")