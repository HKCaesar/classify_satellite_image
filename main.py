import numpy as np
import os
from osgeo import gdal
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from utils import create_mask_from_vector, vectors_to_raster, write_geotiff

# Colors for the ouput 
COLORS = ["#000000", "#FFFF00", "#1CE6FF", "#FF34FF", "#FF4A46", "#008941"]


def main():
    raster_dataset = gdal.Open(raster_data_path, gdal.GA_ReadOnly)
    geo_transform = raster_dataset.GetGeoTransform()
    proj = raster_dataset.GetProjectionRef()
    bands_data = []
    for b in range(1, raster_dataset.RasterCount+1):
        band = raster_dataset.GetRasterBand(b)
        bands_data.append(band.ReadAsArray())

    bands_data = np.dstack(bands_data)
    rows, cols, n_bands = bands_data.shape

    files = [f for f in os.listdir(train_data_path) if f.endswith('.shp')]
    classes = [f.split('.')[0] for f in files]
    shapefiles = [os.path.join(train_data_path, f)
                  for f in files if f.endswith('.shp')]

    labeled_pixels = vectors_to_raster(shapefiles, rows, cols, geo_transform, proj)
    is_train = np.nonzero(labeled_pixels)
    training_labels = labeled_pixels[is_train]
    training_samples = bands_data[is_train]

    classifier = RandomForestClassifier(n_jobs=4, n_estimators=10)
    classifier.fit(training_samples, training_labels)

    n_samples = rows*cols
    flat_pixels = bands_data.reshape((n_samples, n_bands))
    result = classifier.predict(flat_pixels)

    classification = result.reshape((rows, cols))
    write_geotiff(output_fname, classification, geo_transform, proj)

    shapefiles = [os.path.join(validation_data_path, "%s.shp"%c) for c in classes]
    verification_pixels = vectors_to_raster(shapefiles, rows, cols, geo_transform, proj)
    for_verification = np.nonzero(verification_pixels)
    verification_labels = verification_pixels[for_verification]
    predicted_labels = classification[for_verification]

    print("Confussion matrix:\n%s" %
          metrics.confusion_matrix(verification_labels, predicted_labels))
    target_names = ['Class %s' % s for s in classes]
    print("Classification report:\n%s" %
          metrics.classification_report(verification_labels, predicted_labels,
                                        target_names=target_names))
    print("Classification accuracy: %f" %
          metrics.accuracy_score(verification_labels, predicted_labels))

if __name__ == '__main__':
    # Input 
    raster_data_path = "data/image/2298119ene2016recorteTT.tif"
    output_fname = "classification.tiff"
    train_data_path = "data/train"
    validation_data_path = "data/test"

    main()

