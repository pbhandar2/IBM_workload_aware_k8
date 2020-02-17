import argparse
import os
import numpy as np
import ntpath

import matplotlib 
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt 

def plot_hrc(ax, file_path):
	hit_rate_curve = np.genfromtxt(file_path, delimiter=',')
	hit_rate_curve = hit_rate_curve[hit_rate_curve[:,0].argsort()]
	ax.plot(hit_rate_curve[1:,0], hit_rate_curve[1:,1], label=ntpath.basename(file_path))


if __name__ == "__main__":
	arg_parser = argparse.ArgumentParser(description="Plot HRC of a file or all files in a folder")
	arg_parser.add_argument("data_path",
		help="The path to the HRC file or folder with HRC files.")
	arg_parser.add_argument("--out",
		help="The output path of the plot.")
	args = arg_parser.parse_args()

	plt.figure(figsize=[14, 10])
	plt.rcParams.update({'font.size': 13})
	ax = plt.subplot(1,1,1)

	if os.path.isdir(args.data_path):
		hrc_file_list = os.walk(args.data_path).__next__()[2]
		for hrc_file in hrc_file_list:
			hrc_file_path = os.path.join(args.data_path, hrc_file)
			plot_hrc(ax,hrc_file_path)
	else:
		plot_hrc(ax,args.data_path)

	plt.ylabel("Hit Rate")
	plt.xlabel("Cache Size")
	plt.legend()

	if args.out:
		plt.tight_layout()
		plt.savefig(args.out)
