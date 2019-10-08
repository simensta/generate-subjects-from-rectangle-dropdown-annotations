#!/usr/bin/env python
# coding: utf-8

import datetime
import csv
import json
import re
import argparse

justice_abreviation_dictionary = {
    'HAB': 'HABlackmun',
    'WJB': 'WJBrennan',
    'HHB': 'HHBurton',
    'WOD': 'WODouglas',
    'FF':  'FFrankfurter',
    'RHJ': 'RHJackson',
    'TM': 'TMarshall',
    'LFP': 'LFPowell',
    'WHR': 'WHRehnquist',
    'WBR': 'WBRurledge',
    'EW': 'EWwarren'
}

# justice_dropdown_dictionary captures the properties and values 
# corresponding to the dropdown options from workflow #3521
justice_dropdown_dictionary = {
    '090a933557f89': 'Black',             
    '5c71a891b4837': 'Blackmun',
    'e1ec42938f3d': 'Brennan',
    '18daf8db00bde': 'Burton',
    '78a880ae99fb2': 'Clark',
    '6f2af80595129': 'Douglas',
    'ed4c9c583b4a7': 'Fortas',
    '0df611635e746': 'Frankfurter',
    '5e2afbc5893d2': 'Ginsburg',
    '22cd4e9ecfb9d': 'Goldberg',
    'dfa947e503dd6': 'Harlan',
    '223e6cb1e1d8e': 'Jackson',
    '2a98ce1175873': 'Kennedy',
    '0ec5e7e94865d': 'Marshall',
    'd7ccedc747b6a': 'OConnor',
    'c25051ea0d895': 'Powell',
    '7f7a6fc7f4d5c': 'Reed',
    '21750f330922a': 'Rehnquist',
    'b63a71ea98766': 'Scalia',
    '21d183267c77': 'Souter',
    '8b62283f2dfde': 'Stevens',
    'cd1896ba3853a': 'Stewart',
    '3cd8c5e843703': 'Thomas',
    '422fba5a6aeb9': 'Warren',
    'd144a06e078f4': 'White',
    '34a8f339d9bf9': 'Whittaker',
    '95c7e690799a8': 'The_Chief_Justice',
    '0bf44c6cdbb6f': 'Chief_Justice',
    'None': 'None',
}

# In earlier versions of Caesar, ruby rockets appeared
# in the reduction export. This method removes the 
# rockets for easier use of the data in python
def remove_rockets_from_object(dataWithRockets):
    dataWithColons = dataWithRockets.replace('=>', ': ')
    frame0 = json.loads(dataWithColons)
    return frame0

def find_parent_file_name(subject_metadata):
    # example file name "1980-WJB_79-408_1_StevensJP.jpg"
    # early metadata contained "file_name" instead of "#image_file"
    if 'file_name' in subject_metadata:
        parent_file_name = subject_metadata['file_name']
    elif '#image_file' in subject_metadata:
        parent_file_name = subject_metadata['#image_file']
    else:
        # This else loop could be modified to throw an error if
        # neither "file_name" nor "#image_file" are in subject_metadata
        parent_file_name = ""
    return parent_file_name

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create a new subject manifest from the rectangle+dropdown annotations for existing subjects")
    parser.add_argument("-subject_export", required=True, help="The file path to the subject export from the Zooniverse project builder")
    parser.add_argument("-reduction_export", required=True, help="The file path to the reduction export from Caesar")
    parser.add_argument("-subject_ids", required=True, help="String of subject ids seperated by commas (no space) to be processed")

    args = parser.parse_args()

    # the following variables track stats of interest
    number_of_subjects_with_unassigned_annotations = 0
    number_of_subjects_with_no_data = 0
    number_of_multiple_labels = 0

    newly_retired_subject_ids = args.subject_ids.split(',')
    file_path_for_caesar_reduction_export = args.reduction_export
    file_path_for_subject_export = args.subject_export

    # Create the CSV file in which each row will be a new transcription subject
    file_path_for_new_csv_manifest = "new_subject_manifests/new_subjects_" + datetime.datetime.now().strftime("%a_%d_%b_%Y_%H_%M_%S").lower() + ".csv"
    with open(file_path_for_new_csv_manifest, 'w') as csvfile:

        # fieldnames captures the headers that will be present in the new subject manifest
        fieldnames = ["image_name","#caesar_id","#parent_subject_ids","#subject_set_id","#x","#y","#width","#height","justice_described","author","#url","oyez","term", "caseId", "docket", "usCite", "caseName", "docketId","#T2_tool0_cluster_count","#label_votes"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # read in the reducer export file from Caesar
        with open(file_path_for_caesar_reduction_export) as csvfile:
            subject_rows = csv.DictReader(csvfile)
            for subject in subject_rows:

                if subject["subject_id"] in newly_retired_subject_ids: 
                    dataWithRockets = subject['data.frame0']
                    
                    # If there is no data, continue to next subject row
                    if dataWithRockets == "":
                        number_of_subjects_with_no_data += 1
                        continue
                    
                    # Replace the ruby rockets with colons so that json.loads can import the data
                    # Later versions of Ceasar exports may not have the rockets
                    frame0 = remove_rockets_from_object(dataWithRockets)
                    numberOfXValues = frame0['T2_tool0_rec_x']
                    
                    # check to see if clusters have been assigned
                    # # the `_cluster_labels` value is a list of numbers that "name" each cluster, 
                    # # there is one value for each annotation. 
                    # # A value of `-1` means it does not belong to any cluster.                  
                    number_of_annotations = len(frame0["T2_tool0_cluster_labels"])
                    number_of_unused_annotations = frame0["T2_tool0_cluster_labels"].count(-1)
                    
                    # Are all the annotations unassigned to a cluster?
                    # For now, let's count the number of times this happens and move to the next subject row
                    if number_of_annotations == number_of_unused_annotations:
                        number_of_subjects_with_unassigned_annotations += 1
                        continue
                    
                    clusters = frame0['T2_tool0_clusters_count']
                   
                    # rectangle clusters
                    for index, cluster in enumerate(clusters):
                        # Only create new subjects out of clusters with three or more annotations
                        if cluster >= 3:
                            
                            cluster_x = frame0['T2_tool0_clusters_x'][index]
                            cluster_y = frame0['T2_tool0_clusters_y'][index]
                            cluster_width = frame0['T2_tool0_clusters_width'][index]
                            cluseter_height = frame0['T2_tool0_clusters_height'][index]

                            # Determine Justice Label
                            number_of_values_for_label = len(frame0['T2_tool0_clusters_details'][index][0]['value'])
                            
                            if number_of_values_for_label is 0:
                                continue
                            
                            possible_justice_labels = frame0['T2_tool0_clusters_details'][index][0]['value'][0]
                            number_of_labels = len(frame0['T2_tool0_clusters_details'][index][0]['value'][0])

                            if number_of_labels > 1:
                                number_of_multiple_labels += 1

                            if number_of_labels is 1:
                                # if no dropdown value is specified, continue to the next cluster
                                if len(frame0['T2_tool0_clusters_details'][index][0]['value']) is 0:
                                    continue
                                justice_details = frame0['T2_tool0_clusters_details'][index][0]['value'][0]
                                pairs = [(v, k) for (k, v) in justice_details.items()]
                                justice_label = pairs[0][1]
                                label_votes = pairs[0][0]
                                
                                if label_votes > 3:
                                    justice_name = justice_dropdown_dictionary[justice_label]
                                    # At this point, the child subject should be turned into a csv row
                                    # In order to get the subject metatdata information, 
                                    # we need read in the subject export
                                    with open(file_path_for_subject_export) as csvfile:
                                        metadata_for_subjects = csv.DictReader(csvfile)
                                        for subject_row in metadata_for_subjects:
                                            if subject_row['subject_id'] == subject['subject_id']:
                                                subject_metadata = json.loads(subject_row['metadata'])
                                                location = json.loads(subject_row['locations'])["0"]

                                                parent_file_name = find_parent_file_name(subject_metadata)
                                                split_parent_file_name = parent_file_name.split(".")
                                                child_file_name = split_parent_file_name[0] + "_" + justice_name + "." + split_parent_file_name[1]

                                                author_initials = parent_file_name.split('-')[1].split('_')[0]
                                                author_name = justice_abreviation_dictionary[author_initials]

                                                writer.writerow({
                                                    "image_name": child_file_name,
                                                    "#caesar_id": subject['id'],
                                                    "#parent_subject_ids": subject['subject_id'],
                                                    "#subject_set_id": subject_row['subject_set_id'],
                                                    "#x": cluster_x,
                                                    "#y": cluster_y,
                                                    "#width": cluster_width,
                                                    "#height": cluseter_height,
                                                    "justice_described": justice_name,
                                                    "author": author_name,
                                                    "#url": location,
                                                    "oyez": subject_metadata['oyez'],
                                                    "term": subject_metadata['term'],
                                                    "caseId": subject_metadata['caseId'],
                                                    "docket": subject_metadata['docket'],
                                                    "usCite": subject_metadata['usCite'],
                                                    "caseName": subject_metadata['caseName'],
                                                    "docketId": subject_metadata['docketId'],
                                                    "#T2_tool0_cluster_count": cluster,
                                                    "#label_votes": label_votes
                                                }) 

    print("Created subject manifest.")                                
    print("number_of_subjects_with_no_data: ", number_of_subjects_with_no_data)
    print("number_of_subjects_with_unassigned_annotations: ", number_of_subjects_with_unassigned_annotations)
    print("number_of_multiple_labels: ", number_of_multiple_labels)
