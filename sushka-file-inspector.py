import enum
import re

import click
from typing import List, Optional
from pathlib import Path

class FileType(enum.Enum):
    MASTER = "master"
    ACCESS = "access"

def file_type_to_str(file_type: FileType) -> Optional[str]:
    if file_type == FileType.MASTER:
        return "master"
    elif file_type == FileType.ACCESS:
        return "access"
    else:
        return None

def str_to_file_type(file_str: str) -> Optional[FileType]:
    if file_str == "master":
        return FileType.MASTER
    elif file_str == "access":
        return FileType.ACCESS
    else:
        return None

def process_master(path: str, extension: str, files: List[str]) -> None:
    pattern = "(.*)ahc_0([0-9]{3})_0([0-9]{3})_0([0-9]{3})((a|b)?)"
    expression = re.compile(pattern)
    for old_name in files:
        for match in expression.findall(old_name):
            directories = match[0]
            vis_number = match[1]
            folder_number = match[2]
            item_number = match[3]
            side_identifier = match[4]
            if len(side_identifier) > 0:
                new_name = f"{directories}ahc{vis_number}{folder_number}{item_number}{side_identifier.upper()}.{extension}"
            else:
                new_name = f"{directories}__ahc_0{vis_number}_0{folder_number}_0{item_number}{side_identifier}.{extension}"

            (Path(path) / Path(old_name)).rename(new_name)

def process_access(path: str, extension: str, files: List[str]) -> None:
    pattern = "(.*)ahc_0([0-9]{3})_0([0-9]{3})_0([0-9]{3})((a|b)?)"
    expression = re.compile(pattern)
    for old_name in files:
        for match in expression.findall(old_name):
            directories = match[0]
            vis_number = match[1]
            folder_number = match[2]
            item_number = match[3]
            side_identifier = match[4]
            if len(side_identifier) > 0:
                new_name = f"{directories}ahc{vis_number}{folder_number}{item_number}{side_identifier.upper()}a.{extension}"
            else:
                new_name = f"{directories}__ahc_0{vis_number}_0{folder_number}_0{item_number}{side_identifier}.{extension}"

            (Path(path) / Path(old_name)).rename(new_name)            


@click.command()
@click.option("--type", help="File type to process (master or access)")
@click.option("--path", help="Folder to process")
@click.option("--extension", help="File extension (without dot)")
def main(type: str, path: str, extension: str) -> None:
    type_enum = str_to_file_type(type)
    assert(type_enum is not None)

    path_obj = Path(path)
    assert (path_obj.exists())

    globbed = path_obj.glob(f"*.{extension}")
    files = [str(f) for f in globbed]

    if type_enum == FileType.MASTER:
        process_master(path, extension, files)
    if type_enum == FileType.ACCESS:
        process_access(path, extension, files)

if __name__ == "__main__":
    main()
