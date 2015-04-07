#!/usr/bin/python

# import modules
import fileinput
import sys

# Open the annotation file to be read
Annotation_file = fileinput.input([sys.argv[1]])
# Open the mapping file to be read
Mapping_file = fileinput.input([sys.argv[2]])
# Create and open the result file
Result_file = open(sys.argv[3], "a")

# Variables, lists and dictionaries
EST_eValue_dict = {}
EST_line_dict = {}
EST_temp_dict = {}
EST_result_list = []
       
# Iterate through each line in the annotation file and tab-delimit.
for line in Annotation_file:
	Annotation_Line = line.split('\t')   
	Annotation_key = Annotation_Line[0]
	Annotation_value = Annotation_Line[3]
	
	EST_line_dict[Annotation_key] = line
	
	# Move to dictionary if annotation is found
	if Annotation_value != 'topnrEvalue' and Annotation_value != 'No_sig_nr_hit':
		for item in line:
			EST_eValue_dict[Annotation_key] = float(Annotation_value)

print "Finished making the EST dictionary"
            
# Iterate through each line in the mapping file and tab-delimit.
for line in Mapping_file:
	Mapping_Line = line.split('\t')
	EST_entries = Mapping_Line[32].split(';')
	Mapping_tag = Mapping_Line[0]
    
	# Check for entries in EST annotation dictionary
	for item in EST_entries:
		if item in EST_eValue_dict:
			EST_temp_dict[item] = EST_eValue_dict[item]
			
	# Check if there are any keys in the dict before next line!
	if len(EST_temp_dict) >= 1:
		min_value = min(EST_temp_dict, key=EST_temp_dict.get)
		min_value = str(min_value)
		EST_result_list.append(min_value)
		del EST_temp_dict[min_value]

		# Write result to file
		line = line.rstrip('\r\n')
		Result_file.write(line)
		Result_file.write('\t')
		Result_file.write(EST_line_dict[EST_result_list[0]])
		EST_temp_dict.clear()
		EST_result_list = list()

print "Finished searching the mapping file against the EST dictionary"

# Close open files     
Annotation_file.close()
Mapping_file.close()
Result_file.close()

print "Script finished"
