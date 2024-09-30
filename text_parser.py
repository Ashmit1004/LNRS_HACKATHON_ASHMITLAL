import spacy

# Load the spaCy model for dependency parsing and entity recognition
nlp = spacy.load("en_core_web_sm")

def extract_flow(text):
    doc = nlp(text)
    conditions = []
    actions = []

    # Loop over each sentence, identifying conditions and actions
    for sent in doc.sents:
        if any(token.text.lower() in ["if", "when"] for token in sent):
            conditions.append(sent.text.strip())
        else:
            actions.append(sent.text.strip())

    return conditions, actions

# Example usage
if __name__ == "__main__":
    text = "If the user clicks the submit button, show the confirmation page."
    conditions, actions = extract_flow(text)
    print("Conditions:", conditions)
    print("Actions:", actions)