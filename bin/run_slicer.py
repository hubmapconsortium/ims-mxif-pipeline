import os
import os.path as osp
import argparse

import yaml

import slicer


def main(pipeline_config: str):
    with open(pipeline_config, 'r') as s:
        config = yaml.safe_load(s)
    pipeline_meta = config['pipeline_meta']
    slicer_meta = config['slicer_meta']
    ome_meta = config['ome_meta']

    num_cycles = ome_meta['num_cycles']
    num_z_planes = ome_meta['num_z_planes']

    in_path = pipeline_meta['slicer_in_path']
    out_base_dir = pipeline_meta['slicer_out_path']

    block_shape = slicer_meta['block_shape_no_overlap']['x']
    overlap = slicer_meta['overlap']['x']

    slicer.main(i=in_path, o=out_base_dir, s=int(block_shape), n=0, v=int(overlap)//2, c=1, r=1,
                nz=int(num_z_planes), nc=int(num_cycles))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pipeline_config', type=str, help='path to pipeline config')
    # parser.add_argument('--img_dir', type=str, help='path to image directory')
    # parser.add_argument('--out_dir', type=str, help='path to output dir')

    args = parser.parse_args()
    main(args.pipeline_config)
