
## converting simulations to Rev ##
import sys
import re

calibration_templ = """
tmrca_NODENAME := tmrca(timetree,NODENAME)
n_TMRCA_NODENAME := -(tmrca_NODENAME)
NODENAME_fossil_age <- -FOSSILAGE
NODENAME_true_age <- TRUENODEAGE
NODENAME_lambda <- 1.0 / (NODENAME_true_age - FOSSILAGE)
NODENAME_fossil_snode ~ dnExponential(lambda=NODENAME_lambda, offset=n_TMRCA_NODENAME)
NODENAME_fossil_snode.clamp(NODENAME_fossil_age)
"""

### MAIN ###

nreps = int(sys.argv[1])

rev_temp_fn = "rev_temp.Rev"
file = open(rev_temp_fn, 'rU')
rev_template = file.read()
file.close()

f_prfx = "B_sfbd_"

for i in range(nreps):
	cal_fn = f_prfx + str(i) + ".calrnd_true.cal"
	dat_fn = f_prfx + str(i) + ".dat"
	tre_fn = f_prfx + str(i) + ".SCL.tre"
	out_pfx = "R" + f_prfx + str(i)
	rev_file_name = out_pfx + "_tru_cal.Rev"
	rev_out = rev_template.replace("SEQDATAFILE",dat_fn)
	rev_out = rev_out.replace("TRUETREEFILE",tre_fn)
	rev_out = rev_out.replace("OUTPUTFILEPFX",out_pfx)
	file = open(cal_fn, 'rU')
	cal_d = file.read().strip().split('\n')
	file.close()
	nodes = {}
	clade_names = []
	c = 0
	root_node = []
	oldest = 0.0
	for line in cal_d[1:]:
		l = line.split()
		if(l[1] == 'root'):
			min_age = l[-3]
			tru_age = l[-1]
			root_node = [min_age, tru_age]
			if(float(min_age) > oldest):
				oldest = float(min_age)
		else:
			taxa = l[1:3]
			min_age = l[-3]
			if(float(min_age) > oldest):
				oldest = float(min_age)
			tru_age = l[-1]
			clade = "clade" + str(c)
			clade_names += [clade]
			tax_str = clade + " <- clade(\"" + taxa[0] + "\",\"" + taxa[1] + "\")"
			nodes[clade] = [tax_str, min_age, tru_age]
			c += 1
	constraints_def = ""
	constraints_names = ""
	for j in clade_names:
		constraints_def += nodes[j][0] + "\n"
		constraints_names += j + ", "
	rev_out = rev_out.replace("CLADEVARDEF",constraints_def)
	rev_out = rev_out.replace("ROOTAGEMIN",str(oldest))
	calibration_defs = ""
	for j in clade_names:
		calib = calibration_templ.replace("NODENAME",j)
		foss_age = nodes[j][1]
		true_age = nodes[j][2]
		calib = calib.replace("FOSSILAGE",foss_age)
		calib = calib.replace("TRUENODEAGE",true_age)
		calibration_defs += calib + "\n"
	rev_out = rev_out.replace("CALIBRATIONDEFS",calibration_defs)
	out = open(rev_file_name,'w')
	out.write(rev_out)
	out.close()
			
	