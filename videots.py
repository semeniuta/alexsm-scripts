import argparse
from datetime import datetime

TS_FORMAT = '%H:%M:%S'

def ts_string(ts):
    return datetime.strftime(ts, TS_FORMAT)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('filepath')
    args = parser.parse_args()

    s = datetime.strptime('00:00:00', TS_FORMAT)

    with open(args.filepath) as f:
        for line in f:
            a, b = line.strip().split(' ')

            segment_start = datetime.strptime(a, TS_FORMAT)
            segment_end = datetime.strptime(b, TS_FORMAT)
            segment_duration = segment_end - segment_start
            
            s += segment_duration

            datetime.strftime(s, TS_FORMAT)

            print(ts_string(segment_start), ts_string(segment_end), ts_string(s))