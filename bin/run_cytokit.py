import os
import os.path as osp
import argparse
import subprocess

import yaml


def read_from_pipeline_config(pipeline_config):
    with open(pipeline_config, 'r') as s:
        config = yaml.safe_load(s)

    meta = config['pipeline_meta']
    return meta


def main(pipeline_config):
    meta = read_from_pipeline_config(pipeline_config)

    cytokit_run_cmd = ('singularity exec --nv ' +
                       '-B {cytokit_data_dir}:/lab/data/ ' +
                       '-B {input_dir}:/lab/slices/ ' +
                       '-B {output_dir}:/lab/output/ ' +
                       '{cytokit_container_path} ' +
                       'bash -c ' +
                       '"source {conda_init_path} && ' +
                       'conda activate cytokit && ' +
                       'cytokit processor run_all ' +
                       '--data-dir /lab/slices/ --config-path {cytokit_config_path} --output-dir /lab/output/" ')

    run_cytokit = cytokit_run_cmd.format(cytokit_data_dir=meta['cytokit_data_dir'],
                                         input_dir=meta['slicer_out_path'],
                                         output_dir=meta['cytokit_out_dir'],
                                         cytokit_container_path=meta['cytokit_container_path'],
                                         conda_init_path=meta['conda_init_path'],
                                         cytokit_config_path=meta['cytokit_config_path'])

    res = subprocess.run(run_cytokit, shell=True, check=True)

    """
    res.returncode
    res.stdout
    res.stderr
    """
    with open(osp.join(os.getcwd(), 'cytokit_out_dir.yaml'), 'w') as s:
        yaml.safe_dump({'cytokit_out_dir': meta['cytokit_out_dir']}, stream=s, default_flow_style=False, indent=4, sort_keys=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pipeline_config', type=str, help='path to pipeline config')
    parser.add_argument('--slicer_out_path', type=str, help='path to slicer output')
    # parser.add_argument('--img_dir', type=str, help="path to directory with image tiles")
    # parser.add_argument('--output_dir', type=str, help="path to directory where output will be stored")
    # parser.add_argument('--cytokit_data_dir', type=str, help="path to directory where cytokit stores runtime data")
    # parser.add_argument('--cytokit_container_path', type=str, help="path to cytokit container")
    # parser.add_argument('--conda_init_path', type=str, help="path to conda parameters file")
    # parser.add_argument('--cytokit_config_path', type=str, help="path to cytokit config file (experiment.yaml)")
    args = parser.parse_args()

    main(args.pipeline_config)
