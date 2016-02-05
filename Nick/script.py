import pandas as pd
import numpy as np

filename = "tempname.txt"

df = pd.read_csv(filename)

################################
#take column C plus column D to create column L at the end
################################

"""weight = df.alignlen + df.mismatch
df["L"] = weight
print(df.head(4))"""

### To add geneid & isoformnum columns to .txt file, find: ^(c.*_.*_i[0-9]+,)(c.*_.*)(_i)([0-9]+)(,) , replace: \1\1\2,\4, ###
    
unique_genes_per_ref = df.groupby(by='ref').geneid.nunique().reset_index()
#print(unique_genes_per_ref)

#len(unique_genes_per_ref.axes)

pd.DataFrame(unique_genes_per_ref)

#To turn atextfile.txt into comma separated .txt file with 2 columns!
#From Desktop, open atextfile.txt in Notepad++. Create header (Ref, UniqueIDs). Find: ^([^\s]+)\s+([^\s])+ Replace: \1,\2 
#Save as: "unique_genes_per_ref.txt"

filename_unique_genes_per_ref = "unique_genes_per_ref.txt"
unique_genes_per_ref_csv = pd.read_csv(filename_unique_genes_per_ref)
#print(unique_genes_per_ref_csv)

unique_genes_per_ref_csv_ONEs = (unique_genes_per_ref_csv.loc[unique_genes_per_ref_csv['UniqueIDs'] == 1])
#print(unique_genes_per_ref_csv_ONEs)

unique_genes_per_ref_csv_ONEs_List =  unique_genes_per_ref_csv_ONEs['Ref'].tolist()
#print(unique_genes_per_ref_csv_ONEs_List), print(type(unique_genes_per_ref_csv_ONEs_List))

#NOT NEEDED, KEEP IN CASE
#totals_unique_genes_per_ref = df.groupby(by='ref').geneid.nunique().value_counts()
#print(totals_unique_genes_per_ref)

#NOT NEEDED, KEEP IN CASE
#binned_unique_genes_per_ref = pd.cut(x=unique_genes_per_ref, bins=1)
#print(binned_unique_genes_per_ref)

unique_match_per_geneid = df.groupby(by='geneid').ref.nunique()
#print(unique_match_per_geneid)

#NOT NEEDED, KEEP IN CASE
#totals_unique_match_per_geneid = df.groupby(by='geneid').ref.nunique().value_counts()
#print(totals_unique_match_per_geneid)

unique_match_per_geneid.to_string('atextfile2.txt')

#To turn atextfile2.txt into comma separated .txt file with 2 columns!
#From Desktop, open atextfile2.txt in Notepad++. Create header. Find: ^([^\s]+)\s+([^\s])+ Replace: \1,\2
#Save as: "unique_match_per_geneid.txt"

filename_unique_match_per_geneid = "unique_match_per_geneid.txt"
unique_match_per_geneid_csv = pd.read_csv(filename_unique_match_per_geneid)
#print(unique_genes_per_ref_csv)

unique_match_per_geneid_csv_ONEs = (unique_match_per_geneid_csv.loc[unique_match_per_geneid_csv['UniqueMatch'] == 1])
#print(unique_match_per_geneid_csv_ONEs)

unique_match_per_geneid_csv_ONEs_List =  unique_match_per_geneid_csv_ONEs['geneid'].tolist()
#print(unique_match_per_geneid_csv_ONEs_List), print(type(unique_match_per_geneid_csv_ONEs_List))

###Filter original CSV. First: Get rows by 'ref' (column), Second: Get rows by 'geneid' (column)