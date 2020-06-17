import argparse
import shutil

import combine_ims


def main(ims_pos_path: str, ims_neg_path):
    ims_combined_out_path = 'ims_combined_multilayer.ome.tiff'

    # Will run combine_ims.py if both positive and negative paths are provided
    # Otherwise will just copy file to output folder
    if ims_pos_path is not None and ims_neg_path is not None:
        combine_ims.main(ims_pos_path, ims_neg_path, ims_combined_out_path)

    # if one of path is None
    elif ims_pos_path is not None and ims_neg_path is None:
        shutil.copy(ims_pos_path, ims_combined_out_path)
    elif ims_pos_path is None and ims_neg_path is not None:
        shutil.copy(ims_neg_path, ims_combined_out_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--multichannel_ims_ometiff_positive_path', type=str,
                        help='path positive multichannel IMS OME-TIFF')
    parser.add_argument('--multichannel_ims_ometiff_negative_path', type=str,
                        help='path negative multichannel IMS OME-TIFF')
    args = parser.parse_args()

    main(args.multichannel_ims_ometiff_positive_path, args.multichannel_ims_ometiff_negative_path)
