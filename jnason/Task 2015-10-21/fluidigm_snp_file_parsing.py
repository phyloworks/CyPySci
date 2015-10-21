
# A Fluidigm SNP calling output text file (csv).

input_filename = 'Data/Fpet.Plates05.06.SNPs25.48.csv'  #'Data/Fpet.Plates05.06.SNPs1.24.csv' 'Data/Fpet.Plates05.06.SNPs25.48.csv'

NUMBER_OF_INDIVIDUALS = 192
NUMBER_OF_LOCI = 24
MINIMUM_CONFIDENCE = 0.0    # The minimum call information confidence score, range 0-100.
                            # If the actual score is less that this minimum, the alleles 
                            # will be set to 0. Regardless of the setting here, the alleles 
                            # will be set to 0 if the "converted" genotype call is 
                            # 'No call' or 'NTC'.

print
print '------------------------------------------------'
print 'Top:    Summary information on the SNP data set.'
print 'Bottom: The parsed SNP data set.'
print '------------------------------------------------'
print

# Open and read in input file.
datalist = open(input_filename, 'r').read().splitlines()
open(input_filename, 'r').close()
print 'Input data file: ', input_filename
print


# Delete the first 16 lines of input_filename.
del(datalist[0:16])

if len(datalist)/24 <> NUMBER_OF_INDIVIDUALS:
    print
    print 'ERROR'
    print 'len(datalist/24) <> NUMBER_OF_INDIVIDUALS'
    print 'len(datalist/24) =', len(datalist)/24
    print 'NUMBER_OF_INDIVIDUALS =', NUMBER_OF_INDIVIDUALS
    print
    print 'Program Terminated'
    print
    import sys
    sys.exit(0) 

print 'NUMBER_OF_INDIVIDUALS =', NUMBER_OF_INDIVIDUALS

bases = ['A','C','G','T']
data_matrix = []
locus_missing_values_list = []
for i in range(NUMBER_OF_LOCI):
    locus_missing_values_list.append(0)
    
individual_missing_loci_list = []
for i in range(NUMBER_OF_INDIVIDUALS):
    individual_missing_loci_list.append(0)
    
confidence_list = []
data_rec = []
locus_sum = 0
IndividSum = 0

print 'NUMBER_OF_LOCI =', NUMBER_OF_LOCI
print
locus_names = []
for i in range(NUMBER_OF_LOCI):
    locus_names.append(datalist[i].split(',')[1])
print 'Locus names:',
for i in locus_names:
    print i,
print
print

for line in datalist:
    locus_sum += 1
    if locus_sum == 1:
        IndividSum += 1
    if IndividSum > NUMBER_OF_INDIVIDUALS:
        print
        print 'ERROR'
        print 'IndividSum > NUMBER_OF_INDIVIDUALS'
        print 'IndividSum =', IndividSum
        print 'NUMBER_OF_INDIVIDUALS =', NUMBER_OF_INDIVIDUALS
        print
        print 'Program Terminated'
        print
        import sys
        sys.exit(0) 
        
    line = line.split(',')
    if locus_sum == 1:
        TreeID = line[4]
        data_rec.append(TreeID)
    
    confidence_score = float(line[7])
    if confidence_score > 0.001:
        confidence_list.append(confidence_score)
    call = line[9].upper()
    
    if (confidence_score < MINIMUM_CONFIDENCE) or (call == 'NO CALL') or (call == 'NTC'):
        data_rec.append(0)
        data_rec.append(0)
        locus_missing_values_list[locus_sum-1] += 1
        individual_missing_loci_list[IndividSum-1] += 1
    else:
        call = call.split(':')
        allele_1 = call[0]
        allele_1 = bases.index(allele_1)+1
        allele_2 = call[1]
        allele_2 = bases.index(allele_2)+1

        if allele_1 <= allele_2:
            data_rec.append(allele_1)
            data_rec.append(allele_2)
        else:
            data_rec.append(allele_2)
            data_rec.append(allele_1)   

    if locus_sum == NUMBER_OF_LOCI:
        data_matrix.append(data_rec)
        data_rec = []
        locus_sum = 0


import numpy
print 'SNP call confidence score mean and std: %6.2f  %6.2f' % (numpy.mean(confidence_list), numpy.std(confidence_list))
print

locus_name_width = max(len(name) for name in locus_names) + 2  # padding
print 'Proportion of missing genotypes per locus (assay):'
for i in range(len(locus_missing_values_list)):
    locus_missing_values_list[i] = locus_missing_values_list[i]*(1/float(NUMBER_OF_INDIVIDUALS))
    print '%s %5.2f' % (locus_names[i].ljust(locus_name_width), locus_missing_values_list[i])
print

col1_width = max(len(word) for row in data_matrix for word in row[0:1]) + 2  # padding
for i in range(len(individual_missing_loci_list)):
    individual_missing_loci_list[i] = individual_missing_loci_list[i]*(1/float(NUMBER_OF_LOCI))
print 'Proportion of missing (no call) loci per individual:'
for i in range(NUMBER_OF_INDIVIDUALS):
    print '%s  %5.2f' % (data_matrix[i][0].ljust(col1_width), individual_missing_loci_list[i])
print 'Average:          %4.2f' % (sum(individual_missing_loci_list)/float(NUMBER_OF_INDIVIDUALS))
print
print

print 'The parsed SNP data table in NasonFile format:'
print
print '# Input filename =', input_filename
print 'allele_delimiter = whitespace'
print 'inheritance = codominant'
print 'locus_names =',
for locus in locus_names:
    print locus,
print
for row in data_matrix:
    print row[0].ljust(col1_width),
    for col in row[1:]:
        print col,
    print

