# Subject Generator from Caesar Reductions

## Running the Script

`generate_transcription_subjects.py` is run from the command line. To read further about the arguments required to run this script, please see the help parameter (i.e., `-h`):

```
$ python generate_transcription_subjects.py -h
usage: generate_transcription_subjects.py [-h] -subject_export SUBJECT_EXPORT
                                          -reduction_export REDUCTION_EXPORT
                                          -subject_ids SUBJECT_IDS

Create a new subject manifest from the rectangle+dropdown annotations for
existing subjects

optional arguments:
  -h, --help            show this help message and exit
  -subject_export SUBJECT_EXPORT
                        The file path to the subject export from the
                        Zooniverse project builder
  -reduction_export REDUCTION_EXPORT
                        The file path to the reduction export from Caesar
  -subject_ids SUBJECT_IDS
                        String of subject ids seperated by commas (no space)
                        to be processed
```

Below is an example of how to run the script from the command line:

```
python generate_transcription_subjects.py -subject_export project-name-subjects.csv -reduction_export caesar-reduction-export.csv -subject_ids 17025343,17032151,17032161,17085641,17085656,17160441,17160652,17032225
```

## Reduction Export Fields:
The following is a description of some of the reduction fields evaluated in `generate_transcription_subjects.py`. For a more thorough and up-to-date description, see the aggregation-for-caesar docs for the [rectangle reducer](https://aggregation-caesar.zooniverse.org/reducers.html#rectangle-reducer) and the [dropdown reducer](https://aggregation-caesar.zooniverse.org/reducers.html#dropdown-reducer).

 - **id**: Caesar Id for reducer entry
 - **reducer_key**: Key name specified for Caesar reducer
 - **workflow_id**: Specifies the id for the workflow that generated the classification that served as input to the reducer
 - **subject_id**: Specifies the id of the subject that was classified
 - **created_at**: Timestamp for the creation of the reduction for the subject in Caesar
 - **updated_at**: Timestamp for the last time this reduction was updated in Caesar
 - **data.frame0**: This field contains the aggregation data for the subject
    - **data.frame0.T2_tool0_rec_x**: all of the x coordinates from all the annotations for this row's subject
    - **T2_tool0_rec_y**: all of the y coordinates from all the annotations for this row's subject
    - **T2_tool0_rec_width**: all of the width values from all the annotations for this row's subject
    - **T2_tool0_rec_height**: all of the height values from all the annotations for this row's subject
    - **T2_tool0_cluster_labels**: _A list of cluster labels for all rectangles drawn with tool*_
        - An example: [0, 1, 0, -1, 1, 2, 0, 1, 2, 0, 2, 1]
        - "the `_cluster_labels` value is a list of numbers that 'name' each cluster, 
        there is one value for each classification.  A value of `-1` means it does not belong to any cluster.
        So in this example the first, third, seventh, and tenth classifications were assigned to the same cluster." - Coleman Krawczyk, [Slack](https://zooniverse.slack.com/archives/C5DMXTVQC/p1518020423000269?thread_ts=1517933068.000918&cid=C5DMXTVQC) 
    - **T2_tool0_clusters_count**: _The number of independent contributions used to calculate each cluster_
