
# Scoring for spelling based on the number of misspelled words
def score_spelling(misSpell_count):
    if misSpell_count >= 15:
        return 4
    elif 10 <= misSpell_count < 15:
        return 3
    elif 5 <= misSpell_count < 10:
        return 2
    elif 1 <= misSpell_count < 5:
        return 1
    else:
        return 0

# Scoring for the length of the essay based on the number of sentences
def score_length(sentence_count):
    if sentence_count >= 15:
        return 5
    elif 8 <= sentence_count <= 14:
        return 4
    elif 6 <= sentence_count <= 7:
        return 3
    elif 1 <= sentence_count <= 5:
        return 2
    else:
        return 1

def score_syntax(syntax_error):
    #max is 5pts(no errors) lowest is 0
    score = 0
    for error_dict in syntax_error:
        for value in error_dict.values():
            if value is False:
                score += 1
    return score


def map_score_to_grade(total_score):
    return 'high' if total_score >= 28 else 'low'

