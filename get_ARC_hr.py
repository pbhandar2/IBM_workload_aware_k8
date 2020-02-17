from PyMimircache import Cachecow 
import sys
import argparse  

def get_hit_ratio_dict_cp_block(input_file, algorithm):
    mimircache = Cachecow()
    params = {
            "init_params": {
                    "label": 1,
                    "real_time": -1,
                    "delimiter": ","
            }
    }
    reader = mimircache.open(input_file)
    return mimircache.get_hit_ratio_dict(algorithm)

if __name__ == "__main__":
	arg_parser = argparse.ArgumentParser(
		description='Get ARC hit rate from a block trace.')

	arg_parser.add_argument('trace_file',
		help='The trace file to be read.')

	arg_parser.add_argument('--trace_type',
		default="cp_block",
		help="""The trace type which dictates how the trace file is read.
			Please check if there is an implementation for your file.""")

	args = arg_parser.parse_args()

	if args.trace_type == "cp_block":
		hit_ratio_dict = get_hit_ratio_dict_cp_block(args.trace_file, "ARC")

