import json

# Function to remove '1.' from the string
def remove_one_and_two(text):
    # Replace '1.'  empty strings
    return text.replace("1.", "").strip()


# Function to remove content after '2.' in the string
def truncate_after_two(text):
    # Look for the substring "\n2" and cut off anything after it
    if "2." in text:
        return text.split("2.")[0].strip()
    return text

def truncate_after_newline(text):
    # Look for the substring "\n" and cut off anything after it
    if "\n" in text:
        return text.split("\n")[0].strip()
    return text

# Function to clean up text (removing only tabs)
def remove_tabs(text):
    # Replace tabs with nothing (remove them)
    return text.replace("\t", "")

# Function to convert triple data into readable sentences
def convert_to_text(triple):
    # Clean and truncate the head and tail fields
    head = truncate_after_newline(remove_tabs(truncate_after_two(triple["Head"].strip().replace("**", "").replace("1.", "").replace(".", ""))))
    relation = truncate_after_newline(remove_tabs(triple["Relation"].strip().replace("**", "")))  # Clean relation text
    tail = truncate_after_newline(remove_tabs(truncate_after_two(triple["Tail"].strip().replace("**", "").replace("\n", " ").replace("1.", "").replace(".", ""))))   
    # Handle specific relations for sentence construction
    
    if relation == "xIntent":
        return f"Why does someone {head}? The intention is {tail}."
    elif relation == "Causal":
        return f"What is the result of {head}? The cause is {tail}."
    elif relation == "xEffect":
        return f"What happens as a result of {head}? The effect is {tail}."
    elif relation == "xReason":
        return f"Why did {head} happen? The reason is {tail}."
    elif relation == "xAttr":
        return f"What can be described about {head}? It is characterized as {tail}."
    elif relation == "xWant":
        return f"What does someone want after {head}? The desire is {tail}."
    elif relation == "oEffect":
        return f"What happens to others as a result of {head}? The effect is {tail}."
    elif relation == "oWant":
        return f"What do others want after {head}? They want {tail}."
    elif relation == "Instrumental":
        return f"How is {head} achieved? It is done through {tail}."
    elif relation == "AtLocation":
        return f"Where does {head} happen? It happens at {tail}."
    elif relation == "HasProperty":
        return f"What property does {head} have? It has the property of {tail}."
    elif relation == "CapableOf":
        return f"What is {head} capable of? It is capable of {tail}."
    elif relation == "MadeUpOf":
        return f"What is {head} made up of? It is made up of {tail}."
    elif relation == "Similar":
        return f"What is similar to {head}? It is similar to {tail}."
    elif relation in ["Partwhole", "PartWhole Relations"]:
        return f"What is {head} a part of? It is part of {tail}."
    elif relation == "Cause and Effect":
        return f"What is the effect of {head}? The effect is {tail}."
    elif relation == "Sequential":
        return f"What happens after {head}? The next step is {tail}."
    elif relation in ["Subevent", "HasSubEvent"]:
        return f"What is a subevent of {head}? The subevent is {tail}."
    elif relation == "Temporal":
        return f"When does {head} happen? It happens during {tail}."
    elif relation == "Conditional":
        return f"Under what condition does {head} happen? It happens if {tail}."
    elif relation == "Analogous":
        return f"What is analogous to {head}? It is analogous to {tail}."
    elif relation == "Contrast":
        return f"How does {head} contrast with {tail}? They are contrasting because {tail}."
    elif relation == "Purpose":
        return f"What is the purpose of {head}? The purpose is {tail}."
    elif relation == "Clarification":
        return f"How is {head} clarified? It is clarified by {tail}."
    elif relation == "Explanation":
        return f"Why does {head} happen? It happens because {tail}."
    elif relation == "Supportive":
        return f"How is {head} supported? It is supported by {tail}."
    elif relation == "Definition":
        return f"How is {head} defined? It is defined as {tail}."
    elif relation == "Synonym":
        return f"What is another word for {head}? A synonym is {tail}."
    elif relation == "Antonym":
        return f"What is the opposite of {head}? The antonym is {tail}."
    elif relation == "Prerequisite":
        return f"What needs to happen before {head}? The prerequisite is {tail}."
    elif relation == "Dependent":
        return f"What depends on {head}? It depends on {tail}."
    elif relation == "Mitigates":
        return f"How does {head} mitigate {tail}? It mitigates it by {tail}."
    elif relation == "IsBefore":
        return f"What happens before {head}? It happens before {tail}."
    elif relation == "IsAfter":
        return f"What happens after {head}? It happens after {tail}."
    elif relation == "Complementary":
        return f"What complements {head}? It is complemented by {tail}."
    elif relation == "Component":
        return f"What is a component of {head}? It is part of {tail}."
    elif relation == "Subset":
        return f"What is {head} a subset of? It is a subset of {tail}."
    elif relation == "Hierarchical":
        return f"What hierarchy is {head} part of? It belongs to the hierarchy of {tail}."
    elif relation == "Interdependent":
        return f"How is {head} interdependent with {tail}? They are interdependent because {tail}."
    elif relation == "Subordinate":
        return f"What is subordinate to {head}? It is subordinate to {tail}."
    elif relation == "Topical":
        return f"What topic is {head} related to? It is related to the topic of {tail}."
    elif relation == "Logical":
        return f"How is {head} logically connected? It is logically related to {tail}."
    elif relation == "Causal Chain":
        return f"What is part of the causal chain with {head}? It is causally connected to {tail}."
    
    # Default pattern if no specific relation is matched
    else:
        return f"{head} and {tail} are connected by {relation} ."

# Load the dataset
with open("cleaned_triples.json", "r") as f:
    triples = json.load(f)

# Convert the triples to text
text_data = [convert_to_text(triple) for triple in triples]

# Display the first few converted texts
for text in text_data[:10]:
    print(text)

# Save the processed text data
with open("converted_text_data.txt", "w") as f:
    for text in text_data:
        f.write(text + "\n")
