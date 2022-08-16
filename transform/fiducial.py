from typing import List, Optional, Tuple, Union

import numpy as np


AXIS2INDEX_DICT = {
    axis: i
    for i, axis in enumerate('xyz')
}


class Fiducial(object):
    def __init__(
            self,
            fiducial: Union[list, tuple, np.ndarray],
            spacing: Union[list, tuple, np.ndarray] = (1, 1, 1),
            origin: Union[list, tuple, np.ndarray] = (0, 0, 0),
            name: Optional[str] = None
        ) -> None:
        self._init_obj = tuple(
            self._to_float32(array)
            for array in (fiducial, spacing, origin)
        ) + (name,)
        [self._check_xyz(array) for array in self._init_obj[:3]]
        self._fiducial = self._init_obj[0]
        self._spacing = self._init_obj[1]
        self._origin = self._init_obj[2]
        self.name = self._init_obj[3]
        self._is_mm = True

    def reset(self):
        self.__init__(*self._init_obj)
        return self

    @property
    def fiducial(self):
        """(x, y, z)"""
        return self._fiducial

    @property
    def spacing(self):
        """(x, y, z)"""
        return self._spacing

    @property
    def origin(self):
        """(x, y, z)"""
        return self._origin

    offset = origin

    @property
    def header(self):
        return {
            'spacing': self._spacing,
            'origin': self._origin,
        }

    def translation(self, value):
        """(x, y, z)"""
        self._check_xyz(value)
        self._orgin += value
        return self

    def flip(self, axis: Union[str, List[str], Tuple[str]]):
        for ax in axis:
            ax = ax.lower()
            index = AXIS2INDEX_DICT[ax]
            self._fiducial[index] *= -1
        return self

    def to_pix(self):
        if self._is_mm:
            self._fiducial /= self._spacing
            self._is_mm = False
        return self

    def to_mm(self):
        if self._is_mm:
            pass
        else:
            self._fiducial *= self._spacing
            self._is_mm = True
        return self

    def _to_float32(self, value):
        return np.array(value, np.float32)

    def _check_xyz(self, value):
        if len(value) != len('xyz'):
            raise ValueError(f"expected 3, got {len(value)}")

    def __str__(self):
        return str(self._fiducial)


if __name__ == '__main__':
    fiducial = Fiducial(np.array([0, 0, 0]))
