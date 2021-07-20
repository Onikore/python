import argparse
import csv
import os

from cv2 import VideoCapture, CAP_PROP_POS_MSEC, imwrite


class ExtractFrames:
    def __init__(self, video_name, csv_name):
        self.VIDEO_NAME = video_name
        self.CSV = csv_name
        self.PATH_NAME = f'{self.VIDEO_NAME}-frames'

    @staticmethod
    def prepare_path(path_name):
        try:
            if not os.path.exists(path_name):
                os.makedirs(path_name)
        except OSError:
            print(f'Error: Creating directory of {path_name}')

    def get_frames(self):
        print(f'Extracting frames from {self.VIDEO_NAME}')
        with open(self.CSV) as f:
            reader = csv.DictReader(f, delimiter=',')
            for line in reader:
                self.prepare_path(line["label"])
                cam = VideoCapture(self.VIDEO_NAME)
                cam.set(CAP_PROP_POS_MSEC, int(line["timestamp"]))
                ret, frame = cam.read()
                if ret:
                    name = f'./{line["label"]}/{self.VIDEO_NAME}-{int(line["timestamp"])}.png'
                    imwrite(name, frame)
                cam.release()
        print('End of extracting frames')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='extractFrames')
    parser.set_defaults(command='zero_args')

    parser.add_argument('-v', '--video',
                        help='Video file to extract',
                        type=str,
                        required=True)

    parser.add_argument('-c', '--csv',
                        help='CSV file containing timestamp and label',
                        type=str,
                        required=True)

    args = parser.parse_args()

    vid2frames = ExtractFrames(args.video, args.csv)
    vid2frames.get_frames()
