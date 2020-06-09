import argparse
import subprocess
import os
import os.path as osp


def main(i: str, o: str, m: str = ''):
    input_file = i
    output_file = o
    mapping = m
    __location__ = osp.realpath(osp.join(os.getcwd(), osp.dirname(__file__)))
    jar_path = osp.join(__location__, 'extract_meta.jar')

    command = 'java -jar {jar_path} {input_file} {output_file} {mapping}'.format(jar_path=jar_path,
                                                                                 input_file=input_file,
                                                                                 output_file=output_file,
                                                                                 mapping=mapping)
    subprocess.run(command, shell=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, help='path to input file')
    parser.add_argument('-o', type=str, help='path to output file')
    parser.add_argument('-m', type=str, default='', help='path to mapping yaml')
    args = parser.parse_args()

    main(args.i, args.o, args.m)
