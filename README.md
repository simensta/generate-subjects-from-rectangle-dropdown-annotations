# Generate subjects from rectangle+dropdown annotations

This collection of python and bash scripts generates new Zooniverse subjects from the aggregated annotations produced by a combined drawing and dropdown labeling task. In this repository, I will reference annotated subjects as parent subjects and the generated subjects as child subjects. The work here is a polished version of the scripts used to generate transcription subjects for the SCOTUS Notes Zooniverse project. That said, there are still variables that are specific to the SCOTUS Notes project within this repository.

The SCOTUS Notes project asked volunteers to identify areas of an image associated with a particular justice and then select the associated justice's name from a dropdown. These independent annotations were aggregated using Zooniverse's [Caesar](https://github.com/zooniverse/caesar) and [aggregation-for-caesar](https://github.com/zooniverse/aggregation-for-caesar) applications.

The general data process can be split into three steps:

1. Identify the parent subjects, by id, that will generate new child subjects. You will need a list of these subject ids before running the scripts in this repository.

2. Process the aggregated annotation data for the subjects identified in step one. The output of this script is a new subject manifest that contains the dimensions of the new subject with respect to their parent subject. The parent subject's metadata is also copied over to the child subject. This step is handled by the files in the generate_subject_manifest folder.

3. Now that the dimensions of the child subjects is recorded in the new subject manifest, the next step is to create the image files for the child subjects. This step is handled by the files in the generated_subject_images folder.
