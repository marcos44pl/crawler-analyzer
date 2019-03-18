import argparse
import enum

page = "https://www.uclm.es/"
project = "UCLM"

class Args(enum.Enum):
    HomePage = "home_page"
    ProjectName = "name"
    SaveFlag = "save"


def parse(desc, def_page=page, def_name=project):
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("--home_page", default=def_page, help="start page for crawler")
    parser.add_argument("--name", default=def_name, help="Name of folder where crawler/ graph will work")
    parser.add_argument("--save", action='store_true', help="Boolean, wheter save crawling documents or not")
    args = parser.parse_args()
    return args.__dict__
