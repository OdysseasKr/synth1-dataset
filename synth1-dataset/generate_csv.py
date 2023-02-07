import copy
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Union
from zipfile import ZipFile

import pandas as pd
from rarfile import RarFile

from .constants import DEFAULT_VALUES, META_COLS


@dataclass
class Preset:
    """
    Represents one preset for Synth1 including all parameters
    """

    name: str
    color: str
    ver: int
    params: Dict[int, int]
    bankname: Optional[str] = ""

    def to_dict(self):
        d = copy.copy(self.params)
        d["name"] = self.name
        d["color"] = self.color
        d["ver"] = self.ver
        d["bankname"] = self.bankname
        return d

    @staticmethod
    def from_file(file_content: str):
        """Creates an instance of Preset from a .sy1 file"""

        lines = file_content.split("\n")
        if len(lines) < 2:
            return None
        name = lines[0].strip()
        color = ""
        ver = ""
        params = {}
        for l in lines[1:]:
            l = l.strip()
            if l == "":
                continue
            elif "color" in l:
                color = lines[1].strip().replace("color=", "")
            elif "ver" in l:
                ver = lines[2].strip().replace("ver=", "")
            else:
                control, value = l.split(",")
                params[int(control)] = int(value)

        sorted_params = {k: params[k] for k in sorted(params.keys())}
        return Preset(name, color, ver, sorted_params)


def read_zipbank(file_path: Union[Path, str]) -> List[Preset]:
    """Reads a .zip bank and returns an array of Presets"""
    presets: List[Preset] = []
    with ZipFile(file_path, "r") as zObject:
        for name in zObject.namelist():
            if not name.endswith(".sy1"):
                continue
            with zObject.open(name) as f:
                file_content = f.read()
                file_content = file_content.decode("utf-8", errors="ignore")
                if file_content == "":
                    continue
                preset = Preset.from_file(file_content)
                if preset is not None:
                    preset.bankname = Path(file_path).stem
                    presets.append(preset)
    return presets


def read_rarbank(file_path: Union[Path, str]) -> List[Preset]:
    """Reads a .rar bank and returns an array of Presets"""
    presets: List[Preset] = []
    with RarFile(file_path, "r") as zObject:
        for name in zObject.namelist():
            if not name.endswith(".sy1"):
                continue
            with zObject.open(name) as f:
                file_content = f.read()
                file_content = file_content.decode("utf-8", errors="ignore")
                if file_content == "":
                    continue
                preset = Preset.from_file(file_content)

                if preset is not None:
                    presets.append(preset)
    return presets


def read_folder(folder_path: Union[Path, str]) -> List[Preset]:
    """Reads a folder containing multiple banks"""
    folder_path = Path(folder_path)
    presets: List[Preset] = []
    for bank in folder_path.glob("**/*.rar"):
        bank_presets = read_rarbank(bank)
        presets.extend(bank_presets)

    for bank in folder_path.glob("**/*.zip"):
        bank_presets = read_zipbank(bank)
        presets.extend(bank_presets)
    return presets


def remove_duplicates(df: pd.DataFrame):
    """Checks the CSV for duplicate entries. Only checks the actual parameters and not meta data"""
    ignored_columns = set(META_COLS)
    cols_to_compare = set(df.columns) - ignored_columns

    return df.drop_duplicates(subset=cols_to_compare)


def generate_csv(folder_path: Union[Path, str], csv_path: Union[Path, str]):
    """Given a folder with banks, generates a csv containing all preset parameters"""
    folder_path = Path(folder_path)
    csv_path = Path(csv_path)
    presets = read_folder(folder_path)

    preset_dicts = [p.to_dict() for p in presets]
    dtypes = defaultdict(lambda: int)
    for c in META_COLS:
        dtypes[c] = str
    df = pd.DataFrame(preset_dicts).astype(dtypes)
    for col, val in DEFAULT_VALUES.items():
        df[col] = df[col].fillna(val)

    df = remove_duplicates(df)
    df.to_csv(csv_path, index=False)
