from argparse import ArgumentParser
from os import mkdir, path, remove
from zipfile import ZipFile

from pandas import read_csv

from angle_converter import parse_dms
from utils import to_kml


def clean_gps_row(content: str) -> str:
    content = content.lstrip().rstrip()
    content = content.replace(" ", "")
    content = content.replace("N", "N;")
    content = content.replace("S", "S;")
    return content


if __name__ == "__main__":
    # python -m main -c coordenadas.csv
    parser = ArgumentParser()
    parser.add_argument("--csv", '-c', required=True)
    parser.add_argument("--output", '-o', choices=["kml", "kmz"], default="kmz")
    parser.add_argument("--folder", '-f', default="data")
    args = parser.parse_args()

    if not path.exists(args.folder):
        mkdir(args.folder)

    for index, row in read_csv(args.csv).iterrows():
        name, gps = row["ID"], clean_gps_row(row["gps"])

        lat, lon = gps.split(";")
        kml_content = to_kml(
            name,
            str(parse_dms(lat)),
            str(parse_dms(lon))
        )

        f = open(f"{args.folder}/{name}.kml", "w")
        f.write(kml_content)
        f.close()

        if args.output == "kml":
            continue

        with ZipFile(f"{args.folder}/{name}.kmz", "w") as myzip:
            myzip.write(f"{args.folder}/{name}.kml")
        remove(f"{args.folder}/{name}.kml")
