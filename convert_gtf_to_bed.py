import os
import sys
import re
import general_functions

gtf = open(sys.argv[1])
gtfname = sys.argv[1]
gtfname = re.sub(".gtf", "", gtfname)
bed = open(gtfname+".bed", "w")
bed10k = open(gtfname+"_10K.bed","w")

count = 0
first = 1
exon_n = 0
all_exons_start = []
all_exons_size = []
for data in gtf:
    comment = re.compile('^#')
    if not comment.match(data):
        #print(data)
        data = data.strip()
        dataTab = data.split("\t")

        chr = dataTab[0]
        source = dataTab[1]
        feature = dataTab[2]
        start = dataTab[3]
        end = dataTab[4]
        score = dataTab[5]
        strand = dataTab[6]
        frame = dataTab[7]
        attribute = dataTab[8]#
        attributeTab = attribute.split(";")
        geneId = attributeTab[0]
        geneId = geneId.split(" ")[1]
        geneId = re.sub("\"", "", geneId)
        if first == 1:
            first = 0
            if feature == "gene":
                currentGeneId = geneId
                geneStart = start
                all_exons_size = []
                all_exons_start = []
                currentGeneOutput =chr+"\t"+start+"\t"+end+"\t"+geneId+"\t"+score+"\t"+strand+"\t"+source+"\t"+feature+"\t"+frame+"\t"
            else:
                raise Exception("First feature needs to be a gene")
        else:
            if currentGeneId == geneId:
                #print ("same gene")
                if feature == "exon":
                    exon_n += 1
                    exon_size = abs(int(start) - int(end))
                    exon_start = int(start)-int(geneStart)
                    all_exons_size.append(exon_size)
                    all_exons_start.append(exon_start)
                   # print("Exons: "+all_exons_size+" "+all_exons_start)

            else:
                all_exons_size = sorted(all_exons_size)
                all_exons_start = sorted(all_exons_start)

                bed.write(currentGeneOutput+"\t"+str(exon_n)+"\t")
                for size_point in all_exons_size:
                    bed.write(str(size_point)+",")
                bed.write("\t")
                for start_point in all_exons_start:
                    bed.write(str(start_point)+",")
                bed.write("\n")
                if count <= 10000:
                  count +=1
                  bed10k.write(currentGeneOutput + "\t"+str(exon_n)+"\t")
                  for size_point in all_exons_size:
                      bed10k.write(str(size_point) + ",")
                  bed10k.write("\t")
                  for start_point in all_exons_start:
                      bed10k.write(str(start_point) + ",")
                  bed10k.write("\n")
                currentGeneId = geneId
                geneStart = start
                all_exons_size = []
                all_exons_start = []
                exon_n = 0
                currentGeneOutput = chr + "\t" + start + "\t" + end + "\t" + geneId + "\t" + score + "\t" + strand + "\t" + start + "\t" + start + "\t" + frame + "\t"


all_exons_size = sorted(all_exons_size)
all_exons_start = sorted(all_exons_start)

bed.write(currentGeneOutput+"\t"+str(exon_n)+"\t")
for size_point in all_exons_size:
    bed.write(str(size_point)+",")
bed.write("\t")
for start_point in all_exons_start:
    bed.write(str(start_point)+",")
bed.write("\n")



