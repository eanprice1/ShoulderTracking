import cv2
import skvideo
skvideo.setFFmpegPath('C:/FFmpeg/bin/')
import skvideo.io
import numpy as np
import Utility as Util
from Point import Point


def main():
    original_video_filename = "Resources/ShoulderVideo.mp4"
    output_filename = "Resources/Output.mp4"
    video = cv2.VideoCapture(original_video_filename)
    height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    scale_percent = 50
    new_video = skvideo.io.FFmpegWriter(output_filename, inputdict={'-pix_fmt': 'bgr24'},
                                        outputdict={'-pix_fmt': 'yuv420p'})
    bound_offset = 20
    i = 0
    while video.isOpened():
        is_valid_frame, frame = video.read()
        if is_valid_frame:
            frame = Util.resize_frame(frame, scale_percent)
            canny = cv2.Canny(frame, 100, 200)
            left_edge, right_edge, first_nonempty_row = Util.detect_head_edges(canny)
            left_edge -= bound_offset
            right_edge += bound_offset
            left_p1, left_p2, right_p1, right_p2 = Util.detect_shoulders(canny, left_edge, right_edge
                                                                         , first_nonempty_row)

            cv2.rectangle(frame, (left_p1.col, left_p1.row), (left_p2.col, left_p2.row), (0, 180, 0), thickness=2)
            cv2.rectangle(frame, (right_p1.col, right_p1.row), (right_p2.col, right_p2.row), (0, 180, 0), thickness=2)
            print(f'New Frame Added: {i}')
            new_video.writeFrame(frame)
        else:
            break
        i += 1

    new_video.close()
    video.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
