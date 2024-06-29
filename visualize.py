
import json
import matplotlib.pyplot as plt
import numpy as np

from datetime import datetime

def sort_dict_asc(dic: dict) -> list | list:
	sorted_dict = sorted(dic.items(), key=lambda x: x[1])
	sorted_keys = [item[0] for item in sorted_dict]
	sorted_vals = [item[1] for item in sorted_dict]
	return sorted_keys, sorted_vals

def generate_two_barh(labels: str, values: float, k: int = 12, save_path: str ="summary_stats.png",
	tick_rot: int = 0, xlim: int = 25) -> None:
	
	y_pos = np.arange(len(labels[-k:]))

	plt.figure(figsize=(12, 5))

	plt.subplot(1,2,1)
	top_labs = labels[-k:]
	top_vals = values[-k:]
	plt.barh(y_pos, top_vals, color='limegreen') # label-value pairs are sorted in asc order so grab top k
	plt.yticks(y_pos, top_labs, rotation=tick_rot)
	plt.xlim(left=top_vals[0]-xlim, right=top_vals[-1]+xlim)
	plt.title(f"Top {k} Career Choices")
	plt.xlabel("Elo")

	plt.subplot(1,2,2)
	bot_labs = labels[:k]
	bot_vals = values[:k]
	plt.barh(y_pos, bot_vals, color='red')
	plt.yticks(y_pos, bot_labs, rotation=tick_rot)
	plt.xlim(left=bot_vals[0]-xlim, right=bot_vals[-1]+xlim)
	plt.title(f"Bottom {k} Career Choices")
	plt.xlabel("Elo")

	date, time =  datetime.now().strftime("%m/%d/%Y"), datetime.now().strftime("%I:%M:%S %p")

	plt.figtext(0.01, 0.01, f"Last Updated: {date}, {time}",
         horizontalalignment='left', 
         verticalalignment='bottom')

	plt.tight_layout()

	plt.savefig(save_path)

def sort_and_generate(elos: dict) -> None:
	sorted_keys, sorted_vals = sort_dict_asc(elos)
	generate_two_barh(labels=sorted_keys, values=sorted_vals)
