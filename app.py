from flask import Flask, request, render_template
from diagram_factory import create_diagram  # Import the create_diagram function

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text_input = request.form['text']  # Get user input text
        diagram_type = request.form['diagramType']  # Get selected diagram type

        # Call the diagram factory to generate the requested diagram
        diagram = create_diagram(diagram_type, text_input)

        # Save the diagram as PNG
        diagram.render('static/diagram', format='png', cleanup=True)  # Cleanup removes the .dot file

        return render_template('index.html', diagram='static/diagram.png')  # Render the output image

    return render_template('index.html', diagram=None)  # Render the empty page on GET request

if __name__ == '__main__':
    app.run(debug=True)  # Run the application in debug mode
