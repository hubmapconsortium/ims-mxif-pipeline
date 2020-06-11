#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python", "ims_pipeline/bin/run_cytokit.py"]

inputs:
  pipeline_config:
    type: File
    inputBinding:
      prefix: "--pipeline_config"

  cytokit_config:
    type: File
    inputBinding:
      prefix: "--cytokit_config"

  slicer_out_dir:
    type: Directory
    inputBinding:
      prefix: "--slicer_out_dir"


outputs:
  cytokit_out_dir:
    type: Directory
    outputBinding:
      glob: cytokit_output
