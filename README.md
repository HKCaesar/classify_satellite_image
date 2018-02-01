# Classify Satellite Images

## Getting Started

In order to use the following code, you need to install:

### 1. GDAL

GDAL is a translator library for raster and vector geospatial data formats.
Please follow this link to install it [Install GDAL](https://trac.osgeo.org/gdal/wiki/GdalOgrInPython)

### 2. Scikit-Learn

Sciki-learn is a Python library for machine learning that you can install with Python Index Package:

### 3. Others

You can install all others dependencies by running on your Terminal

```
pip3 install -r requirements.txt
```

## Data source

In order to test this dataset, please download the following from Google Drive:

[Data Source](https://drive.google.com/open?id=1VzEmH4ex36sbYDWDAf2M2eY-tcjsH2lD)

Please copy the file data at the source of the project.
The file data contains 3 folders (images, test, train).


## How to use your own Images

TO DO

## Code

### Utils functions:

We use 3 differents functions.

1. create_mask_from_vector:

This function rasterize the given vector (wrapper for gdal.RasterizeLayer). 

2. vectors_to_raster:

This function rasterize all the vectors in the given directory into a single image.

3. write_geotiff:

We can save an satellite image with imsave but we'll loose all spatial informations, that's why we use this function which will create a GeoTIFF file with the given data.


### Main function:

TO DO
## Authors

* Yassine Belmamoun (CentraleSupélec)
* Akrem Bahri (CentraleSupélec - MVA)
