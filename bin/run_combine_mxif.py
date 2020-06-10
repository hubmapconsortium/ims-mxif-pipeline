import argparse
import os
import os.path as osp
import yaml

import combine_mxif


def main(pipeline_config: str):
    with open(pipeline_config, 'r') as s:
        config = yaml.safe_load(s)

    pipeline_meta = config['pipeline_meta']
    mxif_data_paths = pipeline_meta['mxif_data_paths']
    mxif_combined_out_path = pipeline_meta['mxif_combined_out_path']

    if not osp.exists('pipeline_output'):
        os.makedirs('pipeline_output')

    combine_mxif.main(mxif_data_paths, mxif_combined_out_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pipeline_config', type=str, help='path to pipeline config')
    args = parser.parse_args()

    main(args.pipeline_config)
