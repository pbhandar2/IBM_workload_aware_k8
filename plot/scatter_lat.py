import sys
import pandas as pd 
import matplotlib.pyplot as plt

if __name__ == "__main__":
	file_path = sys.argv[1]
	df = pd.read_csv(file_path, header=None, names=["time","lat","rw","size"])
	ax1 = df.plot.scatter(x='time', y='lat', c='DarkBlue')
	print(df["lat"].mean()/1000000)
	plt.show()

