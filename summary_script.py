import os

#path_to_GARUDATA = input()
#TODO : Remove the hardcoded directory path

for directory,subdir,files in os.walk('/home/ashwin/Music/ncra-summaryfiles/summary_files/GARUDATA'):
	for fname in files:
		fname = directory + "/" + fname
		fp = open(fname)
		lines = fp.readlines()
		for line in lines:
			if 'processing took' in line:
				if 'day' in line:
					line = line.split(" ")
					total_time = (int(line[3]) * 24 * 60)
					temp_time = line[5].split(":")  
					total_time += int(temp_time[0]) * 60 + int(temp_time[1])
					seconds = temp_time[2]
					print("Total time required for processing is : " + str(total_time) + " minutes " + seconds + " seconds")
				else:
					line = line.split(" ")
					temp_time = line[3].split(":")
					total_time = int(temp_time[0]) * 60 + int(temp_time[1])
					seconds = temp_time[2]
					print("Total time required for processing is : " + str(total_time) + " minutes " + seconds + " seconds") 
			dict = {}
			if 'image' in line:
				line = line.split(" ")
				print(line)
