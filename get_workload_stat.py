import pandas as pd 
import argparse 

def get_workload_stat(trace_file):
	df = pd.read_csv(trace_file, header=None, names=["LBA", "R/W"])
	read_count = len(df[df["R/W"] == "r"])
	write_count = len(df[df["R/W"] == "w"])
	unique_rw_block = df.groupby("R/W")["LBA"].nunique()
	# print(unique_rw_block)
	# print(read_count, write_count)
	return read_count, write_count, unique_rw_block

	
if __name__ == "__main__":
	arg_parser = argparse.ArgumentParser(description="Get stats for block traces with format: LBA, read/write.")
	arg_parser.add_argument("trace_file",
		help="Path to the trace file or directory containing only trace files.")
	arg_parser.add_argument("--out",
		help="The output path of the statistics.")
	args = arg_parser.parse_args()

	get_workload_stat(args.trace_file)

