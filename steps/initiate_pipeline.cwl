#!/usr/bin/env cwl-runner

cwlVersion: v1.1
class: CommandLineTool
requirements:
  DockerRequirement:
    dockerPull: hubmap/ims-mxif-pipeline:1.2
baseCommand: ["python", "/opt/ims_pipeline/bin/initiate_pipeline.py"]

inputs:
  experiment_name:
    type: string
    inputBinding:
      prefix: "--experiment_name"
  mxif_dataset_dir_path:
    type: Directory
    inputBinding:
      prefix: "--mxif_dataset_dir_path"
  multichannel_ims_ometiff_positive_path:
    type: File
    inputBinding:
      prefix: "--multichannel_ims_ometiff_positive_path"
  multichannel_ims_ometiff_negative_path:
    type: File
    inputBinding:
      prefix: "--multichannel_ims_ometiff_negative_path"

  gpus:
    type: string
    inputBinding:
      prefix: "--gpus"
  nuclei_channel:
    type: string
    inputBinding:
      prefix: "--nuclei_channel"
  block_size:
    type: int
    inputBinding:
      prefix: "--block_size"
  overlap:
    type: int
    inputBinding:
      prefix: "--overlap"

outputs:
  pipeline_config:
    type: File
    outputBinding:
      glob: './pipeline_output/pipeline_config.yaml'

  cytokit_config:
    type: File
    outputBinding:
      glob: './pipeline_output/cytokit_config.yaml'
