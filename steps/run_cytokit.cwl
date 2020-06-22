#!/usr/bin/env cwl-runner

class: CommandLineTool
cwlVersion: v1.1
baseCommand: ["sh", "conda_init.sh"]

hints:
  DockerRequirement:
    dockerPull: hubmap/cytokit:latest
    dockerOutputDirectory: "/lab/cytokit_output"
  DockerGpuRequirement: {}

  InitialWorkDirRequirement:
    listing:

      - entryname: conda_init.sh
        entry: |-
          __conda_setup="\$('/opt/conda/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
          if [ \$? -eq 0 ]; then
             eval "\$__conda_setup"
          else
             if [ -f "/opt/conda/etc/profile.d/conda.sh" ]; then
                 . "/opt/conda/etc/profile.d/conda.sh"
             else
                 export PATH="/opt/conda/bin:$PATH"
             fi
          fi
          unset __conda_setup

          export PYTHONPATH=/lab/repos/cytokit/python/pipeline
          conda activate cytokit

          cytokit processor run_all --data-dir $(inputs.slicer_out_dir.path) --config-path $(inputs.cytokit_config.path) --output-dir /lab/cytokit_output


inputs:
  pipeline_config:
    type: File

  cytokit_config:
    type: File

  slicer_out_dir:
    type: Directory


outputs:
  cytokit_out_dir:
    type: Directory
    outputBinding:
      glob: /lab/cytokit_output
