import argparse 
import pathlib
import pandas as pd 
import matplotlib.pyplot as plt
import json 
import numpy as np 
from sklearn.preprocessing import MinMaxScaler

RESULT_PATH=pathlib.Path("./pv/results/")

def main(workload_name):
    data_json = {}
    key_list = []
    for file_path in RESULT_PATH.iterdir():
        if workload_name in file_path.stem:
            split_file_name = file_path.stem.split("_")
            try:
                with file_path.open("r") as f:
                    if len(split_file_name) == 1:
                        data_json["max"] = json.load(f)
                    else:
                        data_json[int(split_file_name[-1])] = json.load(f)
                        key_list.append(int(split_file_name[-1]))
            except ValueError as e:
                print("Error in file {}".format(file_path))
                print(e)

    
    

    mean_latency_array = np.zeros(shape=(len(key_list)+1, 1))
    key_list = sorted(key_list)
    for index, key in enumerate(key_list):
        mean_latency_array[index][0] = data_json[key]['jobs'][0]['read']['clat_ns']['mean']
    else:
        mean_latency_array[len(key_list)][0] = data_json["max"]['jobs'][0]['read']['clat_ns']['mean']


    scaler = MinMaxScaler()
    scaler.fit(mean_latency_array)
    print(scaler.transform(mean_latency_array))



    # print(scaler.transform(mean_latency_list))

    # norm = np.linalg.norm(mean_latency_list)
    # mean_latency_array = np.array(mean_latency_list, dtype=float)/norm

    # print(mean_latency_array)

    # plt.plot(key_list, mean_latency_array)
    # plt.tight_layout()
    # plt.savefig("lat_vs_cache_size.png")






    # clat_file_path = DATA_PATH.joinpath("{}_clat.1.log".format(workload_name))
    # plot_path = OUTPUT_PATH.joinpath("{}.png".format(workload_name))
    # df = pd.read_csv(clat_file_path, names=["time", "lat", "op", "bs"])
    # df.plot.scatter(x="time", y="lat")

    # plt.tight_layout()
    # plt.savefig(plot_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Generate a latency vs time plot for FIO run.")
    parser.add_argument("workload_name", help="The name of the workload")
    args = parser.parse_args()

    main(args.workload_name)