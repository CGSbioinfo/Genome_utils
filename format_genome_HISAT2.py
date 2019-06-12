import os
import sys
import re
import argparse
import general_functions


__version__='v2.0'

if __name__ == '__main__':

	##Load arguments
	parser = argparse.ArgumentParser(prog='format_genome_HISAT2.py',description = 'Prepare fasta file for HISAT aligner')
	parser.add_argument('-v', '--version', action='version', version='%(prog)s-'+__version__)
	parser.add_argument('--input_folder', help='Input folder with fasta file')
	parser.add_argument('--output_folder', help='Output for star indexes')
	args=parser.parse_args()
	print(args)
	input_folder = args.input_folder
	output_folder = args.output_folder

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

	inputFiles = os.listdir(input_folder)
	inputFasta = [inputFiles[y] for y, x in enumerate(inputFiles) if re.findall("fa", x)]
	if not inputFasta:
		fasta_suffix = True
		inputFasta = [inputFiles[y] for y, x in enumerate(inputFiles) if re.findall("fasta", x)]
	else:
		fasta_suffix = False

	inputGTF = [inputFiles[y] for y, x in enumerate(inputFiles) if re.findall("gtf", x)]

	if len(inputFasta)>1:
		sys.exit("More than one fasta file present in the input folder")
	else:
		print("Found fasta file "+str(inputFasta))


	print("Running genome indexing")
	sys.stdout.flush()
	fastaName = inputFasta[0]
	if not fasta_suffix:
		fastaName = fastaName.strip(".fa")
	else:
		fastaName = fastaName.strip(".fasta")

	general_functions.make_sure_path_exists(output_folder)
	os.system("hisat2-build -f "+input_folder+"/"+str(inputFasta[0]) +" "+fastaName)
	general_functions.cleanup_folder_move(pattern = ".ht2", indir = "./", outdir = output_folder )