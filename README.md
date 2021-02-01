# Mask RCNN detections for Toyota Smarthome dataset

This project uses [Matterport's implementation of Mask RCNN](https://github.com/matterport/Mask_RCNN) to retrieve
bounding boxes for detected humans in the [Toyota Smarthome](https://project.inria.fr/toyotasmarthome/) dataset, as 
described in our paper (Climent-Pérez et al. 2021, _accepted_).

These calculated bounding boxes are then used in the `DAIGroup/i3d` project to extract crops of the images around the
detections.

## Download and reproducibility

You have two options, to **clone** this project and run it (you will need a copy of the dataset), or to download the detections that this network produced.

### Pre-calculated bounding boxes

You can dowload them from this Google Drive link. [[download]](https://drive.google.com/file/d/1a0aSnX0EI46jWOn5lX482Tpyf7vbyCn-/view?usp=sharing).

There are two directories within the downloaded `.tgz` file.

* `mp4_mrcnn_bbox` contains the bounding boxes calculated with Mask RCNN as is, that is, the _raw_ version.
* `mp4_mrcnn_bbox_nogaps` contains versions of _some_ videos that had gaps in detection, of <60 frames, that have been
filled-in with the preprocessing scripts found in the companion `DAIGroup/i3d` project ([here](github.com/DAIGroup/i3d)).
  
The preprocessing scripts in the `DAIGroup/i3d` project **will take the _best_ available file**: that is, if the detection file is only
present in the `mp4_mrcnn_bbox` directory it will take that, but if a _corrected_ version is available in the
`mp4_mrcnn_bbox_nogaps` directory it will take that instead.
  
**NOTE:** If using them in your research, please cite (Climent-Pérez et al. 2021) below.

## References

* **(Das et al. 2019)** Das, S., Dai, R., Koperski, M., Minciullo, L., Garattoni, L., Bremond, F., & Francesca, G. (2019). Toyota smarthome: Real-world activities of daily living. In Proceedings of the IEEE International Conference on Computer Vision (pp. 833-842).
* **(Climent-Pérez et al. 2021, _accepted_)** Climent-Pérez, P., Florez-Revuelta, F. (2021). Improved action recognition with Separable spatio-temporalattention using alternative Skeletal and Video pre-processing, Sensors, _accepted_.

### Copyright of Mask RCNN implementation
Copyright (c) 2017 Matterport, Inc.

Licensed under the MIT License (see [LICENSE](https://github.com/matterport/Mask_RCNN) for details)
Written by Waleed Abdulla



