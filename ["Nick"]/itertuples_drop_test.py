import pandas as pd
filename = "testfile.txt"														
test_df = pd.read_csv(filename)	
											
geneid_prev = "start"
evalue_prev = "start"
i = 0
print("#######################")

test_df.drop("c10_2") #cant drop row based on index, for some reason
"""
for row in test_df.itertuples():
	geneid_current = test_df.iloc[i,1] 
	evalue_current = test_df.iloc[i,3]

	if geneid_current == geneid_prev: 
		print(geneid_current, "is equal to", geneid_prev)
		if evalue_current >= evalue_prev:
			print(evalue_current, "is greater than", evalue_prev, "should drop this row")
			test_df.drop(test_df.index[i])
			
		elif evalue_current <= evalue_prev:
			print(evalue_current, "is less than", evalue_prev, "should drop previous row")
			test_df.drop(test_df.index[i-1])
			geneid_prev = geneid_current
			evalue_prev = evalue_current
			
		elif evalue_current == evalue_prev:
			print(evalue_current, "is equal to", evalue_prev, "should drop previous row")
			test_df.drop(test_df.index[i-1])						#delete previous row if same evalue, or flag for us to look at it?
			geneid_prev = geneid_current
			evalue_prev = evalue_current
			
	else:
		print(geneid_current, "is not equal to", geneid_prev)
		geneid_prev = geneid_current
		evalue_prev = evalue_current
		
	i = i + 1
"""
print(test_df)
