import copy
import os
import os.path as osp
import argparse

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
               region: int, nzplanes: int, nchannels: int, selected_channels: list):
    with tif.TiffFile(in_path) as TF:
        npages = len(TF.pages)

    # split image by number of blocks
    if nblocks == 0:
        for c in selected_channels:
            for z in range(0, nzplanes):
                page = c * nzplanes + z
                print('page', page + 1, '/', npages)
                this_plane_split, this_plane_img_names = split_by_size(
                    tif.imread(in_path, key=page), region, zplane=z, channel=c, block_w=block_size, block_h=block_size,
                    overlap=overlap
                )
                task = []
                for i, img in enumerate(this_plane_split):
                    task.append(dask.delayed(tif.imwrite)(osp.join(out_dir, this_plane_img_names[i]), img,
                                                          photometric='minisblack'))

                dask.compute(*task, scheduler='threads')

    # split image by block size
    elif block_size == 0:
        for c in selected_channels:
            for z in range(0, nzplanes):
                page = c * nzplanes + z
                print('page', page + 1, '/', npages)
                this_plane_split, this_plane_img_names = split_by_nblocks(
                    tif.imread(in_path, key=page), region, zplane=0, channel=c, x_nblocks=nblocks, y_nblocks=nblocks,
                    overlap=overlap
                )
                task = []
                for i, img in enumerate(this_plane_split):
                    task.append(dask.delayed(tif.imwrite)(osp.join(out_dir, this_plane_img_names[i]), img,
                                                          photometric='minisblack'))
                dask.compute(*task, scheduler='threads')


def main(in_path: str = None, out_dir: str = None, block_size: int = None, nblocks: int = None, overlap: int = None,
         cycle: int = None, region: int = None, nzplanes: int = None, nchannels: int = None, selected_channels: list = None):

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

    if selected_channels is None:
        selected_channels = list(range(0, nchannels))
    else:
        selected_channels = [ch_id for ch_id in selected_channels if ch_id < nchannels]

    split_tiff(in_path, out_dir, block_size, nblocks, overlap, region, nzplanes, nchannels, selected_channels)


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
    parser.add_argument('--selected_channels', type=int, nargs='+', default=None,
                        help="space separated ids of channels you want to slice, e.g. 0 1 3, default all")

    args = parser.parse_args()
    main(args.i, args.o, args.s, args.n, args.v, args.cycle, args.region,
         args.nzplanes, args.nchannels, args.selected_channels)
