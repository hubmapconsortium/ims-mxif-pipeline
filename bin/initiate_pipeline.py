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


def main(path_to_submission_file: str, path_to_external_output_directory: str):
    __location__ = osp.realpath(osp.join(os.getcwd(), osp.dirname(__file__)))

    with open(path_to_submission_file, 'r') as f:
        submission = yaml.safe_load(f)

    base_pipeline_dir = '.'

    dir_paths = create_base_dirs(base_pipeline_dir)
    pipeline_config_path = osp.join(dir_paths['pipeline_output_dir'], 'pipeline_config.yaml')
    pipeline_output_dir = dir_paths['pipeline_output_dir']
    cytokit_container_path = submission['cytokit_container_path']
    cytokit_data_dir = submission['cytokit_data_dir']
    cytokit_output_dir = dir_paths['cytokit_output_dir']
    conda_init_path = osp.join(__location__, 'conda_init.sh')
    cytokit_config_path = osp.join(dir_paths['pipeline_output_dir'], 'cytokit_config.yaml')

    collect_meta.main(path_to_submission_file, base_pipeline_dir, pipeline_output_dir, pipeline_config_path,
                      cytokit_container_path, cytokit_output_dir, cytokit_data_dir, conda_init_path, cytokit_config_path,
                      path_to_external_output_directory)

    generate_cytokit_config.main(pipeline_config_path, cytokit_config_path)

    shutil.copy(pipeline_config_path, '.')
    shutil.copy(cytokit_config_path, '.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_to_submission_file', type=str, help='path to submission file')
    parser.add_argument('--path_to_external_output_directory', type=str, help='path_to_external_output_directory')

    args = parser.parse_args()
    main(args.path_to_submission_file, args.path_to_external_output_directory)
