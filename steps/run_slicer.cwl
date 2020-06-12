#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python", "/opt/ims_pipeline/bin/run_slicer.py"]

inputs:
  pipeline_config:
    type: File
    inputBinding:
      prefix: "--pipeline_config"

outputs:
  slicer_out_dir:
    type: Directory
    outputBinding:
      glob: "images/Cyc?_reg?"
