#!/usr/bin/python
# Continuous integration to see updated tree of Cognitive Atlas concepts and Neurovault images

from pybraincompare.ontology.inference import calculate_reverse_inference_distance
from pybraincompare.mr.datasets import get_standard_mask
import nibabel
from nilearn.image import resample_img
from glob import glob
import pandas
import numpy
import os

print "Reverse Inference!"

base = "./reverse-inference-ci"
data = "%s/data" %(base)
mr = "%s/data/mr" %(base)
output = "%s/output" %(base)
groups = glob("%s/groups/*.pkl" %(data))
input_images = glob("%s/input/*.nii.gz" %base)
print "Found %s input images." %(len(input_images))

results = pandas.DataFrame(columns=["image_id","concept","concept_id","reverse_inference_score"])
standard = nibabel.load("%s/MNI152.nii.gz" %mr)
standard_mask = get_standard_mask()

if not os.path.exists(output):
    os.mkdir(output)

for input_image in input_images:

    image_name = os.path.split(image)[1].replace(".nii.gz","")
    nii = resample_img(input_image,target_affine=standard.get_affine(),target_shape=standard.shape)
    output_file = "%s/%s.nii.gz" %(output,image_name)
    nibabel.save(nii,output_file)

    print "Calculating reverse inference for image %s" %(input_image)
    for node in groups:
        group = pickle.load(open(node,"rb"))

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

results.to_html("%s/index.html" %base)
