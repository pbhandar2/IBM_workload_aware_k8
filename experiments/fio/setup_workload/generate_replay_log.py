import argparse 
import pathlib 


def main(latency_log_path, file_to_replay, output_file_name):
    replay_log_path = pathlib.Path("/mnt/data/replay_logs/").joinpath(output_file_name)

    with replay_log_path.open("w+") as replay_log_handler:

        # header of the replay log 
        replay_log_handler.write("fio version 2 iolog\n")
        replay_log_handler.write("{} add\n".format(file_to_replay))
        replay_log_handler.write("{} open\n".format(file_to_replay))

        with latency_log_path.open("r") as latency_log_handler:
            latency_log_line = latency_log_handler.readline().rstrip()
            while latency_log_line:
                split_latency_log_line = latency_log_line.split(",")

                # gather necessary information from latency log 
                offset = int(split_latency_log_line[-1])
                block_size = int(split_latency_log_line[-2])
                op = int(split_latency_log_line[-3])

                if op == 0:
                    replay_log_handler.write("{} read {} {}\n".format(file_to_replay, op, block_size))
                else:
                    replay_log_handler.write("{} write {} {}\n".format(file_to_replay, op, block_size))

                latency_log_line = latency_log_handler.readline().rstrip()

        # footer of the replay log 
        replay_log_handler.write("{} close\n".format(file_to_replay))


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Generate replay log based on the latency log.")
    parser.add_argument("latency_log_path", type=pathlib.Path, help="Path to latency log")
    parser.add_argument("file_to_replay", help="The path to the file to be reading in the replay log.")
    parser.add_argument("output_file_name", help="The output file name, path is fixed (check code)")
    args = parser.parse_args()

    main(args.latency_log_path, args.file_to_replay, args.output_file_name)