"""
Analysis script for pilot data.
"""
import argparse
from collections import defaultdict
import os
import csv 

parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', type=str, required=True)

# Main function.
if __name__ == "__main__": 
    args = parser.parse_args()
    all_unique_subjects = set()
    base_scenario_types = ['narrative-each-sentence-uncertain-latent-uncertain-outcome', 'narrative-same-latent-likely-latent-likely-outcome', 'narrative-similar-events-likely-latent-likely-outcome']

    # Read in participant data if they successfully made it to the end of the experiment.
    scenario_html_keyboard_responses = defaultdict(lambda: defaultdict(dict))
    scenario_question_responses = defaultdict(lambda: defaultdict(dict))

    for csv_file in os.listdir(args.input_dir):
        try:
            with open(os.path.join(args.input_dir, csv_file), 'r') as f: 
                f_text = f.read()
            if 'survey-text' in f_text and 'Q0' in f_text and 'survey-html-form' in f_text and 'html-keyboard-response' in f_text:
                # Read in the participant data.
                with open(os.path.join(args.input_dir, csv_file), 'r') as f: 
                    reader = csv.DictReader(f)
                    for row in reader:
                        subject = row['subject']
                        all_unique_subjects.add(subject)
                        if row['trial_type'] == 'html-keyboard-response':
                            scenario = eval(row['scenario'])
                            keypresses = eval(row['all_keypresses'])
                            setting, scenario_type = scenario['setting'], scenario['scenario_type']
                            scenario_html_keyboard_responses[setting][scenario_type][subject] = keypresses
                        elif row['trial_type'] == 'survey-html-form':
                            scenario = eval(row['scenario'])
                            setting, scenario_type = scenario['setting'], scenario['scenario_type']
                            scenario_question_responses[setting][scenario_type][subject] = scenario
        except:
            continue
        

    # Summary analysis 1: How many participants saw each condition?
    print("====Summary of number of responses===")
    print("Total unique subjects: " + str(len(all_unique_subjects)))
    for setting in scenario_question_responses.keys():
        print(setting)
        for base_scenario_type in base_scenario_types:
            print("\t", base_scenario_type, len(scenario_question_responses[setting][base_scenario_type].keys())) 

    # Fun analysis 1: *across* participants, for a given setting, is there a difference in the overall raw funness rating for a given narrative type?
    print("=======Engagement ratings======")
    print("=====Raw averages=======")
    for setting in scenario_question_responses.keys():
        print(setting)
        for base_scenario_type in base_scenario_types:
            # Average funness rating across participants.
            funness_ratings = [scenario_question_responses[setting][base_scenario_type][subject]['slider_values']['slider-q-engaging'] for subject in scenario_question_responses[setting][base_scenario_type].keys()]
            if len(funness_ratings) > 0:
                print("\t", base_scenario_type, "n=" + str(len(funness_ratings)), "Mean: " + str(sum(funness_ratings) / len(funness_ratings)), "Std: " + str((sum((x - sum(funness_ratings) / len(funness_ratings)) ** 2 for x in funness_ratings) / len(funness_ratings)) ** 0.5)) 
            else:
                print("\t", base_scenario_type, "Mean: N/A", "Std: N/A") 
    

        # What were the average funness ratings for each story and how much inter-participant variability is there?
        # Do we need to normalize the funness ratings for each participant?
    
    # Comprehension analyis 
    print("=======Comprehension questions======")
    for setting in scenario_question_responses.keys():
        print(setting)
        for base_scenario_type in base_scenario_types:
            # Average funness rating across participants.
            latent_values = [scenario_question_responses[setting][base_scenario_type][subject]['input_values']['input-q-comprehension-openended-latent'] for subject in scenario_question_responses[setting][base_scenario_type].keys()]
            outcome_values = [scenario_question_responses[setting][base_scenario_type][subject]['input_values']['input-q-comprehension-openended-outcome'] for subject in scenario_question_responses[setting][base_scenario_type].keys()]
            if len(latent_values) > 0:
                print("\t", base_scenario_type, "n=" + str(len(latent_values)), "Latent: " + str(latent_values))
                print("\t", base_scenario_type, "n=" + str(len(outcome_values)), "Outcome: " + str(outcome_values))
            else:
                print("\t", base_scenario_type, "Comprehension: N/A") 
    




