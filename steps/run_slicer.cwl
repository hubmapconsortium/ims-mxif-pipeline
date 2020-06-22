#!/usr/bin/env cwl-runner

cwlVersion: v1.1
class: CommandLineTool
requirements:
  DockerRequirement:
    dockerPull: hubmap/ims-mxif-pipeline:latest
baseCommand: ["python", "/opt/ims_pipeline/bin/run_slicer.py"]

inputs:
  pipeline_config:
    type: File
    inputBinding:
      prefix: "--pipeline_config"
  mxif_dataset_dir_path:
    type: Directory
    inputBinding:
      prefix: "--mxif_dataset_dir_path"
  block_size:
    type: int
    inputBinding:
      prefix: "--block_size"
  overlap:
    type: int
    inputBinding:
      prefix: "--overlap"

outputs:
  slicer_out_dir:
    type: Directory
    outputBinding:
      glob: "tiles"
