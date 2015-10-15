
## converting simulations to Rev ##
import sys



### MAIN ###

nreps = int(sys.argv[1])

f_prfx = "B_sfbd_"

for i in range(nreps):
	cal_fn = f_prfx + str(i) + ".calrnd_true.cal"
	dat_fn = f_prfx + str(i) + ".dat"
	tre_fn = f_prfx + str(i) + ".SCL.tre"
	file = open(cal_fn, 'rU')
	cal_d = file.read().strip().split('\n')
	file.close()
	data = {}
	for line in cal_d[1:]:
		l = line.split()
		print(l)
	