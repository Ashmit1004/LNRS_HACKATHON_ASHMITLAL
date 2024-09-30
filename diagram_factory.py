from diagram_generator import DiagramGenerator  # Import the DiagramGenerator class
from text_parser import extract_flow  # Import the extract_flow function

def create_diagram(diagram_type, input_text):
    # Instantiate the DiagramGenerator
    diagram_generator = DiagramGenerator()

    # Handle different diagram types and call respective methods
    if diagram_type == 'flowchart':
        conditions, actions = extract_flow(input_text)  # Extract conditions and actions
        return diagram_generator.generate_flowchart(conditions, actions)
    elif diagram_type == 'sequence':
        return diagram_generator.generate_sequence_diagram(input_text)
    elif diagram_type == 'mindmap':
        return diagram_generator.generate_mind_map(input_text)
    elif diagram_type == 'architecture':
        return diagram_generator.generate_architecture_diagram(input_text)
    elif diagram_type == 'uml':
        return diagram_generator.generate_uml_diagram(input_text)
    elif diagram_type == 'gantt':
        return diagram_generator.generate_gantt_chart(input_text)
    elif diagram_type == 'userjourney':
        return diagram_generator.generate_user_journey_map(input_text)
    else:
        raise ValueError(f"Unsupported diagram type: {diagram_type}")

# Helper function for flowchart to extract conditions and actions
def extract_flow(input_text):
    conditions = []
    actions = []
    lines = input_text.split("\n")
    for line in lines:
        if "if" in line.lower():
            conditions.append(line)
        else:
            actions.append(line)
    return conditions, actions
