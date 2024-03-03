#!/usr/bin/env python3

import argparse
import matplotlib.pyplot as plt
import polars as pl

parser = argparse.ArgumentParser(
    description="Visualize the Chronobox timestamps for a single run.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument("infile", help="path to the Chronobox timestamps CSV file")
parser.add_argument("board_name", help="board name (e.g. 'cb01')")
parser.add_argument("channel_number", type=int, help="channel number")
parser.add_argument("--t-bins", type=int, default=100, help="number of bins along t")
parser.add_argument(
    "--t-max", type=float, default=float("inf"), help="maximum time in seconds"
)
parser.add_argument("--t-min", type=float, default=0.0, help="minimum time in seconds")
args = parser.parse_args()

df = pl.read_csv(args.infile, comment_prefix="#").filter(
    pl.col("board") == args.board_name,
    pl.col("channel") == args.channel_number,
    pl.col("chronobox_time").is_between(args.t_min, args.t_max),
    pl.col("leading_edge"),
)

plt.hist(df["chronobox_time"], bins=args.t_bins)

plt.xlabel("Chronobox time [s]")
plt.ylabel("Counts")

plt.show()