import argparse

import yaml

import stitcher


def main(pipeline_config: str):
    with open(pipeline_config, 'r') as s:
        config = yaml.safe_load(s)
    slicer_meta = config['slicer_meta']
    pipeline_meta = config['pipeline_meta']

    overlap = int(slicer_meta['overlap']['x'] // 2)
    padding = ','.join(list(slicer_meta['padding'].values()))
    cytokit_out_dir = pipeline_meta['cytokit_out_dir']
    stitcher_out_path = pipeline_meta['stitcher_out_path']
    stitcher.main(cytokit_out_dir, stitcher_out_path, overlap, padding)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pipeline_config', type=str, help='path to pipeline config')
    parser.add_argument('--cytokit_out_dir', type=str, help='path to cytokit output mask')
    args = parser.parse_args()

    main(args.pipeline_config)
