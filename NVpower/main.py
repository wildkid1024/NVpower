# encoding=utf8
import os
import argparse

from .energy_measure import run_energy_mj

def parse_args():
    parser = argparse.ArgumentParser(description='The tool for NVIDIA power measure')
    parser.add_argument('-j', '--job', default=None, type=str, help='The executable process')
    parser.add_argument('-d', '--gpu_id', default=0, type=int, help='The device id which is monitored')
    parser.add_argument('-i', '--interval', default=1000, type=float, help='The sampling interval(ms) when sampling gpu status')
    parser.add_argument('-o', '--outfile', default='', type=str, help='The results output file path')
    parser.add_argument('-t', '--threshold_power', default=0, type=int, help='The static threshold power')
    return parser.parse_args()


def main():
    args = parse_args()

    print("start sampling...")
    @run_energy_mj(args.gpu_id, args.interval, args.threshold_power)
    def run_job():
        os.system(args.job)

    run_job()
    print("end sampling...")

if __name__ == "__main__":
    main()
