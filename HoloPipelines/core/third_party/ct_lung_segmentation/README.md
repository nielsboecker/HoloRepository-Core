This is an existing implementation of a lung and airway segmentation from CT scans, taken from https://github.com/wanwanbeen/ct_lung_segmentation (commit [120f617](https://github.com/wanwanbeen/ct_lung_segmentation/commit/120f617089a759d1fbf569cc78c21987fd6335aa)).

The actual segmentation logic is untouched. The files around have been slightly changed to fit into our system. The most significant changes are:
* added `__init__.py` to import as module
* changed the output paths
