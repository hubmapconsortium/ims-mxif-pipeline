## IMS pipeline

### Input

To run pipeline you need to create a submission file that contains paths to the datasets 
and some running parameters. Example of submission file is `sample_submission.yaml` 


### Output

Output can be found either in the directory where this pipeline was invoked or 
ata the location of cwltool argument `--outdir`. 


### Requirements

`cwltool` that can run containers with access to GPU: 
https://github.com/hubmapconsortium/cwltool/tree/docker-gpu

Docker containers:
 - vaskivskyi/ims:latest
 - hubmap/cytokit:latest

If not present locally will be downloaded by cwltool.
