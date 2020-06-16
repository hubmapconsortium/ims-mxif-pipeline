#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
requirements:
  DockerRequirement:
    dockerPull: vaskivskyi/ims:latest
baseCommand: ["python", "/opt/ims_pipeline/bin/initiate_pipeline.py"]

inputs:
  experiment_name:
    type: string
    inputBinding:
      prefix: "--experiment_name"
  cytokit_container_path:
    type: File
    inputBinding:
      prefix: "--cytokit_container_path"
  cytokit_data_dir:
    type: Directory
    inputBinding:
      prefix: "--cytokit_data_dir"
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

  ngpus:
    type: int
    inputBinding:
      prefix: "--ngpus"
  best_focus_channel:
    type: Any
    inputBinding:
      prefix: "--best_focus_channel"
  nuclei_channel:
    type: string
    inputBinding:
      prefix: "--nuclei_channel"
  membrane_channel:
    type: Any
    inputBinding:
      prefix: "--membrane_channel"
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
      glob: pipeline_config.yaml

  cytokit_config:
    type: File
    outputBinding:
      glob: cytokit_config.yaml
