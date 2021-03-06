#!/usr/bin/python
# Continuous integration to see updated tree of Cognitive Atlas concepts and Neurovault images

from pybraincompare.ontology.inference import calculate_reverse_inference_distance
from pybraincompare.mr.datasets import get_standard_mask
import nibabel
from nilearn.image import resample_img
from glob import glob
import pandas
import pickle
import numpy
import os

print "Reverse Inference!"

base = "./reverse-inference-ci"
data = "%s/data" %(base)
mr = "%s/data/mr" %(base)
output = "%s/output" %(base)
templates = "%s/template" %(base)
groups = glob("%s/groups/*.pkl" %(data))
input_images = glob("%s/input/*.nii.gz" %base)
print "Found %s input images." %(len(input_images))

results = pandas.DataFrame(columns=["image_id","concept","concept_id","reverse_inference_score"])
standard = nibabel.load("%s/MNI152.nii.gz" %mr)
standard_mask = get_standard_mask()

if not os.path.exists(output):
    os.mkdir(output)

for input_image in input_images:

    image_name = os.path.split(input_image)[1].replace(".nii.gz","")
    nii = resample_img(input_image,target_affine=standard.get_affine(),target_shape=standard.shape)
    output_file = "%s/%s.nii.gz" %(output,image_name)
    nibabel.save(nii,output_file)

    print "Calculating reverse inference for image %s" %(input_image)
    for node in groups:
        group = pickle.load(open(node,"rb"))

        print "Calculating against concept %s..." %(group["name"])
        # Remove image from the in and out groups
        in_group = ["%s/%s" %(mr,x) for x in group["in"]]
        out_group = ["%s/%s" %(mr,x) for x in group["out"]]
        in_count = len(in_group) 
        out_count = len(out_group)

        # REVERSE INFERENCE: OVERVIEW
        # Calculate reverse inference (posterior) for query image
        # P(node mental process|activation) = P(activation|mental process) * P(mental process)
        # divided by
        # P(activation|mental process) * P(mental process) + P(A|~mental process) * P(~mental process)
        # P(activation|mental process): my voxelwise prior map

        # REVERSE INFERENCE: DISTANCE METRIC #########################################################
        # This is a reverse inference score, the p(cognitive process | query)
        ri = calculate_reverse_inference_distance(nii,in_group,out_group,standard_mask)
        results.loc["%s_%s" %(image_name,group["nid"])] = [image_name,group["name"],group["nid"],ri]

print "Saving result to /home/ubuntu/reverse-inference-ci/index.html..."

# Prepare rendered table
table = '<table id="fresh-table" class="table">\n<thead>\n'
fields = results.columns.tolist()
for field in fields:
    table = '%s<th data-field="%s" data-sortable="true">%s</th>' %(table,field,field)
table = '%s\n</thead>\n<tbody>\n' %(table)

for row in results.iterrows():
    table = "%s<tr>\n" %(table)
    for field in row[1]:
        table = "%s<td>%s</td>\n" %(table,field)
    table = "%s</tr>\n" %(table)

table = "%s</tbody></table>\n" %(table)

# Write the new table
table_template = "".join(open("%s/table.html" %templates,"rb").readlines())
table_template = table_template.replace("[[SUB_TABLE_SUB]]",table)
filey = open("index.html","wb")
filey.writelines(table_template)
filey.close()

# Finally, save other versions of data for download
results.to_csv("reverse-inference-ci-results.tsv",sep="\t")
results.to_json("reverse-inference-ci-results.json")
