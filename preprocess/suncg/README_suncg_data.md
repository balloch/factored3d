# Downloading metadata and running the precompute_scene_voxels.m script

### Getting it working with minimum data
cd factored3d;
mkdir external; cd external;
Download https://drive.google.com/open?id=1vXGr5tA7VQpwkc0umOG6Ww2d3D_lH183 and unzip in external/suncgdir

Make sure factored3d/external/suncgdir/scene_voxels is empty before running the following script:
Run precompute_scene_voxels(1, 0);
Run scripts/visualize.py

### SUNCG Dataset
Make sure the contents of the SUNCG dataset are in SUNCG_DIR. There should be 5 folders named 'house', 'room', 'object', 'texture' and 'object_vox' in SUNCG_DIR. We now download additional meta-data. Most of the scripts below are from the factored3d preprocessing readme, but I removed the ones that we definitely don't need.

```
cd factored3d;
mkdir external; cd external;
# SSC-Net code (used for computing voxelization for the baseline)
git clone https://github.com/shurans/sscnet ./sscnet

git clone https://github.com/shurans/SUNCGtoolbox

cd ..


cd SUNCG_DIR;

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


### Rendering images from camera views using SUNCGToolbox
This is the command to run from the directory house/[id]/. This will be put into a script that runs on all ids in the house directory.
```
../../../SUNCGtoolbox/gaps/bin/x86_64/scn2img house.json ../../camera/[id]/room_camera.txt ../../project_camera/[id]/ -categories ../../../SUNCGtoolbox/metadata/ModelCategoryMapping.csv -capture_color_images -capture_depth_images -capture_normal_images -capture_node_images -width 640 -height 480 -headlight
```