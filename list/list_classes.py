from enum import Enum


class Resolution(Enum):
    Low = 0
    High = 1


class List:
    def __init__(self, resolution, obj_list, obj_list_idx, data_ul_obj_list):
        self.resolution = resolution
        self.obj_list = obj_list
        self.obj_list_idx = obj_list_idx
        self.data_ul_obj_list = data_ul_obj_list


