import argparse
import os

from cv2 import VideoCapture, CAP_PROP_POS_MSEC, imwrite


class Vid2Frame:
    def __init__(self, video_name, interval):
        self.VIDEO_NAME = video_name
        self.INTERVAL = interval
        self.PATH_NAME = f'{self.VIDEO_NAME}-frames'

    def prepare(self):
        try:
            if not os.path.exists(self.PATH_NAME):
                os.makedirs(self.PATH_NAME)
        except OSError:
            print(f'Error: Creating directory of {self.PATH_NAME}')

    def get_frames(self):
        print(f'Extracting frames from {self.VIDEO_NAME}')
        cam = VideoCapture(self.VIDEO_NAME)
        currentframe = 0
        while True:
            cam.set(CAP_PROP_POS_MSEC, (currentframe * self.INTERVAL))
            ret, frame = cam.read()
            if ret:
                name = f'./{self.PATH_NAME}/{self.VIDEO_NAME}-{currentframe * self.INTERVAL}.png'
                imwrite(name, frame)
                currentframe += 1
            else:
                break
        print('End of extracting frames')
        cam.release()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='vid2frames')
    parser.set_defaults(command='zero_args')

    parser.add_argument('-v', '--video',
                        help='Video file to extract',
                        type=str,
                        required=True)

    parser.add_argument('-i', '--interval',
                        help='Interval in milliseconds',
                        type=int,
                        required=True)

    args = parser.parse_args()

    vid2frames = Vid2Frame(args.video, args.interval)
    vid2frames.prepare()
    vid2frames.get_frames()
