"""
Batches stimuli into JSON files.
"""

import os
import json
import argparse
import csv
from collections import defaultdict
import stimuli_utils

parser = argparse.ArgumentParser()

parser.add_argument('--csv', type=str, default='stimuli/csv/engaging-narratives-jun-1.csv')
parser.add_argument('--output_dir', type=str, default='stimuli/json/')
parser.add_argument('--output_file', type=str, required=True)

# Main function.
if __name__ == "__main__": 
    args = parser.parse_args()

    # Read in the CSV.
    with open(args.csv, "r") as f:
        # Use CSV dict-reader to read the base file.
        reader = csv.DictReader(f)
        stimuli = list(reader)

    stimuli_for_settings = defaultdict(dict)
    stimuli_qs_for_settings = defaultdict(dict)
    question_types = []
    narrative_types = []

    for stim in stimuli:
        if stim['narrative-type'].startswith('q'):
            is_narrative = False
            question_types.append(stim['narrative-type'])
            stim_dict = stimuli_qs_for_settings
        else:
            is_narrative = True
            narrative_types.append(stim['narrative-type'])
            stim_dict = stimuli_for_settings
        settings = [k for k in stim.keys() if k != 'narrative-type']
        for setting in settings:    
            if is_narrative:
                stim_dict[setting][stim['narrative-type']] = {
                    'raw_narrative' : stim[setting],
                    'narrative-sentences' : stimuli_utils.generate_narrative_sentences(stim[setting])
                }
            else:
                if stim['narrative-type'] == 'q-comprehension-outcome':
                    stim_dict[setting][stim['narrative-type']] = stimuli_utils.generate_desire_question(stim[setting])
                elif stim['narrative-type'] == 'q-comprehension-initial-belief':
                    stim_dict[setting][stim['narrative-type']] = stimuli_utils.generate_boolean_belief_question(stim[setting])
                elif stim['narrative-type'] == 'q-engaging':
                    stim_dict[setting][stim['narrative-type']] = stimuli_utils.generate_engaging_question(stim[setting])
    
    # JSON with all the possible settings; the scenario types; and the scenario types for each setting.
    stimuli_batch = {
        'settings': list(stimuli_for_settings.keys()),
        'scenario-types': narrative_types,
        'question-types': question_types,
        'stimuli-for-settings': stimuli_for_settings,
        'stimuli-qs-for-settings': stimuli_qs_for_settings
    }

    with open(os.path.join(args.output_dir, args.output_file), 'w') as f:
        json.dump(stimuli_batch, f, indent=4)