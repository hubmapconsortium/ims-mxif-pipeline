#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python", "/opt/ims_pipeline/bin/run_combine_mxif.py"]

inputs:
  pipeline_config:
    type: File
    inputBinding:
      prefix: "--pipeline_config"

outputs:
  combined_mxif:
    type: File
    outputBinding:
      glob: "./pipeline_output/*_mxif_combined_multilayer.ome.tiff"