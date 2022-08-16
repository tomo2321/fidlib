import collections
from typing import OrderedDict, Union

import numpy as np


def read(
    filepath: str,
    *,
    with_radius=False
) -> OrderedDict[str, np.ndarray]:

    fiducial_dict = collections.OrderedDict()
    with open(filepath) as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith('#'):
            continue
        cell_list = line.split(',')
        label_name = cell_list[-3]
        coordinate_xyz = np.array(cell_list[1:4], np.float32)
        if with_radius:
            radius = cell_list[-2] if cell_list[-2] else 1
            coordinate_xyz = np.append(coordinate_xyz, radius).astype(np.float32)
        fiducial_dict[label_name] = coordinate_xyz
    return fiducial_dict


def write(
    fiducial_dict: OrderedDict[str, Union[list, tuple, np.ndarray]],
    filepath: str
) -> None:

    contents = [
        '# Markups fiducial file version = 4.10\n',
        '# CoordinateSystem = 0\n',
        '# columns = id,x,y,z,ow,ox,oy,oz,vis,sel,lock,label,desc,associatedNodeID\n',
    ]

    def _row(index: int, pos: np.ndarray, name: str) -> str:
        x, y, z = pos
        return (
            f"vtkMRMLMarkupsFiducialNode_{index},{x:.3f},{y:.3f},{z:.3f}"
            f",0.000,0.000,0.000,1.000,1,1,0,{name},,vtkMRMLScalarVolumeNode1\n"
        )

    for i, (name, pos) in enumerate(fiducial_dict.items()):
        contents.append(_row(i, pos, name))

    with open(filepath, 'w') as f:
        f.writelines(contents)


if __name__ == '__main__':
    fcsv_filepath = './raw_tmp/landmark.fcsv'
    print(read(fcsv_filepath))


# from collections import namedtuple
# from pathlib import Path
# from typing import Dict, Tuple, Union

# import numpy as np

# _Fiducial = namedtuple("_Fiducial", "x y z radius")


# class Fiducial(_Fiducial):
#     @property
#     def pos(self) -> Tuple[float, float, float]:
#         return np.asarray((self.x, self.y, self.z))

#     def update(self, x=None, y=None, z=None, pos=None, radius=None):
#         if radius is None:
#             radius = self.radius
#         if pos is None:
#             if x is None:
#                 x = self.x
#             if y is None:
#                 y = self.y
#             if z is None:
#                 z = self.z
#             pos = (x, y, z)
#         return Fiducial(*pos, radius)


# def read_fiducials_with_radius_from_fcsv(filename: Path) -> Dict[str, Fiducial]:
#     """
#     below is the detail of fiducials file
#     --- landmark.fcsv ---
#     # Markup fiducial file version = X.X
#     # CoordinateSystem = int (default = 0)
#     # columns = id,x,y,z,ow,ox,oy,oz,vis,sel,lock,label,desc,associatedNodeID
#     vtkMRMLMarkupsFiducialNode_X,...,vtkMRMLScalarVolumeNode1
#     ...
#     --- end ---
#     """
#     marks = {}
#     with open(filename, "r") as f:
#         for line in f:
#             if line[0] == "#":
#                 continue
#             cell = line.split(",")
#             # label = (x, y, z, radius)
#             radius = float(cell[-2]) if cell[-2] else 1
#             marks[cell[-3]] = Fiducial(
#                 -float(cell[1]), -float(cell[2]), float(cell[3]), radius
#             )
#     return marks


# def write_fcsv_with_radius(
#     fiducials: Dict[str, np.ndarray],
#     radius: Dict[str, float],
#     file_path: Union[str, Path],
# ) -> None:
#     """Write fcsv with radius in desc column."""
#     contents = [
#         "# Markups fiducial file version = 4.10\n",
#         "# CoordinateSystem = 0\n",
#         "# columns = id,x,y,z,ow,ox,oy,oz,vis,sel,lock,label,desc,associatedNodeID\n",
#     ]

#     def _row(index: int, pos: np.ndarray, radius: float, name: str) -> str:
#         x, y, z = pos
#         return (
#             f"vtkMRMLMarkupsFiducialNode_{index},{x:.3f},{y:.3f},{z:.3f}"
#             f",0.000,0.000,0.000,1.000,1,1,0,{name},{radius},vtkMRMLScalarVolumeNode1\n"
#         )

#     for i, (name, pos) in enumerate(fiducials.items()):
#         contents.append(_row(i, pos, radius[name], name))

#     with open(file_path, "w") as f:
#         f.writelines(contents)


# FiducialNames = (
#     "anterior_sacral_slope",
#     "posterior_sacral_slope",
#     "rt_ASIS",
#     "lt_ASIS",
#     "rt_hip_center",
#     "lt_hip_center",
#     "pubic_tubercle",
# )
