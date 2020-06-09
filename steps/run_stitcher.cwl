#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python", "ims_pipeline/bin/run_stitcher.py"]

inputs:
  pipeline_config:
    type: File
    inputBinding:
      prefix: "--pipeline_config"

  cytokit_out_dir:
    type: File
    inputBinding:
      prefix: "--cytokit_out_dir"

outputs:
  stitched_mask:
    type: File
    outputBinding:
      glob: "./pipeline_output/*_segmentation_mask_stitched.ome.tiff"
