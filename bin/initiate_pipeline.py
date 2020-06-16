import os
import os.path as osp
import argparse
import shutil

import yaml

import collect_meta
import generate_cytokit_config


def create_base_dirs(out_dir: str):
    dir_paths = dict(meta_dir=osp.join(out_dir, 'meta'),
                     images_dir=osp.join(out_dir, 'images'),
                     cytokit_output_dir=osp.join(out_dir, 'cytokit_output'),
                     cytokit_data_dir=osp.join(out_dir, 'cytokit_data'),
                     pipeline_output_dir=osp.join(out_dir, 'pipeline_output')
                     )

    for path in dir_paths.values():
        if not osp.exists(path):
            os.makedirs(path)
    return dir_paths


def main(epxeriment_name, cytokit_container_path, cytokit_data_dir, mxif_dataset_dir_path,
         multichannel_ims_ometiff_positive_path, multichannel_ims_ometiff_negative_path,
         ngpus, best_focus_channel, nuclei_channel, membrane_channel, block_size, overlap):
    __location__ = osp.realpath(osp.join(os.getcwd(), osp.dirname(__file__)))

    base_pipeline_dir = os.getcwd()
    dir_paths = create_base_dirs(base_pipeline_dir)

    submission = dict(epxeriment_name=epxeriment_name,
                      cytokit_container_path=cytokit_container_path,
                      cytokit_data_dir=cytokit_data_dir,
                      mxif_dataset_dir_path=mxif_dataset_dir_path,
                      multichannel_ims_ometiff_positive_path=multichannel_ims_ometiff_positive_path,
                      multichannel_ims_ometiff_negative_path=multichannel_ims_ometiff_negative_path,
                      ngpus=ngpus,
                      best_focus_channel=best_focus_channel,
                      nuclei_channel=nuclei_channel,
                      membrane_channel=membrane_channel,
                      block_size=block_size,
                      overlap=overlap
                      )
    pipeline_config_path = osp.join(dir_paths['pipeline_output_dir'], 'pipeline_config.yaml')
    pipeline_output_dir = dir_paths['pipeline_output_dir']
    cytokit_container_path = cytokit_container_path
    cytokit_data_dir = cytokit_data_dir
    cytokit_output_dir = dir_paths['cytokit_output_dir']
    conda_init_path = osp.join(__location__, 'conda_init.sh')
    cytokit_config_path = osp.join(dir_paths['pipeline_output_dir'], 'cytokit_config.yaml')

    collect_meta.main(submission, base_pipeline_dir, pipeline_output_dir, pipeline_config_path,
                      cytokit_container_path, cytokit_output_dir, cytokit_data_dir, conda_init_path,
                      cytokit_config_path)

    generate_cytokit_config.main(pipeline_config_path, cytokit_config_path)

    shutil.copy(pipeline_config_path, '.')
    shutil.copy(cytokit_config_path, '.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--experiment_name', type=str, help='experiment name will be used for naming files and folders')
    parser.add_argument('--cytokit_container_path', type=str, help='path to cytokit container')
    parser.add_argument('--cytokit_data_dir', type=str, help='path to cytokit data dir')
    parser.add_argument('--mxif_dataset_dir_path', type=str,
                        help='path to directory with MxIF datasets. Contains two directories: processedMicroscopy, rawMicroscopy')
    parser.add_argument('--multichannel_ims_ometiff_positive_path', type=str,
                        help='path positive multichannel IMS OME-TIFF')
    parser.add_argument('--multichannel_ims_ometiff_negative_path', type=str,
                        help='path negative multichannel IMS OME-TIFF')
    parser.add_argument('--ngpus', type=int, help='number of gpus to use')
    parser.add_argument('--best_focus_channel', type=str,
                        help='If data has multiple z-planes, specify channel to use for detecting best focused plane')
    parser.add_argument('--nuclei_channel', type=str, help='Channel that will be used for nucleus segmentation')
    parser.add_argument('--membrane_channel', type=str, help='Channel that will be used for cell membrane segmentation')
    parser.add_argument('--block_size', type=int, help='size of one tile for image segmentation')
    parser.add_argument('--overlap', type=str, help='ize of overlap for one edge (each image has 4 overlapping edges)')
    args = parser.parse_args()

    main(args.experiment_name, args.cytokit_container_path, args.cytokit_data_dir, args.mxif_dataset_dir_path,
         args.multichannel_ims_ometiff_positive_path, args.multichannel_ims_ometiff_negative_path,
         args.ngpus, args.best_focus_channel, args.nuclei_channel, args.membrane_channel, args.block_size, args.overlap)
