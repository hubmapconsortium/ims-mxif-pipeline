#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
requirements:
  DockerRequirement:
    dockerPull: vaskivskyi/ims:latest
baseCommand: ["python", "/opt/ims_pipeline/bin/initiate_pipeline.py"]

inputs:
  submission:
    type: File
    inputBinding:
      prefix: "--path_to_submission_file"


outputs:
  pipeline_config:
    type: File
    outputBinding:
      glob: pipeline_config.yaml

  cytokit_config:
    type: File
    outputBinding:
      glob: cytokit_config.yaml
