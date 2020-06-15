#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
requirements:
  DockerRequirement:
    dockerPull: vaskivskyi/ims:latest
baseCommand: ["python", "/opt/ims_pipeline/bin/run_combine_ims.py"]

inputs:
  pipeline_config:
    type: File
    inputBinding:
      prefix: "--pipeline_config"

outputs:
  combined_ims:
    type: File
    outputBinding:
      glob: "./pipeline_output/*_ims_combined_multilayer.ome.tiff"