# encoding=utf8
import os
import argparse

from .energy_measure import run_energy_mj

def parse_args():
    parser = argparse.ArgumentParser(description='The tool for NVIDIA power measure')
    parser.add_argument('-j', '--job', default=None, type=str, help='the executable process')
    parser.add_argument('-d', '--gpu_id', default=0, type=int, help='The device id which is monitored')
    parser.add_argument('-i', '--interval', default=1, type=float, help='The sampling interval(ms) when sampling gpu status')
    return parser.parse_args()


def main():
    args = parse_args()

    print("start sampling...")
    @run_energy_mj(args.gpu_id, args.interval)
    def run_job():
        os.system(args.job)

    run_job()
    print("end sampling...")

if __name__ == "__main__":
    main()
