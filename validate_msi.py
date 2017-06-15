import contextlib

import collections.abc
import msilib
import argparse
import os

import sys

MSI_FILE = "C:/Users/hborcher/PycharmProjects/helloFreeze/dist/helloFreeze-0.0.2-amd64.msi"


class Query(contextlib.AbstractContextManager, collections.abc.Collection):
    def __init__(self, file_name, item="File"):
        self.data = msilib.OpenDatabase(file_name, msilib.MSIDBOPEN_READONLY)
        self._item = item

        pass

    def __enter__(self):
        self.view = self.data.OpenView("SELECT * FROM {}".format(self._item))
        self.view.Execute(None)
        self.fields = self.get_field_names(self.view)
        self.records = dict()

        while True:
            my_info = dict()
            try:

                record = self.view.Fetch()
            except msilib.MSIError as e:
                break
            for i in range(record.GetFieldCount()):
                field_id = i + 1
                field_name = record.GetString(field_id)
                if i == 0:
                    key = field_name
                my_info[self.fields[field_id]] = field_name
            self.records[key] = my_info
        return self

    @staticmethod
    def get_field_names(view):
        fields = view.GetColumnInfo(msilib.MSICOLINFO_NAMES)
        field_lookeup = dict()
        for i in range(0, fields.GetFieldCount()):
            field_id = i + 1
            field_lookeup[field_id] = fields.GetString(field_id)
        return field_lookeup

    def __exit__(self, exc_type, exc_value, traceback):
        self.view.Close()

    def __contains__(self, x):
        return self.records.__contains__(x)

    def __iter__(self):
        for record in self.records.items():
            yield record

    def __len__(self):
        return len(self.records)


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("msi", help="path to the MSI file")
    parser.add_argument("requirement_file", help="path to a file contains a lists the required file names")
    return parser


def get_requirements(file_name):
    with open(file_name, "r") as f:
        for line in f:
            required_file = line.strip()
            if required_file:
                yield required_file
    pass


def main():
    parser = get_parser()
    args = parser.parse_args()
    print("Checking {} for files listed in {}".format(args.msi, args.requirement_file))
    print()

    requirements = get_requirements(args.requirement_file)
    missing_files = []


    with Query(args.msi) as files_in_msi:
        for required_file in requirements:
            if required_file in files_in_msi:
                print("{:<20} Found".format(required_file))
            else:
                print("{:<20} Missing".format(required_file))
                missing_files.append(required_file)

    print()
    if missing_files:
        print("Unable to find \"{}\".".format("\", \"".join(missing_files)), file=sys.stderr, flush=True)
        print("Validation: FAILED!")
        sys.exit(1)

    else:
        print("Validation: PASSED!")


if __name__ == '__main__':
    # main()
    main()
