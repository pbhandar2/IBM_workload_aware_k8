import argparse 
import pathlib 
import json 
import os 
from os.path import dirname, abspath

BASE_CONFIG = {
    "cache_dir":"/cache",
    "page_size":4096,
    "caches":[{
        "replacement_policy":"LRU",
        "size":128000, 
        "dir":"*"
    }]
}


CONFIG_PATH = pathlib.Path(dirname(abspath(__file__))).joinpath("config")


def main(memory_size_mb, fs_type, page_size, output_path):
    output_file_name="lru_{}_{}.json".format(fs_type, memory_size_mb)
    output_path = output_path.joinpath(output_file_name)

    config = dict(BASE_CONFIG)
    config["page_size"] = page_size*1024 # KB to bytes 
    config["caches"][0]["size"] = int(memory_size_mb*1024/page_size)

    with output_path.open("w+") as json_handle:
        json.dump(config, json_handle)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate configuration based on the input")
    parser.add_argument("memory_mb", type=int, help="The memory size in MB")
    parser.add_argument("fs_type", help="The type of FS (determines certain configurations of KubeCacheFS)")
    parser.add_argument("--ps", type=int, default=4, help="The page size in KB")
    parser.add_argument("--output_dir", type=pathlib.Path, \
        default=pathlib.Path(CONFIG_PATH), help="The output path of the config file")
    args = parser.parse_args()
    main(args.memory_mb, args.fs_type, args.ps, args.output_dir)


