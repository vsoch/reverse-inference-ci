# Reverse Inference Scores for a Query Image

[![Circle CI](https://circleci.com/gh/vsoch/reverse-inference-ci.svg?style=svg)](https://circleci.com/gh/vsoch/reverse-inference-ci)

This is a continuous integration "reproducible repo," meaning that you can submit a PR to the branch with your image of interest in the reverse-inference-ci/input folder, and a results report will be generated to show a reverse inference score for your image against all Cognitive Atlas Concepts, defined at the timepoint (and with same image sets as) this [recent work](http://www.github.com/vsoch/semantic-image-comparison). In this work, we show the value of semantic image comparison, and you can view the entire set of our images at their corresponding tagged nodes at this [web interface](http://www.vsoch.github.io/semantic-image-comparison-web).

# Instructions

First fork the repo on github. Then clone your fork

      git clone http://www.github.com/[your-username]/reverse-inference-ci

Then add your images to the [reverse-inference-ci/input](reverse-inference-ci/input) folder

Push to your master

      git push origin master

Then submit a PR (pull request) to the original repo. Go to the circle link at the button above to watch the analysis run.
Finally, browse to Artifacts --> /home/ubuntu/reverse-inference-ci/index.html and click the file to review your results table.

