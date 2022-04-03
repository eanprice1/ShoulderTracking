import cv2
from Point import Point


def resize_frame(frame, scale_percent: int):
    (h, w, _) = frame.shape
    dimensions = aspect_ratio_resize(w, h, scale_percent)
    return cv2.resize(frame, dimensions, fx=0, fy=0, interpolation=cv2.INTER_AREA)


def aspect_ratio_resize(width, height, scale_percent: int):
    width = int(width * scale_percent / 100)
    height = int(height * scale_percent / 100)
    return width, height


def detect_head_edges(frame):
    (num_rows, num_cols) = frame.shape
    left_line = list()
    right_line = list()
    first_nonempty_row = 0

    for row in range(first_nonempty_row, int(num_rows/2)):
        found_first = False
        first = 0
        found_last = False
        last = 0

        for col in range(0, int(num_cols * .4)):
            if frame[row, col] == 255:
                if found_first is False:
                    first = col
                    found_first = True
                    break

        for col in range(num_cols - 1, int(num_cols * .6), -1):
            if frame[row, col] == 255:
                if found_last is False:
                    last = col
                    found_last = True
                    break

        if found_first:
            left_line.append(first)
        if found_last:
            right_line.append(last)
        if found_first and found_last:
            first_nonempty_row = row

    left_edge = int(sum(left_line) / len(left_line))
    right_edge = int(sum(right_line) / len(right_line))

    return left_edge, right_edge, first_nonempty_row


def detect_shoulders(frame, left_edge, right_edge, first_nonempty_row):
    (num_rows, num_cols) = frame.shape
    left_p1 = Point()
    found_left_p1 = False
    right_p1 = Point()
    found_right_p1 = False

    row = first_nonempty_row
    for row in range(num_rows):
        if frame[row, left_edge] == 255 and found_left_p1 is False:
            left_p1 = Point(row, left_edge)
            found_left_p1 = True
        if frame[row, right_edge] == 255 and found_right_p1 is False:
            right_p1 = Point(row, right_edge)
            found_right_p1 = True
        if found_left_p1 and found_right_p1:
            break

    left_p2 = Point(left_p1.row, left_p1.col)
    right_p2 = Point(right_p1.row, right_p1.col)
    for row in range(first_nonempty_row, num_rows):
        for col in range(left_edge - 1, -1, -1):
            if frame[row, col] == 255:
                if col < left_p2.col:
                    left_p2 = Point(row, col)
                else:
                    break
        for col in range(right_edge + 1, num_cols):
            if frame[row, col] == 255:
                if col > right_p2.col:
                    right_p2 = Point(row, col)
                else:
                    break

    return left_p1, left_p2, right_p1, right_p2
    # frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    # cv2.circle(frame, (left_p1.col, left_p1.row), 2, (0, 180, 0), thickness=2)
    # cv2.circle(frame, (left_p2.col, left_p2.row), 2, (0, 180, 0), thickness=2)
    # cv2.rectangle(frame, (left_p1.col, left_p1.row), (left_p2.col, left_p2.row), (0, 180, 0), thickness=2)
    # cv2.circle(frame, (right_p1.col, right_p1.row), 2, (0, 180, 0), thickness=2)
    # cv2.circle(frame, (right_p2.col, right_p2.row), 2, (0, 180, 0), thickness=2)
    # cv2.rectangle(frame, (right_p1.col, right_p1.row), (right_p2.col, right_p2.row), (0, 180, 0), thickness=2)



