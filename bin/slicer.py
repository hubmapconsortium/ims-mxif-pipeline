import copy
import os
import os.path as osp
import argparse
from string import Template

import yaml
import json
import numpy as np
import tifffile as tif
import dask


def split_by_size(arr: np.ndarray, region: int, zplane: int, channel: int, block_w: int, block_h: int, overlap: int):
    """ Splits image into blocks by size of block.
        block_w - block width
        block_h - block height
    """
    img_width, img_height = arr.shape[-1], arr.shape[-2]
    x_axis = -1
    y_axis = -2
    arr_shape = list(arr.shape)
    dtype = arr.dtype

    x_nblocks = arr_shape[x_axis] // block_w if arr_shape[x_axis] % block_w == 0 else (arr_shape[x_axis] // block_w) + 1
    y_nblocks = arr_shape[y_axis] // block_h if arr_shape[y_axis] % block_h == 0 else (arr_shape[y_axis] // block_h) + 1

    # check if image size is divisible by block size
    pad_shape = copy.copy(arr_shape)
    if img_height % block_h != 0:
        do_horizontal_padding = True
    else:
        do_horizontal_padding = False

    if img_width % block_w != 0:
        do_vertical_padding = True
    else:
        do_vertical_padding = False

    blocks = []
    img_names = []

    # row
    for i in range(0, y_nblocks):
        # height of this block
        ver_f = block_h * i
        ver_t = ver_f + block_h

        if overlap != 0:
            # vertical overlap of this block
            if i == 0:
                ver_t += overlap
            elif i == y_nblocks - 1:
                ver_f -= overlap
                ver_t = img_height
            else:
                ver_f -= overlap
                ver_t += overlap

        # col
        for j in range(0, x_nblocks):
            name = '{region:d}_{tile:05d}_Z{zplane:03d}_CH{channel:d}.tif'.format(region=region,
                                                                                  tile=(i * x_nblocks) + (j + 1),
                                                                                  zplane=zplane + 1,
                                                                                  channel=channel + 1)

            # width of this block
            hor_f = block_w * j
            hor_t = hor_f + block_w

            if overlap != 0:
                # horizontal overlap of this block
                if j == 0:
                    hor_t += overlap
                elif j == x_nblocks - 1:
                    hor_f -= overlap
                    hor_t = img_width
                else:
                    hor_f -= overlap
                    hor_t += overlap

            block = arr[ver_f: ver_t, hor_f: hor_t]

            # handling cases when image size is not divisible by block size
            if j == x_nblocks - 1 and do_horizontal_padding:
                pad_shape = list(block.shape)
                rest = img_width % block_w
                pad_shape[x_axis] = block_w - rest
                pad_shape[y_axis] = block.shape[y_axis]  # width of padding
                block = np.concatenate((block, np.zeros(pad_shape, dtype=dtype)), axis=x_axis)

            if i == y_nblocks - 1 and do_vertical_padding:
                pad_shape = list(block.shape)
                rest = img_height % block_h
                pad_shape[x_axis] = block.shape[x_axis]
                pad_shape[y_axis] = block_h - rest  # height of padding
                block = np.concatenate((block, np.zeros(pad_shape, dtype=dtype)), axis=y_axis)

            # handling cases when of overlap on the edge images
            if overlap != 0:
                overlap_pad_shape = list(block.shape)
                if i == 0:
                    overlap_pad_shape[x_axis] = block.shape[x_axis]
                    overlap_pad_shape[y_axis] = overlap
                    block = np.concatenate((np.zeros(overlap_pad_shape, dtype=dtype), block), axis=0)
                    # print('i0', block.shape)
                elif i == y_nblocks - 1:
                    overlap_pad_shape[x_axis] = block.shape[x_axis]
                    overlap_pad_shape[y_axis] = overlap
                    block = np.concatenate((block, np.zeros(overlap_pad_shape, dtype=dtype)), axis=0)
                    # print('i-1', block.shape)
                if j == 0:
                    overlap_pad_shape[x_axis] = overlap
                    overlap_pad_shape[y_axis] = block.shape[y_axis]
                    block = np.concatenate((np.zeros(overlap_pad_shape, dtype=dtype), block), axis=1)
                    # print('j0', block.shape)
                elif j == x_nblocks - 1:
                    overlap_pad_shape[x_axis] = overlap
                    overlap_pad_shape[y_axis] = block.shape[y_axis]
                    block = np.concatenate((block, np.zeros(overlap_pad_shape, dtype=dtype)), axis=1)
                    # print('j-1', block.shape)
            # print('\n')
            blocks.append(block)
            img_names.append(name)

    return blocks, img_names


def split_by_nblocks(arr: np.ndarray, region: int, zplane: int, channel: int, x_nblocks: int, y_nblocks: int,
                     overlap: int):
    """ Splits image into blocks by number of block.
        x_nblocks - number of blocks horizontally
        y_nblocks - number of blocks vertically
    """
    img_width, img_height = arr.shape[-1], arr.shape[-2]
    block_w = img_width // x_nblocks
    block_h = img_height // y_nblocks
    return split_by_size(arr, region, zplane, channel, block_w, block_h, overlap)


def split_tiff(in_path: str, out_dir: str, block_size: int, nblocks: int, overlap: int,
               cycle: int, region: int, nzplanes: int, nchannels: int):
    with tif.TiffFile(in_path) as TF:
        npages = len(TF.pages)
        plane_shape = TF.series[0].shape
        try:
            meta = TF.ome_metadata
        except AttributeError:
            meta = None

    # split image by number of blocks
    if nblocks == 0:
        p = 0
        for c in range(0, nchannels):
            for z in range(0, nzplanes):
                print('page', p + 1, '/', npages)
                this_plane_split, this_plane_img_names = split_by_size(
                    tif.imread(in_path, key=p), region, zplane=z, channel=c, block_w=block_size, block_h=block_size,
                    overlap=overlap
                )
                task = []
                for i, img in enumerate(this_plane_split):
                    task.append(dask.delayed(tif.imwrite)(osp.join(out_dir, this_plane_img_names[i]), img,
                                                          photometric='minisblack'))

                dask.compute(*task, scheduler='threads')
                p += 1

        x_nblocks = plane_shape[-1] // block_size if plane_shape[-1] % block_size == 0 else (plane_shape[
                                                                                                 -1] // block_size) + 1
        y_nblocks = plane_shape[-2] // block_size if plane_shape[-2] % block_size == 0 else (plane_shape[
                                                                                                 -2] // block_size) + 1

    # split image by block size
    elif block_size == 0:
        p = 0
        for c in range(0, nchannels):
            for z in range(0, nzplanes):
                print('page', p + 1, '/', npages)
                this_plane_split, this_plane_img_names = split_by_nblocks(
                    tif.imread(in_path, key=p), region, zplane=0, channel=c, x_nblocks=nblocks, y_nblocks=nblocks,
                    overlap=overlap
                )
                task = []
                for i, img in enumerate(this_plane_split):
                    task.append(dask.delayed(tif.imwrite)(osp.join(out_dir, this_plane_img_names[i]), img,
                                                          photometric='minisblack'))
                dask.compute(*task, scheduler='threads')
                p += 1
        x_nblocks = nblocks
        y_nblocks = nblocks

    block_shape = this_plane_split[0].shape
    block_shape_no_overlap = (block_shape[-2] - overlap * 2, block_shape[-1] - overlap * 2)

    nblocks_info = dict(x=x_nblocks, y=y_nblocks)
    block_shape_info = dict(x=block_shape[-1], y=block_shape[-2])
    block_shape_no_overlap_info = dict(x=block_shape_no_overlap[-1], y=block_shape_no_overlap[-2])
    original_img_shape_info = dict(x=plane_shape[-1], y=plane_shape[-2])
    new_image_shape_info = dict(x=block_shape[-1] * x_nblocks, y=block_shape[-2] * y_nblocks)
    overlap_info = dict(x=overlap * 2, y=overlap * 2)

    padding = dict(left=0, right=0, top=0, bottom=0)
    padding["right"] = block_shape_no_overlap[-1] - (plane_shape[-1] % block_shape_no_overlap[-1])
    padding["bottom"] = block_shape_no_overlap[-2] - (plane_shape[-2] % block_shape_no_overlap[-2])
    img_name = osp.basename(in_path)

    slicer_description = {'image_name': img_name,
                          'original_image_shape': original_img_shape_info,
                          'new_image_shape': new_image_shape_info,
                          'block_shape': block_shape_info,
                          'block_shape_no_overlap': block_shape_no_overlap_info,
                          'nblocks': nblocks_info,
                          'overlap': overlap_info,
                          'padding': padding,
                          'tiling_mode': 'grid',
                          'cycle': cycle,
                          'region': region
                          }

    if meta is not None:
        with open(osp.join(out_dir, 'ome_meta.xml'), 'w') as f:
            f.write(meta)

    print(yaml.dump(slicer_description, default_flow_style=False, indent=4, sort_keys=False))

    with open(osp.join(out_dir, 'description.yaml'), 'w') as s:
        yaml.safe_dump(slicer_description, stream=s, default_flow_style=False, indent=4, sort_keys=False)


def main(i: str = None, o: str = None, s: int = None, n: int = None, v: int = None,
         c: int = None, r: int = None, nz: int = None, nc: int = None):
    in_path = i
    out_dir = o
    nblocks = n
    block_size = s
    overlap = v
    cycle = c
    region = r
    nzplanes = nz
    nchannels = nc
    # Cyc{cycle:d}_reg{region:d}/{region:d}_{tile:05d}_Z{z:03d}_CH{channel:d}.tif
    out_dir = osp.join(out_dir, 'Cyc{cycle}_reg{region}'.format(cycle=cycle, region=region))
    if not in_path.endswith(('tif', 'tiff')):
        raise ValueError('Only tif, tiff input files are accepted')

    if not osp.exists(out_dir):
        os.makedirs(out_dir)

    if nblocks != 0 and block_size != 0:
        raise ValueError('One of the parameters -s or -n must be zero')

    if nblocks == 0 and block_size == 0:
        raise ValueError('One of the parameters -s or -n must be non zero')

    split_tiff(in_path, out_dir, block_size, nblocks, overlap, cycle, region, nzplanes, nchannels)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Split image into number of blocks')
    parser.add_argument('-i', type=str, help='path to image file')
    parser.add_argument('-o', type=str, help='path to output dir')
    parser.add_argument('-s', type=int, default=1000,
                        help='size of block, default 1000x1000, if set to 0, then -n parameter used instead')
    parser.add_argument('-n', type=int, default=0,
                        help='number of blocks, default 0, if set to 0, then -s parameter used instead')
    parser.add_argument('-v', type=int, default=0, help='size of overlap, default 0 (no overlap)')
    parser.add_argument('--cycle', type=int, default=1, help='cycle number, default 1')
    parser.add_argument('--region', type=int, default=1, help='region number, default 1')
    parser.add_argument('--nzplanes', type=int, default=1, help='number of z-planes, default 1')
    parser.add_argument('--nchannels', type=int, default=1, help='number of channels, default 1')

    args = parser.parse_args()
    main(i=args.i, o=args.o, s=args.s, n=args.n, v=args.v, c=args.cycle, r=args.region, nz=args.nzplanes,
         nc=args.nchannels)

