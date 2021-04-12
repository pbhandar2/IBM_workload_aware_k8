import argparse 
import pathlib
import pandas as pd 
import matplotlib.pyplot as plt

DATA_PATH=pathlib.Path("./pv/lat_log/")
OUTPUT_PATH=pathlib.Path("./pv/lat_log_plot")

def main(workload_name):
    clat_file_path = DATA_PATH.joinpath("{}_clat.1.log".format(workload_name))
    plot_path = OUTPUT_PATH.joinpath("{}.png".format(workload_name))
    df = pd.read_csv(clat_file_path, names=["time", "lat", "op", "bs"])
    df.plot.scatter(x="time", y="lat")

    plt.tight_layout()
    plt.savefig(plot_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Generate a latency vs time plot for FIO run.")
    parser.add_argument("workload_name", help="The name of the workload")
    args = parser.parse_args()

    main(args.workload_name)