import os
import sys
import re
import argparse
import general_functions


__version__='v2.0'

if __name__ == '__main__':

	##Load arguments
	parser = argparse.ArgumentParser(prog='format_genome_STAR.py',description = 'Prepare fasta file for STAR aligner')
	parser.add_argument('-v', '--version', action='version', version='%(prog)s-'+__version__)
	parser.add_argument('--input_folder', help='Input folder with fasta file and GTF file')
	parser.add_argument('--output_folder', help='Output for star indexes')
	parser.add_argument('--RAM', help = 'RAM upper limit for genome generation, worked with 150G on mouse')
	args=parser.parse_args()
	print(args)
	input_folder = args.input_folder
	output_folder = args.output_folder
	ramLimit = args.RAM

	inputFiles = os.listdir(input_folder)
	print("Checking if file are compressed")
	inputGZ = [inputFiles[y] for y, x in enumerate(inputFiles) if re.findall("gz", x)]
	if inputGZ:
		print("Files are compressed, unzipping")
		sys.stdout.flush()
		for file in inputGZ:
			os.system("gunzip "+input_folder+"/"+file)
		print("Done")
	else:
		print("Files are not compressed")


	inputFasta = [inputFiles[y] for y, x in enumerate(inputFiles) if re.findall("fa", x)]
	if not inputFasta:
		inputFasta = [inputFiles[y] for y, x in enumerate(inputFiles) if re.findall("fasta", x)]

	inputGTF = [inputFiles[y] for y, x in enumerate(inputFiles) if re.findall("gtf", x)]

	if len(inputFasta)>1:
		sys.exit("More than one fasta file present in the input folder")
	else:
		print("Found fasta file "+str(inputFasta))
	if len(inputGTF)>1:
		sys.exit("More than one gft file present in the input folder")
	else:
		print("Found gtf file "+str(inputGTF))

	print("Running genome indexing")
	general_functions.make_sure_path_exists(output_folder)
	#os.chdir("/mnt/homes/hmg/jb393/")
	#general_functions.make_sure_path_exists("/mnt/homes/hmg/jb393/temp/")
	#os.chdir("/mnt/homes/hmg/jb393/temp/")
	#print(str(os.getcwd()))

	ramLimitG=re.findall("G", ramLimit)
	if ramLimitG:
		ramLimit = ramLimit.strip("G")
		ramLimit = int(ramLimit)*1000000000

	print("Ram limit set to: "+str(ramLimit))
	os.system("STAR --limitGenomeGenerateRAM "+str(ramLimit)+" --runThreadN 8 --runMode genomeGenerate --genomeFastaFiles "+input_folder+"/"+str(inputFasta[0]) +" --sjdbGTFfile "+input_folder+"/"+str(inputGTF[0])+" --genomeDir "+output_folder)
