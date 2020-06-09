import argparse
import shutil
import yaml

import combine_ims


def main(pipeline_config: str):
    with open(pipeline_config, 'r') as s:
        config = yaml.safe_load(s)

    submission = config['submission']
    pipeline_meta = config['pipeline_meta']
    ims_combined_path = submission['multichannel_ims_ometiff_combined_path']
    ims_pos_path = submission['multichannel_ims_ometiff_positive_path']
    ims_neg_path = submission['multichannel_ims_ometiff_negative_path']
    ims_combined_out_path = pipeline_meta['ims_combined_out_path']

    # Will run combine_ims.py if both positive and negative paths are provided
    # Otherwise will just copy file to output folder
    if ims_combined_path is not None:
        shutil.copy(ims_combined_path, ims_combined_out_path)
    elif ims_pos_path is not None and ims_neg_path is not None:
        combine_ims.main(ims_pos_path, ims_neg_path, ims_combined_out_path)

    # if one of path is None
    elif ims_pos_path is not None and ims_neg_path is None:
        shutil.copy(ims_pos_path, ims_combined_out_path)
    elif ims_pos_path is None and ims_neg_path is not None:
        shutil.copy(ims_neg_path, ims_combined_out_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pipeline_config', type=str, help='path to pipeline config')
    args = parser.parse_args()

    main(args.pipeline_config)
