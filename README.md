# rectangle-dropdown-annotation-generated-subjects

This is a collection of scripts that generate new Zooniverse subjects from the aggregated results for subjects attached to an existing workflow. For the purpose of this repository, we will call the existing subjects parent subjects and the generated subjects child subjects. The work here is a polished version of the scripts used to generate transcription subjects for the SCOTUS Notes Zooniverse project. That said, there are still variables that are specific to the SCOTUS Notes project.

The SCOTUS Notes project asked volunteers to identify areas of a notation associated with a particular justice and then select the associated justice's name from a dropdown. These independent annotations were aggergated using Zooniverse's Caesar and aggregation-for-caesar applications.

The general data process can be split into three steps:

1. Identify the parent subjects, by id, that will generate new child subjects. You will need a list of these subject ids before running the scripts in this repository.

2. Process the aggregated annotation data for the subjects identified in step one. The output of this script is a new subject manifest that contains the dimensions of the new subject with respect to their parent subject. The parent subject's metadata is also copied over to the child subject. This step is handled by the files in the generating_subjects_from_rectangle_dropdown_data folder.

3. Now that the dimensions of the child subjects is recorded in the new subject manifest, the next step is to create the image files for the child subjects. This step is handled by the files in the ________________ folder.
