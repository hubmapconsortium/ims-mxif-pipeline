#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python", "ims_pipeline/bin/run_cytokit.py"]

inputs:
  pipeline_config:
    type: File
    inputBinding:
      prefix: "--pipeline_config"
  slicer_out_path:
    type: File
    inputBinding:
      prefix: "--slicer_out_path"

outputs:
  cytokit_out_dir:
    type: File
    outputBinding:
      glob: cytokit_out_dir.yaml
