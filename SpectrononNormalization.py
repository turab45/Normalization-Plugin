import pickle
from sklearn.decomposition import PCA
from sklearn import preprocessing
from resononhyperspectral import EnviType
from src.apps.spectronon.workbench.plugin import CubePlugin
from src.lib.resonon.core.data.cube import Cube
from src.lib.resonon.utils.spec import SpecInt, SpecBool
import numpy as np


class SpectrononNormalization(CubePlugin):
    """Normalize Datacube using the Spectronon method"""
    label = "Normalization using the Spectronon method"
    tooltip = "Principal Component Analysis can be used to reduce the dimensionality of a datacube or remove " \
              "noise. It is also useful for exploratory data analysis."
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
        array.shape = -1, datacube.bands
        
        # mean = np.mean(array, axis=2, keepdims=True)
        # std = np.std(array, axis=2, keepdims=True, ddof=0)
        # standardized_cube = (array - mean) / std
        # array = standardized_cube
        scaler = preprocessing.StandardScaler().fit(array)
        array = scaler.transform(array)

        # pca = PCA(n_components=self.numBands.value)
        # pca.fit(array)
        # results = pca.transform(array)

        # self.wb.plot(pca.explained_variance_ratio_)
        array.shape = datacube.lines, datacube.samples, -1
        new_cube.set_data(array)
        return new_cube

