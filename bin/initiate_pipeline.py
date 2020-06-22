import os
import os.path as osp
import argparse
import shutil

import yaml

import generate_pipeline_config
import generate_cytokit_config


def create_base_dirs(out_dir: str):
    dir_paths = dict(meta_dir=osp.join(out_dir, 'meta'),
                     images_dir=osp.join(out_dir, 'images'),
                     pipeline_output_dir=osp.join(out_dir, 'pipeline_output')
                     )

    for path in dir_paths.values():
        if not osp.exists(path):
            os.makedirs(path)
    return dir_paths


def main(experiment_name, mxif_dataset_dir_path,
         multichannel_ims_ometiff_positive_path, multichannel_ims_ometiff_negative_path,
         ngpus, nuclei_channel, block_size, overlap):

    __location__ = osp.realpath(osp.join(os.getcwd(), osp.dirname(__file__)))

    base_pipeline_dir = '.'
    dir_paths = create_base_dirs(base_pipeline_dir)

    submission = dict(experiment_name=experiment_name,
                      mxif_dataset_dir_path=mxif_dataset_dir_path,
                      multichannel_ims_ometiff_positive_path=multichannel_ims_ometiff_positive_path,
                      multichannel_ims_ometiff_negative_path=multichannel_ims_ometiff_negative_path,
                      ngpus=ngpus,
                      nuclei_channel=nuclei_channel,
                      block_size=block_size,
                      overlap=overlap
                      )
    pipeline_config_path = osp.join(dir_paths['pipeline_output_dir'], 'pipeline_config.yaml')
    generate_pipeline_config.main(submission, base_pipeline_dir, pipeline_config_path)

    cytokit_config_path = osp.join(dir_paths['pipeline_output_dir'], 'cytokit_config.yaml')
    generate_cytokit_config.main(pipeline_config_path, cytokit_config_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--experiment_name', type=str, help='experiment name will be used for naming files and folders')
    parser.add_argument('--mxif_dataset_dir_path', type=str,
                        help='path to directory with MxIF datasets. Contains two directories: processedMicroscopy, rawMicroscopy')
    parser.add_argument('--multichannel_ims_ometiff_positive_path', type=str,
                        help='path positive multichannel IMS OME-TIFF')
    parser.add_argument('--multichannel_ims_ometiff_negative_path', type=str,
                        help='path negative multichannel IMS OME-TIFF')
    parser.add_argument('--ngpus', type=int, help='number of gpus to use')
    parser.add_argument('--nuclei_channel', type=str, help='Channel that will be used for nucleus segmentation')
    parser.add_argument('--block_size', type=int, help='size of one tile for image segmentation')
    parser.add_argument('--overlap', type=int, help='size of overlap for one edge (each image has 4 overlapping edges)')
    args = parser.parse_args()

    main(args.experiment_name, args.mxif_dataset_dir_path,
         args.multichannel_ims_ometiff_positive_path, args.multichannel_ims_ometiff_negative_path,
         args.ngpus, args.nuclei_channel, args.block_size, args.overlap)
