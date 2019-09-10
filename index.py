import sys
from start import *


def create_index(path_to_data_dump, path_to_index_folder):
    index_wrapper(path_to_data_dump, path_to_index_folder)


def main():
    path_to_data_dump = sys.argv[1]
    path_to_index_folder = sys.argv[2]

    create_index(path_to_data_dump, path_to_index_folder)


if __name__ == '__main__':
    main()
