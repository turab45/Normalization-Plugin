import pickle
from sklearn.decomposition import PCA
from sklearn import preprocessing
from resononhyperspectral import EnviType
from src.apps.spectronon.workbench.plugin import CubePlugin
from src.lib.resonon.core.data.cube import Cube
from src.lib.resonon.utils.spec import SpecInt, SpecBool
import numpy as np


class NormalizationSimple(CubePlugin):
    """Perform Principal Component Analysis"""
    label = "Normalization Simple"
    tooltip = "Normalization Simple using numpy only."
    documentation = """  
                """

    def obsolete_header_keys(self):
        """
        Return a list of header keys that should be removed from the result header if they exist in the parent datacube
        """
        return ["reflectance scale factor", "bit depth", 'ceiling']

    def changed_header_data(self):
        """
        Return a dict of metadata keys/values that should be added or changed in the result datacube
        """
        return {"interleave": "bip",
                "data type": int(EnviType.FLOAT32)}

    def setup(self):
        datacube = self.datacube
        # self.numBands = SpecInt("Bands To Return", 1, datacube.bands, defaultValue=8)
        # self.standardize = SpecBool("Standardize?", True)
        # self.savePickle = SpecBool("Save Transformation Matrix?", defaultValue=False)

    def action(self):
        new_cube = Cube.from_metadata(self.result_header())
        datacube = self.datacube
        array = datacube.bip().copy_data(dtype=EnviType.FLOAT32)
        #array.shape = -1, datacube.bands
        
        mean = np.mean(array, axis=2, keepdims=True)
        std = np.std(array, axis=2, keepdims=True, ddof=0)
        standardized_cube = (array - mean) / std
        array = standardized_cube
        array.shape = datacube.lines, datacube.samples, -1
        new_cube.set_data(array)
        return new_cube

