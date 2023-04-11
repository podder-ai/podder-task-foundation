import importlib
import json


class NumpyJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        try:
            numpy = importlib.import_module("numpy")
            if isinstance(obj, numpy.integer):
                return int(obj)
            elif isinstance(obj, numpy.floating):
                return float(obj)
            elif isinstance(obj, numpy.ndarray):
                return obj.tolist()
        except ModuleNotFoundError:
            pass
        return super(NumpyJsonEncoder, self).default(obj)
