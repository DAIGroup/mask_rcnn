"""
    Non-maxima supression algorithm for densepose 2 results.
"""
import numpy as np

def _intersection_over_union(bbox1, bbox2):
    x1, y1, w1, h1 = bbox1
    x2, y2, w2, h2 = bbox2

    # Intersection rectangle (max TL corner, min BR corner)
    ix0 = max(x1, x2)
    iy0 = max(y1, y2)
    ixf = min(x1 + w1 - 1, x2 + w2 - 1)
    iyf = min(y1 + h1 - 1, y2 + h2 - 1)

    intersection = (ixf - ix0) * (iyf - iy0)
    area1 = w1*h1
    area2 = w2*h2

    union = area1 + area2 - intersection  # subtraction of common "intersection" area.
    iou = intersection / union
    return iou


def non_maxima_supression(scores, bboxes):
    sorted_scores = sorted(scores, reverse=True)
    indices = np.zeros((len(scores)))

