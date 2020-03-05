from PyMimircache import Cachecow 
import sys
import argparse  

def get_mimircache_cp_block(input_file):
	mimircache = Cachecow()
    params = {
            "init_params": {
                    "label": 1,
                    "real_time": -1,
                    "delimiter": ","
            }
    }
    mimircache.open(input_file)
    return mimircache

def get_hit_count_dict_cp_block(input_file, algorithm, cache_size):
	mimircache = get_mimircache_cp_block(input_file)
	hit_count = get_hit_count_dict(algorithm, cache_size, use_general_profiler=True)
	return hit_count 

def get_hit_ratio_dict_cp_block(input_file, algorithm, cache_size):
	mimircache = get_mimircache_cp_block(input_file)
    reader = mimircache.open(input_file)
    return mimircache.get_hit_ratio_dict(algorithm, cache_size=cache_size)

if __name__ == "__main__":
	arg_parser = argparse.ArgumentParser(
		description='Get hit rate from a block trace.')

	arg_parser.add_argument('trace_file',
		help='The trace file to be read.')

	arg_parser.add_argument('algorithm',
		help='The replacement algorithm to use.')

	arg_parser.add_argument('--trace_type',
		default="cp_block",
		help="""The trace type which dictates how the trace file is read.
			Please check if there is an implementation for your file.""")

	arg_parser.add_argument('--cache_size',
		default=256*5*1024,
		help='The size of the cache (in terms of 4K pages). Default is 5GB.')

	arg_parser.add_argument('--out_path',
		default=None,
		help='The path of the file to write the hit rate curve to.')

	args = arg_parser.parse_args()

	if args.trace_type == "cp_block":
		hit_count_dict = get_hit_count_dict_cp_block(args.trace_file, args.algorithm, args.cache_size)
		print(hit_count_dict)



