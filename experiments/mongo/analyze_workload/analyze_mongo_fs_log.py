import argparse 
import pathlib 
import time 
import pprint
from collections import defaultdict

def main(mongo_log_path):
    stat_dict = defaultdict(float)
    read_file_dict = defaultdict(float)
    write_file_dict = defaultdict(float)
    file_io_stat = {}
    fs_op_count = defaultdict(int)
    with mongo_log_path.open("r") as f:
        line = f.readline()
        while line:

            split_line = line.split(",")
            fs_operation = split_line[0]
            path = pathlib.Path(fs_operation[1])

            fs_op_count[fs_operation] += 1

            if fs_operation == "write" or fs_operation == "read":
                length = int(split_line[2])/(1024*1024)
                offset = int(split_line[3])

                stat_dict["{}_MB".format(fs_operation)] += length 
                

                if fs_operation == "read":
                    read_file_dict[pathlib.Path(split_line[1])] += length
                elif fs_operation == "write":
                    write_file_dict[pathlib.Path(split_line[1])] += length

            line = f.readline()


        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(stat_dict)
        pp.pprint(read_file_dict)
        pp.pprint(write_file_dict)
        pp.pprint(fs_op_count)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get a report of mongo traces")
    parser.add_argument("mongo_log_path", type=pathlib.Path, help="The path of mongo log")
    args = parser.parse_args()

    main(args.mongo_log_path)