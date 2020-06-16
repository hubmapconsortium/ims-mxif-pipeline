#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow


inputs:
  - id: cytokit_container_path
    type: File
  - id: cytokit_data_dir
    type: Directory
  - id: mxif_dataset_dir_path
    type: Directory
  - id: multichannel_ims_ometiff_positive_path
    type: File
  - id: multichannel_ims_ometiff_negative_path
    type: File

  - id: ngpus
    type: int
  - id: best_focus_channel
    type: Any
  - id: nuclei_channel
    type: string
  - id: membrane_channel
    type: Any
  - id: block_size
    type: int
  - id: overlap
    type: int

steps:
  - id: initiate_pipeline
    in:
      - id: submission
        source: submission_file
    run: steps/initiate_pipeline.cwl
    out:
      - id: cytokit_config
      - id: pipeline_config

  - id: run_slicer
    in:
      - id: pipeline_config
        source: initiate_pipeline/pipeline_config
    run: steps/run_slicer.cwl
    out:
      - id: slicer_out_dir

  - id: run_cytokit
    in:
      - id: pipeline_config
        source: initiate_pipeline/pipeline_config
      - id: cytokit_config
        source: initiate_pipeline/cytokit_config
      - id: slicer_out_dir
        source: run_slicer/slicer_out_dir
    run: steps/run_cytokit.cwl
    out:
      - id: cytokit_out_dir

  - id: run_stitcher
    in:
      - id: pipeline_config
        source: initiate_pipeline/pipeline_config
      - id: cytokit_out_dir
        source: run_cytokit/cytokit_out_dir
    run: steps/run_stitcher.cwl
    out:
      - id: stitched_mask

  - id: run_combine_ims
    in:
      - id: pipeline_config
        source: initiate_pipeline/pipeline_config
    run: steps/run_combine_ims.cwl
    out:
      - id: combined_ims

  - id: run_combine_mxif
    in:
      - id: pipeline_config
        source: initiate_pipeline/pipeline_config
    run: steps/run_combine_mxif.cwl
    out:
      - id: combined_mxif


outputs:
  pipeline_config:
    outputSource: initiate_pipeline/pipeline_config
    type: File
    label: "Pipeline config"

  cytokit_config:
    outputSource: initiate_pipeline/cytokit_config
    type: File
    label: "Cytokit config"

  stitched_mask:
    outputSource: run_stitcher/stitched_mask
    type: File
    label: "Stitched segmentation mask"

  combined_ims:
    outputSource: run_combine_ims/combined_ims
    type: File
    label: "Combined positive and negative IMS"

  combined_mxif:
    outputSource: run_combine_mxif/combined_mxif
    type: File
    label: "Combined positive and negative MxIF"

