#!/usr/bin/env cwl-runner

cwlVersion: v1.1
class: Workflow

inputs:
  experiment_name:
    type: string
  mxif_dataset_dir_path:
    type: Directory
  multichannel_ims_ometiff_positive_path:
    type: File
  multichannel_ims_ometiff_negative_path:
    type: File

  gpus:
    type: string
    default: "0"
  nuclei_channel:
    type: string
    default: "DAPI"
  block_size:
    type: int
    default: 1000
  overlap:
    type: int
    default: 20

steps:
  initiate_pipeline:
    in:
      experiment_name:
        source: experiment_name
      mxif_dataset_dir_path:
        source: mxif_dataset_dir_path
      multichannel_ims_ometiff_positive_path:
        source: multichannel_ims_ometiff_positive_path
      multichannel_ims_ometiff_negative_path:
        source: multichannel_ims_ometiff_negative_path

      gpus:
        source: gpus
      nuclei_channel:
        source: nuclei_channel
      block_size:
        source: block_size
      overlap:
        source: overlap
    run: steps/initiate_pipeline.cwl
    out: [cytokit_config, pipeline_config]

  run_slicer:
    in:
      pipeline_config:
        source: initiate_pipeline/pipeline_config
      mxif_dataset_dir_path:
        source: mxif_dataset_dir_path
      block_size:
        source: block_size
      overlap:
        source: overlap
    run: steps/run_slicer.cwl
    out: [slicer_out_dir]

  run_cytokit:
    in:
      pipeline_config:
        source: initiate_pipeline/pipeline_config
      cytokit_config:
        source: initiate_pipeline/cytokit_config
      slicer_out_dir:
        source: run_slicer/slicer_out_dir
    run: steps/run_cytokit.cwl
    out: [cytokit_out_dir]

  run_stitcher:
    in:
      pipeline_config:
        source: initiate_pipeline/pipeline_config
      cytokit_out_dir:
        source: run_cytokit/cytokit_out_dir
    run: steps/run_stitcher.cwl
    out: [stitched_mask]

  run_combine_ims:
    in:
      multichannel_ims_ometiff_positive_path:
        source: multichannel_ims_ometiff_positive_path
      multichannel_ims_ometiff_negative_path:
        source: multichannel_ims_ometiff_negative_path
    run: steps/run_combine_ims.cwl
    out: [combined_ims]

  run_combine_mxif:
    in:
      mxif_dataset_dir_path:
        source: mxif_dataset_dir_path
      pipeline_config:
        source: initiate_pipeline/pipeline_config
    run: steps/run_combine_mxif.cwl
    out: [combined_mxif]


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

