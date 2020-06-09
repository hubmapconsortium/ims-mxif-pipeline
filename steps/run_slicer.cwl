#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python", "ims_pipeline/bin/run_slicer.py"]

inputs:
  pipeline_config:
    type: File
    inputBinding:
      prefix: "--pipeline_config"

outputs:
  slicer_out_path:
    type: File
    outputBinding:
      glob: slicer_out_path.yaml
