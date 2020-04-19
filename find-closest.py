import numpy as np
from decimal import Decimal
import os
import matplotlib.pyplot as plt

STRAT_DIR = "/home/djb236/FINAL2/STRATIFIED/Ta=7.50E+05/Phi=30/"
BOUS_FILE = "/home/djb236/FINAL2/Ro_collected.txt"
SAVE_DIR = "/home/djb236/FINAL2/STRATIFIED/Ta=7.50E+05/"

strat_f = open(STRAT_DIR + "Ro.dat", "r")
strat_raw = strat_f.read()
strat_f.close()

bous_f = open(BOUS_FILE, "r")
bous_raw = bous_f.read()
bous_f.close()

def file_exists (fname, dir):
	found = False
	for f in dir:
		if (f == fname):
			found = True
			break

	return found

def match_bous (strat_Ro):
	smallest_diff = 1
	Ro_best = 5
	Ta_best = -1
	for line in bous_raw.split("\n"):
		if (line != ""):
			Ro = float(line.split(",")[1])
			if ( (Ro - strat_Ro)**2 < smallest_diff ):
				smallest_diff = (Ro - strat_Ro)**2
				Ro_best = Ro
				Ta_best = float(line.split(",")[0].split("=")[1])

	if ( np.sqrt(( 1 - (strat_Ro/Ro_best) )**2) < 0.01):
		return Ta_best, Ro_best
	else:
		return -1, -1

def change_to_strings (nums):
	arr = []
	for num in nums:
		arr.append('%.2E' % Decimal (str(num)))

	return arr

def find_param (str, param):
	retval = ""
	for line in str.split("\n"):
		if (line != ""):
			if (line.split("=")[0].strip() == param.strip()):
				retval += line.split("=")[1].strip()
				break

	return retval

def get_strat_data (components):
	f = open(STRAT_DIR + "RS_" + components + "_z_rms.dat", "r")
	f_raw = f.read()
	f.close()

	RS, y = [], []
	for line in f_raw.split("\n"):
		if (line != ""):
			y.append(float(line.split(",")[0]))
			RS.append(float(line.split(",")[1]))

	return RS, y

def plot_comp (strat_data, matched_y, matched_RS, comp):
	plt.plot(strat_data[0], strat_data[1], label="Stratified")
	plt.scatter(matched_RS, matched_y, s=15, label="Boussinesq", c="red")
	# plt.xscale("log")
	plt.legend()
	plt.title("RS_" + comp)
	plt.savefig(SAVE_DIR + "RS_" + comp + "_comparison.png")
	plt.clf()


matched_Tas = []
matched_y = []
matched_Ros = []
strat_Ros = []
strat_y = []
matched_count = 0
for layer in strat_raw.split("\n"):
	if (layer != "" and layer.find("Ro") == -1):
		strat_Ro = float(layer.split(",")[1])
		strat_Ros.append(strat_Ro)
		strat_y.append(float(layer.split(",")[0]))
		matched_Ta, matched_Ro = match_bous (strat_Ro)
		if (matched_Ta != -1):
			matched_Ros.append(matched_Ro)
			matched_y.append(float(layer.split(",")[0]))
			matched_count += 1
			matched_Tas.append(matched_Ta)
			print("Stratified " + str(strat_Ro) + " matched with boussinesq Ta=" + str(matched_Ta) + " (Ro=" + str(matched_Ro) + ")")

print("Matched " + str(matched_count))
print(matched_Tas)

Tas_array = change_to_strings (matched_Tas)


RS_uv = []
RS_uw = []
RS_vw = []

base_dir = "/home/djb236/FINAL2"
for Ta in Tas_array:
	os.chdir(base_dir + "/Ta=" + Ta)

	for Phi in os.listdir():
		os.chdir(base_dir + "/Ta=" + Ta + "/" + Phi)

		if (file_exists ("averages.txt", os.listdir())):
			f = open("averages.txt", "r")
			f_raw = f.read()
			f.close()
			RS_uv.append(float(find_param (f_raw, "RS_uv_z rms")))
			RS_uw.append(float(find_param (f_raw, "RS_uw_z rms")))
			RS_vw.append(float(find_param (f_raw, "RS_vw_z rms")))

print("RS_uv:")
for i in range(len(matched_y)):
	print(str(matched_y[i]) + "," + str(RS_uv[i]))

print("RS_uw:")
for i in range(len(matched_y)):
	print(str(matched_y[i]) + "," + str(RS_uw[i]))

print("RS_vw:")
for i in range(len(matched_y)):
	print(str(matched_y[i]) + "," + str(RS_vw[i]))

plot_comp(get_strat_data ("uv"), matched_y, RS_uv, "uv")
plot_comp(get_strat_data ("uw"), matched_y, RS_uw, "uw")
plot_comp(get_strat_data ("vw"), matched_y, RS_vw, "vw")

plt.plot(strat_Ros, strat_y, label="Stratified")
plt.scatter(matched_Ros, matched_y, s=15, label="Boussinesq", c="red")
print(strat_y)
print(matched_y)
plt.ylabel("z")
plt.xlabel("Ro")
plt.legend()
plt.savefig(SAVE_DIR + "Ro_comparison.png")
plt.clf()
