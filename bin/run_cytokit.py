import os
import os.path as osp
import argparse
import subprocess
import shutil

import yaml


def read_from_pipeline_config(pipeline_config):
    with open(pipeline_config, 'r') as s:
        config = yaml.safe_load(s)

    meta = config['pipeline_meta']
    return meta


def main(pipeline_config: str, cytokit_config: str, slicer_out_dir: str):
    meta = read_from_pipeline_config(pipeline_config)
    if not osp.exists('cytokit_output'):
        os.makedirs('cytokit_output')
    shutil.copy(cytokit_config, '.')

    quote = ''' " '''
    conda_init = '''__conda_setup=\"$(\'/opt/conda/bin/conda\' \'shell.bash\' \'hook\' 2> /dev/null)\"; if [ $? -eq 0 ]; then eval \"$__conda_setup\"; else if [ -f \"/opt/conda/etc/profile.d/conda.sh\" ]; then . "/opt/conda/etc/profile.d/conda.sh\"; else export PATH=\"/opt/conda/bin:$PATH\"; fi fi; unset __conda_setup; export PYTHONPATH=/lab/repos/cytokit/python/pipeline '''
    conda_activate = ''' && conda activate cytokit '''
    run_cytokit = ''' && cytokit processor run_all '''
    run_param = ''' --data-dir {input_dir} --config-path {cytokit_config_path} --output-dir {output_dir} '''
    run_param.format(input_dir=slicer_out_dir, output_dir='cytokit_output', cytokit_config_path='cytokit_config.yaml')
    cytokit_run_cmd = quote + conda_init + conda_activate + run_cytokit + run_param + quote

    res = subprocess.run(cytokit_run_cmd, shell=True, check=True)

    """
    res.returncode
    res.stdout
    res.stderr
    """


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pipeline_config', type=str, help='path to pipeline config')
    parser.add_argument('--cytokit_config', type=str, help='path to cytokit config')
    parser.add_argument('--slicer_out_dir', type=str, help='path to slicer output')
    # parser.add_argument('--img_dir', type=str, help="path to directory with image tiles")
    # parser.add_argument('--output_dir', type=str, help="path to directory where output will be stored")
    # parser.add_argument('--cytokit_data_dir', type=str, help="path to directory where cytokit stores runtime data")
    # parser.add_argument('--cytokit_container_path', type=str, help="path to cytokit container")
    # parser.add_argument('--conda_init_path', type=str, help="path to conda parameters file")
    # parser.add_argument('--cytokit_config_path', type=str, help="path to cytokit config file (experiment.yaml)")
    args = parser.parse_args()

    main(args.pipeline_config, args.cytokit_config, args.slicer_out_dir)
