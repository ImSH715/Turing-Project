import pandas as pd
import rasterio
from rasterio.windows import Window
from pyproj import Transformer
import numpy as np
import os
from PIL import Image

#df = '../Dataset/Censo Forestal.csv'
df_tif_included = '../Dataset/features_tif_included.csv'
#df_five = '../Dataset/five_random_per_species.csv'
tif_repo = '../../../p4_transparent_mosaic_group1.tif'
save_repo = '../Dataset/Feature_Images'

df = pd.read_csv(df_tif_included)
raster = rasterio.open(tif_repo)

around_size = 20


classes = df['NOMBRE_CIENTIFICO'].unique()
for cls in classes:
    os.makedirs(os.path.join(save_repo, cls), exist_ok=True)



def generate_feature_jpg(input, tif, output, feature_size):
    res_x, res_y = tif.res
    half_w = int(feature_size/res_x/2)
    half_h = int(feature_size/res_y/2)

    # feature extraction based on the coordinate
    counter = {cls:1 for cls in input['NOMBRE_CIENTIFICO'].unique()} # File number per class
    
    for idx, row in input.iterrows():
        x,y = row['COORDENADA_ESTE'], row['COORDENADA_NORTE']
        cls = row['NOMBRE_CIENTIFICO']

        # Coordinate -> Rows and Columns
        row_idx, col_idx = tif.index(x,y)

        # Checking range
        if (0 <= row_idx - half_h) and (row_idx + half_h <= tif.height) and \
            (0 <= col_idx - half_w) and (col_idx + half_w <= tif.width):
            # Feature Extraction
            window = Window(col_idx - half_w, row_idx - half_h, 2*half_w, 2*half_h)
            feature = tif.read(window=window) # Shape into : (bands, height, width)

            # Coverting to RGB image
            feature_img = np.moveaxis(feature, 0, -1) # (height, width, bands)
            if feature_img.shape[2]>3:
                feature_img = feature_img[:,:,:3]

            feature_img = np.clip(feature_img, 0, 255).astype(np.uint8)

            save_img_path = os.path.join(output, cls, f"{counter[cls]}.jpg")
            Image.fromarray(feature_img).save(save_img_path)
            counter[cls] += 1
            print(f"Feature Saved {x},{y}")
        else:
            print(f"Feature Skipped {x}, {y}")

generate_feature_jpg(df, raster, save_repo, around_size)