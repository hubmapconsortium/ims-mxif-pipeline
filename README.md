## IMS pipeline

### Input

To run pipeline you need to create a submission file that contains paths to the datasets 
and some running parameters. Example of submission file is `sample_submission.yaml` 


### Output

Output can be found either in the directory where this pipeline was invoked or 
at the location of `cwltool` argument `--outdir`. 

- `segmentation_mask_stitched.ome.tiff`
   Multichannel segmentation mask produced by Cytokit using nuclei channel. 
- `ims_combined_multilayer.ome.tiff` \
   All IMS channels combined together in one OME-TIFF
- `mxif_combined_multilayer.ome.tiff` \
   All MxIF channels combined together in one OME-TIFF
- `cytokit_config.yaml` \
   Configuration file that contain parameters for running Cytokit.
- `pipeline_config.yaml` \
   Runtime parameters that were used in the pipeline.


### Requirements

`cwltool` that can run containers with access to GPU: 
https://github.com/hubmapconsortium/cwltool/tree/docker-gpu

Docker containers:
 - vaskivskyi/ims:latest
 - hubmap/cytokit:latest

If not present locally will be downloaded by `cwltool`.
