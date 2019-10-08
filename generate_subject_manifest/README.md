# Subject Generator from Caesar Reductions

## Running the Script

Script `generate_transcription_subjects.py` is run from the command line. To read further about the arguments required to run this script, you can run the following:

```
python generate_transcription_subjects.py -h
usage: generate_transcription_subjects.py [-h]
                                          subject_export reduction_export
                                          subject_ids

Create a new subject manifest from the rectangle+dropdown annotations for
existing subjects

positional arguments:
  subject_export    The file path to the subject export from the Zooniverse
                    project builder
  reduction_export  The file path to the reduction export from Caesar
  subject_ids       String of subject ids seperated by commas (no space) to be
                    processed

optional arguments:
  -h, --help        show this help message and exit

```

Below is an example of how to run the script:

```
python generate_transcription_subjects.py -subject_export project-name-subjects.csv -reduction_export caesar-reduction-export.csv -subject_ids 17025343,17032151,17032161,17085641,17085656,17160441,17160652,17032225
```

## Reduction Export Fields:
The following bullet list may be helpful in understanding the reduction export.

 - **id**: Caesar Id for reducer entry
 - **reducer_key**: Key name specified for Caesar reducer
 - **workflow_id**: Specifies the id for the workflow that generated the classification that served as input to the reducer
 - **subject_id**: Specifies the id of the subject that was classified
 - **created_at**: Timestamp for the creation of the reduction for the subject in Caesar
 - **updated_at**: Timestamp for the last time this reduction was updated in Caesar
 - **subgroup** - this project is not using this field
 - **data.frame0**: This field contains the aggregations data for the subject
    - **data.frame0.T2_tool0_rec_x**: all of the x coordinates from all the annotations for this row's subject
    - **T2_tool0_rec_y**: all of the y coordinates from all the annotations for this row's subject
    - **T2_tool0_rec_width**: all of the width values from all the annotations for this row's subject
    - **T2_tool0_rec_height**: all of the height values from all the annotations for this row's subject
    - **T2_tool0_cluster_labels**: _A list of cluster labels for all rectangles drawn with tool*_
        - An example: [0, 1, 0, -1, 1, 2, 0, 1, 2, 0, 2, 1]
        - "the `_cluster_labels` value is a list of numbers that 'name' each cluster, 
        there is one value for each classification.  A value of `-1` means it does not belong to any cluster.
        So in this example the first, third, seventh, and tenth classifications were assigned to the same cluster." 
    - **T2_tool0_details**
    - **T2_tool0_clusters_count**: _The number of independent contributions used to calculate each cluster_
    - **T2_tool0_clusters_x**
    - **T2_tool0_clusters_y**
    - **T2_tool0_clusters_width**
    - **T2_tool0_clusters_height**
    - **T2_tool0_clusters_details**