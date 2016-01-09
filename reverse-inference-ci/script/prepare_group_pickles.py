# This script will prepare the pickles from the semantic image comparison analysis to be used on continuous integration, basically removing file paths from the processing cluster
from glob import glob
import pickle
import os
group_pickles = glob("../data/groups/*.pkl")

for group_pickle in group_pickles:
    print "Preparing group pickle %s" %group_pickle
    group = pickle.load(open(group_pickle,"rb"))
    group["in"] = [os.path.split(x)[-1] for x in group["in"]]
    group["out"] = [os.path.split(x)[-1] for x in group["out"]]
    pickle.dump(group,open(group_pickle,"wb"))
