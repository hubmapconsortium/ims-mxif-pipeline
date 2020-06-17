import os
import os.path as osp
import argparse

import yaml

import slicer

from extract_from_names import extract_cycle_info_from_names


def main(pipeline_config: str, mxif_dataset_dir_path: str, block_size: int, overlap: int):
    with open(pipeline_config, 'r') as s:
        config = yaml.safe_load(s)

    ome_meta = config['ome_meta']
    num_cycles = ome_meta['num_cycles']
    num_z_planes = ome_meta['num_z_planes']

    per_cycle_info = extract_cycle_info_from_names(mxif_dataset_dir_path)
    cycle = min(list(per_cycle_info.keys()))
    region = min(list(per_cycle_info[cycle].keys()))

    in_path = per_cycle_info[cycle][region]['proc_path']
    output_dir = 'tiles'

    if not osp.exists(output_dir):
        os.makedirs(output_dir)

    slicer.main(in_path, output_dir, block_size, 0, overlap, cycle, region,
                int(num_z_planes), int(num_cycles))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pipeline_config', type=str, help='path to pipeline config')
    parser.add_argument('--mxif_dataset_dir_path', type=str,
                        help='path to directory with MxIF datasets. Contains two directories: processedMicroscopy, rawMicroscopy')
    parser.add_argument('--block_size', type=int, help='size of one tile for image segmentation')
    parser.add_argument('--overlap', type=int, help='size of overlap for one edge (each image has 4 overlapping edges)')
    # parser.add_argument('--img_dir', type=str, help='path to image directory')
    # parser.add_argument('--out_dir', type=str, help='path to output dir')

    args = parser.parse_args()
    main(args.pipeline_config, args.mxif_dataset_dir_path, args.block_size, args.overlap)
