import pandas as pd
filename = "testfile.txt"														
df_combined = pd.read_csv(filename)												
geneid_prev = "null"
evalue_prev = "null"
index_prev = "null"
print("#######################")
for row in df_combined.itertuples():
	current_geneid = df_combined.iloc[2]  #### This is the problem area. Can't grab from column (look at how we did it earlier)
	current_evalue = df_combined.iloc[4]
	if current_geneid.str.match(geneid_prev, as_indexer = True) is True: 
		if current_evalue >= evalue_prev:
			df_combined.drop()
		elif current_evalue <= evalue_prev:
			df_combined.drop(index_prev)
			geneid_prev = current_geneid
			evalue_prev = current_evalue
			index_prev = df_combined.iloc[0]
		elif current_evalue == evalue_prev:
			df_combined.drop(index_prev)						#delete previous row if same evalue, or flag for us to look at it?
			geneid_prev = current_geneid
			evalue_prev = current_evalue
			index_prev = df_combined.iloc[0]
		print("is True")
	elif current_geneid.str.match(geneid_prev, as_indexer = True) is not True:
		geneid_prev = current_geneid
		evalue_prev = current_evalue
		index_prev = df_combined.iloc[0]
		print("is not True")
		
print(df_combined)
