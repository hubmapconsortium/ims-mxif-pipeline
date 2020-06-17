import argparse
import xml.etree.ElementTree as ET
from io import StringIO
import copy

import yaml
import tifffile as tif


def read_ome_meta(path: str):
    with tif.TiffFile(path) as TF:
        # ims_shape = TF.series[0].shape
        ims_ome_meta = TF.ome_metadata

    return ims_ome_meta


def strip_namespace(xmlstr: str):
    it = ET.iterparse(StringIO(xmlstr))
    for _, el in it:
        _, _, el.tag = el.tag.rpartition('}')
    root = it.root
    return root


def get_all_channels_and_tiffdata(xml):
    pixels = xml.find('Image').find('Pixels')
    nchannels = int(pixels.get('SizeC'))
    channels = pixels.findall('Channel')
    tiffdata = pixels.findall('TiffData')
    return nchannels, channels, tiffdata


def get_necessary_meta(path):
    ome_meta = read_ome_meta(path)
    xml = strip_namespace(ome_meta)
    nchannels, channels, tiffdata = get_all_channels_and_tiffdata(xml)
    meta = {'nchannels': nchannels, 'channels': channels, 'tiffdata': tiffdata}
    return meta


def main(mxif_data_paths: list, mxif_combined_out_path: str):

    combined_xml = strip_namespace(read_ome_meta(mxif_data_paths[0]))

    for child in combined_xml.find('Image').find('Pixels').getchildren():
        combined_xml.find('Image').find('Pixels').remove(child)

    combined_meta = []
    prev_num_ch = 0
    for path in mxif_data_paths:
        meta = get_necessary_meta(path)
        for i in range(0, meta['nchannels']):
            new_id = str(prev_num_ch + i)
            meta['channels'][i].set('ID', 'Channel:0:' + new_id)
            # meta['tiffdata'][i].set('FisrtC', new_id)
            # meta['tiffdata'][i].set('IFD', new_id)
        combined_meta.append(meta)
        prev_num_ch += meta['nchannels']

    total_channels = str(prev_num_ch)
    combined_xml.find('Image').find('Pixels').set('SizeC', total_channels)

    for dataset in combined_meta:
        for c in dataset['channels']:
            combined_xml.find('Image').find('Pixels').append(c)
    #
    # for dataset in combined_meta:
    #     for t in dataset['tiffdata']:
    #         combined_xml.find('Image').find('Pixels').append(t)

    # these attributes contain symbol that is cannot be encoded with ascii. ascii encoding required by tifffile
    pixel_attribs = combined_xml.find('Image').find('Pixels').attrib
    if 'PhysicalSizeXUnit' in pixel_attribs:
        del combined_xml.find('Image').find('Pixels').attrib['PhysicalSizeXUnit']
    if 'PhysicalSizeYUnit' in pixel_attribs:
        del combined_xml.find('Image').find('Pixels').attrib['PhysicalSizeYUnit']

    combined_xml_str = ET.tostring(combined_xml, method='xml', encoding='utf-8')
    xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>'
    description = combined_xml_str.decode('ascii', errors='backslashreplace')
    description = xml_declaration + description

    with tif.TiffWriter(mxif_combined_out_path, bigtiff=True) as TW:
        for dataset in range(0, len(mxif_data_paths)):
            npages = combined_meta[dataset]['nchannels']
            for page in range(0, npages):
                TW.save(tif.imread(mxif_data_paths[dataset], key=page),
                        photometric='minisblack', description=description)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mxif_data_paths', type=str, nargs='+',
                        help='spcae separated list of paths to MxIF OME-TIFF')
    parser.add_argument('--mxif_combined_out_path', type=str,
                        help='path to output combined MxIF images')
    args = parser.parse_args()

    main(args.mxif_data_paths, args.mxif_combined_out_path)
