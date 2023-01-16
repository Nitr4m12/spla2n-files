from csv import DictReader, DictWriter
from sys import argv

from common.util import config

VERSION = config.get_default_version()
DATA_PATH = config.get_versioned_data_path(VERSION)

def get_csv_rows(file: str) -> list:
    rows: list = []
    with open(file, "r") as csvfile:
        reader = DictReader(csvfile)
        for row in reader:
            rows.append(row)

    return rows

def write_csv_rows(file: str, rows: list) -> None:
    with open(file, "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

def calculate_func_size(addr1: int, addr2: int) -> int:
    return int(addr2, 16) - int(addr1, 16)

def main() -> None:
    funcs: list = get_csv_rows(argv[1])
    funcs2: list = []
    data_syms: list = []

    for i in range(len(funcs)-1):
        if funcs[i]["Type"] == "Function":
            funcs2.append(
                {"Address": f"0x000000{funcs[i]['Address']}",
                "Quality": "U",
                "Size": calculate_func_size(funcs[i]["Address"], funcs[i+1]["Address"]),
                "Name": funcs[i]["Name"],})

        if funcs[i]["Type"] == "Data Label":
            data_syms.append({
                "Address": f"0x000000{funcs[i]['Address']}",
                "Name": funcs[i]["Name"],
            })

    write_csv_rows(DATA_PATH / "blitz_functions.csv", funcs2)
    write_csv_rows(DATA_PATH / "data_symbols.csv", data_syms)


if __name__ == "__main__":
    main()


