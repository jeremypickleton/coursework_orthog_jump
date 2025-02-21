import csv
from block import Block, Spike, End, Ship


def load_level_from_csv(file_path):
    worldmap = []
    with open(file_path) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            worldmap.append(row)

    return worldmap


def write_to_csv(file_path, data):
    with open(file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data)


def get_last_attempt_num():
    with open("./assets/leaderboard.csv", mode="r") as file:
        reader = csv.reader(file)
        rows = list(reader)
        if rows:
            return rows[-1]
        return None


def generate_blocks_from_map(worldmap):
    rowno = 0
    while rowno < len(worldmap):
        colno = 0
        while colno < len(worldmap[rowno]):
            if worldmap[rowno][colno] == "#":
                Block(colno * 50, rowno * 50)
            if worldmap[rowno][colno] == "s":
                Spike(colno * 50, rowno * 50)
            if worldmap[rowno][colno] == "f":
                End(colno * 50, rowno * 50)
            if worldmap[rowno][colno] == "p":
                Ship(colno * 50, rowno * 50)
            colno += 1
        rowno += 1
