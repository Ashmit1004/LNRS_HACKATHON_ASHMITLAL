import re
from graphviz import Digraph  # Ensure to import Graphviz
import spacy

# Load the spaCy model for dependency parsing and entity recognition
nlp = spacy.load("en_core_web_sm")

class DiagramGenerator:
    def generate_flowchart(self, conditions, actions):
        dot = Digraph('Flowchart')
        
        for i, condition in enumerate(conditions):
            dot.node(f'condition_{i}', condition, shape='diamond')

        for i, action in enumerate(actions):
            dot.node(f'action_{i}', action, shape='box')

        for i in range(len(conditions)):
            if i < len(actions):
                dot.edge(f'condition_{i}', f'action_{i}', label='then')

        return dot  # Return the Graphviz object

    def generate_sequence_diagram(self, input_text):
        dot = Digraph('Sequence Diagram')
        
        # Define participants dynamically
        participants = set()
        
        # Split input into lines
        lines = input_text.split("\n")
        
        for line in lines:
            line = line.strip()
            if "sends" in line:
                parts = re.split(r'\s+sends\s+', line)
                if len(parts) == 2:
                    sender, receiver_action = parts[0], parts[1]
                    receiver_parts = receiver_action.split("to")
                    if len(receiver_parts) == 2:
                        receiver = receiver_parts[0].strip()
                        action = receiver_parts[1].strip()
                        participants.update([sender.strip(), receiver])
                        dot.node(sender.strip(), shape='rect')
                        dot.node(receiver.strip(), shape='rect')
                        dot.edge(sender.strip(), receiver.strip(), label=action)

        # Add nodes for all unique participants
        for participant in participants:
            dot.node(participant.strip(), participant.strip())

        return dot  # Return the Graphviz object

    def generate_gantt_chart(self, input_text):
        tasks = input_text.split("\n")
        dot = Digraph('Gantt Chart')
        dot.node('Project', 'Project starts at 2023-01-01', shape='box')

        for i, task in enumerate(tasks):
            task = task.strip()
            dot.node(f'task_{i}', f'{task}', shape='box')
            dot.edge('Project', f'task_{i}', label='starts')

        return dot  # Return the Graphviz object

    def generate_mind_map(self, input_text):
        lines = input_text.split("\n")
        dot = Digraph('Mind Map')
        
        main_topic = ""
        subtopic_parent = None
        
        for line in lines:
            line = line.strip()
            if "Main Topic:" in line:
                main_topic = line.split("Main Topic:")[1].strip()
                dot.node('root', main_topic, shape='ellipse')
                subtopic_parent = 'root'
            elif "Subtopics:" in line:
                subtopics = line.split(":")[1].strip().split(", ")
                for subtopic in subtopics:
                    subtopic_cleaned = subtopic.strip()
                    dot.node(subtopic_cleaned, subtopic_cleaned, shape='ellipse')
                    dot.edge(subtopic_parent, subtopic_cleaned)
                    subtopic_parent = subtopic_cleaned 
            else:
                # Handle additional lines as subtopics or branches
                if subtopic_parent:
                    dot.node(line, line, shape='ellipse')
                    dot.edge(subtopic_parent, line)

        return dot  # Return the Graphviz object

    def generate_architecture_diagram(self, input_text):
        lines = input_text.split("\n")
        dot = Digraph('Architecture Diagram')
        components = []
        flows = []

        for line in lines:
            if "Components:" in line:
                components = line.split(":")[1].strip().split(", ")
            elif "Flows:" in line:
                flows.append(line)

        for component in components:
            dot.node(component.strip(), component.strip(), shape='rectangle')

        for flow in flows:
            parts = re.split(r'\sconnects\sto\s', flow)
            if len(parts) == 2:
                sender, receiver = parts
                dot.edge(sender.strip(), receiver.strip())

        return dot  # Return the Graphviz object

    def generate_uml_diagram(self, input_text):
        lines = input_text.split("\n")
        dot = Digraph('UML Diagram')
        
        for line in lines:
            if "Classes:" in line:
                classes = line.split(":")[1].strip().split(", ")
                for class_info in classes:
                    if ':' in class_info:  # Check if ':' is present
                        class_name, methods = class_info.split(":")
                        methods_list = methods.strip().split(", ")
                        dot.node(class_name.strip(), class_name.strip(), shape='record')
                        for method in methods_list:
                            method_cleaned = method.strip()
                            if method_cleaned:  # Ensure method is not empty
                                method_node_name = f'{class_name.strip()}_{method_cleaned}'
                                dot.node(method_node_name, method_cleaned, shape='record')
                                dot.edge(class_name.strip(), method_node_name, label='has method')
                    else:
                        dot.node(class_info.strip(), class_info.strip(), shape='record')  # Handle classes without methods

        return dot  # Return the Graphviz object

    def generate_user_journey_map(self, input_text):
        lines = input_text.split("\n")
        dot = Digraph('User Journey Map')

        dot.node('start', 'Start')
        previous_phase = 'start'
        
        phases = []
        actions = []

        for line in lines:
            if "Phases:" in line:
                phases = line.split(":")[1].strip().split(", ")
            elif "Actions:" in line:
                actions = line.split(":")[1].strip().split(", ")
        
            for phase in phases:
                phase_cleaned = phase.strip()
                dot.node(phase_cleaned, phase_cleaned)
                dot.edge(previous_phase, phase_cleaned)
                previous_phase = phase_cleaned
            
            for i, action in enumerate(actions):
                if i < len(phases):
                    action_cleaned = action.strip()
                    dot.node(f'action_{i}', action_cleaned)
                    dot.edge(phases[i].strip(), f'action_{i}', label='Action')

        dot.edge(previous_phase, 'end', label='End')
        
        return dot  # Return the Graphviz object

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