# Generate Subject Images

This folder contains a bash script (i.e., create_child_subject_images.sh) for parsing a subject manifest produced by generate_transcription_subjects.py. Using the parsed dimension data, the script creates a new image file for each subject row.

An example of running create_child_subject_images.sh from the command line:

```
bash create_child_subject_images.sh path/to/new_subject_manifests/new_subjects_tue_08_oct_2019_14_35_39.csv path/to/generate_subject_images/generated_subject_images
```
