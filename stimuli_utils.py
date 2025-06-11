def generate_narrative_sentences(narrative, background=None):
    if background:
        background_sentences = [s.strip() for s in background.split('\n') if len(s.strip()) > 0]
    beginning_sentences = [s.strip() for s in narrative.split('BEGINNING')[-1].split('MIDDLE')[0].split('\n') if len(s.strip()) > 0]
    middle_sentences = [s.strip() for s in narrative.split('MIDDLE')[-1].split('END')[0].split('\n') if len(s.strip()) > 0]
    end_sentences = [s.strip() for s in narrative.split('END')[-1].split('\n') if len(s.strip()) > 0]
    if background:
        return [background_sentences] + [beginning_sentences, middle_sentences, end_sentences]
    return [beginning_sentences, middle_sentences, end_sentences]

def generate_openended_confidence_question(raw_question_text):
    question = raw_question_text.split('-')[0].strip()
    options = "How confident are you in your answer?"
    options_likert = ['Completely unsure', 'Somewhat unsure', 'Neutral', 'Somewhat sure', 'Completely sure']

    return {
        'question': question,
        'options': options,
        'options_likert_scale' : options_likert
    }

def generate_desire_question(raw_question_text):
    question = raw_question_text.split('-')[0].strip()
    options = [s.strip() for s in raw_question_text.split('-')[1:]]
    options_likert = ['Definitely did not want', 'Somewhat did not want', 'Neither wanted nor didn\'t want', 'Somewhat wanted', 'Definitely wanted']

    return {
        'question': question,
        'options': options,
        'options_likert_scale' : [
            [ol + " " + o for ol in options_likert]
            for o in options
        ]
    }

def generate_boolean_belief_question(raw_question_text):
    question = raw_question_text.split('-')[0].strip()
    option = [s.strip() for s in raw_question_text.split('-')[1:]][0]
    option_likert = ['Definitely believed', 'Somewhat believed', 'Neither believed nor did not believe', 'Somewhat did not believe', 'Definitely did not believe']  
    q = {
        'question': question,
        'option': option,
        'option_likert_scale': [ol + " " + option for ol in option_likert]
    }
    return q

def generate_engaging_question(raw_question_text):
    question = raw_question_text.strip()
    option_likert = ['The least fun story in this setting', 'The most fun story in this setting']
    return {
    'question': question,
       'option_likert_scale' : option_likert
    }