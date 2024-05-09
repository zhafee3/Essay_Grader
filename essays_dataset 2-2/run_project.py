import os
import csv
from grade import parse_essay, essay_coherence, identify_grammar_errors, grammar_score, read_essay, count_sentences, count_misspelled_words, pTag, extract_topic, topic_relevance, evaluate_sentences,check_sentence_structure,relevance_Score
from score import score_spelling, score_length, map_score_to_grade, score_syntax

# Main function to process the grading for each essay
def main():
    with open('index.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            filename = row['filename']
            grade = row['grade']
            prompt = row['prompt']
            essays_folder = 'essays'
            file_path = os.path.join(essays_folder, filename)
            essay = read_essay(file_path)

            # Process essay
            doc = parse_essay(filename)

            syntax_errors = evaluate_sentences(doc)
            syntax_score = score_syntax(syntax_errors)
            #syntax score (ciii)
            #print(syntax_score)
           # print(syntax_errors)
            sentences = [str(sent) for sent in doc.sents]
            sentence_count = count_sentences(filename)
            misspell_count = count_misspelled_words(filename)
            length_score = score_length(sentence_count)
            spelling_score = score_spelling(misspell_count)
            coherence_mean, coherence_std = essay_coherence(sentences)
            # print(coherence_mean)
            # print(coherence_std)
            topicScore = topic_relevance(essay,prompt)
            relScore = relevance_Score(topicScore)
            #print(relScore)

            tagged_words = pTag(filename)
            agreement_errors, verb_tense_errors = identify_grammar_errors(tagged_words)
            grammar_score_value = grammar_score(agreement_errors, verb_tense_errors)

                            # Calculate final score and map to grade
            #final_score = 2 * length_score - spelling_score + grammar_score_value + 2 * coherence_mean + 3 * coherence_std
            final_score = 2 * length_score - spelling_score + grammar_score_value + 2 * syntax_score + 3 * relScore +coherence_std
            #print(final_score)
            grade = map_score_to_grade(final_score)

            # Output result
            print(f"Filename: {row['filename']}, Expected Grade: {row['grade']}, Calculated Grade: {grade}, Sentence Score: {length_score},Spelling Score: {spelling_score}, Grammar Score: {grammar_score_value}, Syntax Score: {syntax_score}, Relevance Score: {relScore},Total Score: {final_score}")
            #


if __name__ == "__main__":
    main()
