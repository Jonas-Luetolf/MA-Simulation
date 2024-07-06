from pathlib import Path
import os
import sys

import numpy as np
import pandas as pd


def load_csv(path: Path) -> tuple[np.ndarray, np.ndarray]:
    data = pd.read_csv(path, sep=",")

    X = np.array(data.drop(columns=["collision", "start_x", "start_y", "v_x", "v_y"]))
    X = X.reshape((len(X), 1, 270))

    Y = np.array(data["collision"])
    Y = Y.reshape(len(Y), 1, 1)

    return X, Y


def load_and_clean_data(
    path: Path, false_ratio=0.5, start_row=1, nrows=100_000
) -> pd.DataFrame:

    data = pd.read_csv(path, sep=",", skiprows=list(range(1, start_row)), nrows=nrows)
    data = data.sort_values("collision", ascending=False)

    num_true = data["collision"].value_counts()[True]
    num_false = int(num_true / (1 - false_ratio) - num_true)

    if num_true + num_false > len(data):
        return data

    new_len = num_true + num_false

    if not isinstance(data, pd.DataFrame):
        raise TypeError(f"loaded data must be DataFrame got {type(data)}")

    data: pd.DataFrame = data[0:new_len]

    return data


def split_data(data: pd.DataFrame, num_train: int, num_test: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    data = data.sample(frac=1, random_state=42).reset_index(drop=True)

    assert num_train + num_test < len(data)

    train = data.iloc[:num_train]
    test = data.iloc[num_train:(num_train+num_test)]

    return train, test


def clean(input_path: Path, train_path: Path, test_path: Path, n_train: int, n_test: int, len: int=500_000, itersize: int = 100_000):
    assert len % itersize == 0

    for n in range(len // itersize):
        clean_data = load_and_clean_data(input_path, start_row=n * itersize)

        train, test = split_data(clean_data, n_train, n_test)

        train.to_csv(
            train_path, index=False, header=not os.path.exists(train_path), mode="a"
        )
        test.to_csv(
            test_path, index=False, header=not os.path.exists(test_path), mode="a"
        )

        print(f"processed {n * itersize} rows")


def check_args(args: list) -> bool:
    for i in args[1:4]:
        if not os.path.isfile(i):
            print(i)
            return False

    for i in args[4:]:
        if not i.isdigit:
            return False

    return True


def parse_args(args: list) -> list:
    ret = []
    ret += list(map(Path, args[1:4]))
    ret += list(map(int, args[4:]))

    return ret


def main(args: list):
    if len(args) == 8 and check_args(args):
        clean(*parse_args(args))

    else:
        print(len(args))
        print("invalid args")


if __name__ == "__main__":
    main(sys.argv)
