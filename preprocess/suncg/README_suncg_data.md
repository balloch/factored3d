# Downloading metadata and running the precompute_scene_voxels.m script

### SUNCG Dataset
Make sure the contents of the SUNCG dataset are in SUNCG_DIR. There should be 5 folders named 'house', 'room', 'object', 'texture' and 'object_vox' in SUNCG_DIR. We now download additional meta-data. Most of the scripts below are from the factored3d preprocessing readme, but I removed the ones that we definitely don't need.

```
cd factored3d;
mkdir external; cd external;
# SSC-Net code (used for computing voxelization for the baseline)
git clone https://github.com/shurans/sscnet ./sscnet
cd ..

cd SUNCG_DIR;

# Download data splits
mkdir splits
cd splits
wget https://people.eecs.berkeley.edu/~shubhtuls/cachedir/factored3d/suncg_split.pkl
cd ..

# Download layout data (suncg houses with objects removed)
# we use this data to render the amodal depths
wget https://people.eecs.berkeley.edu/~shubhtuls/cachedir/factored3d/layout.tar.gz
tar -zxvf layout.tar.gz
mv houseLayout layout

# Download meta-data
wget https://people.eecs.berkeley.edu/~shubhtuls/cachedir/factored3d/ModelCategoryMappingEdited.csv

mkdir zipfiles; cd zipfiles;

# Download camera viewpoints
wget http://pbrs.cs.princeton.edu/pbrs_release/data/camera_v2.zip
unzip camera_v2.zip -d ../camera

# meta-data
wget http://pbrs.cs.princeton.edu/pbrs_release/data/data_goodlist_v2.txt
```

Following this:
Make sure your suncg_dir variable is properly set within globals.m
Run precompute_scene_voxels(1, 0);
