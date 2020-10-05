#!/usr/bin/env cwl-runner

cwlVersion: v1.1
class: CommandLineTool
requirements:
  DockerRequirement:
    dockerPull: hubmap/ims-mxif-pipeline:1.3
baseCommand: ["python", "/opt/ims_pipeline/bin/run_combine_ims.py"]

inputs:
  multichannel_ims_ometiff_positive_path:
    type: File
    inputBinding:
      prefix: "--multichannel_ims_ometiff_positive_path"
  multichannel_ims_ometiff_negative_path:
    type: File
    inputBinding:
      prefix: "--multichannel_ims_ometiff_negative_path"

outputs:
  combined_ims:
    type: File
    outputBinding:
      glob: "ims_combined_multilayer.ome.tiff"
