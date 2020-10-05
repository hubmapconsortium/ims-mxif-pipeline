#!/usr/bin/env cwl-runner

cwlVersion: v1.1
class: CommandLineTool
requirements:
  DockerRequirement:
    dockerPull: hubmap/ims-mxif-pipeline:1.3
baseCommand: ["python", "/opt/ims_pipeline/bin/run_stitcher.py"]

inputs:
  pipeline_config:
    type: File
    inputBinding:
      prefix: "--pipeline_config"

  cytokit_out_dir:
    type: Directory
    inputBinding:
      prefix: "--cytokit_out_dir"

outputs:
  stitched_mask:
    type: File
    outputBinding:
      glob: "segmentation_mask_stitched.ome.tiff"
