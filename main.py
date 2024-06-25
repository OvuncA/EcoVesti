from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from crew import EcovestiV2Crew
import threading
import uuid

# Initialize Flask APP
app = Flask(__name__)
load_dotenv()

# Configure CORS
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# In-memory storage for results
results = {}

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    else:
        # This is not used since the form is submitted via JavaScript
        return jsonify({'error': 'Invalid route for POST request'}), 400

@app.route("/analyze/", methods=['POST'])
def analyze():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'Missing URL'}), 400

    message = f"I've started the analysis for {url}"

    # Generate a unique ID for this request
    request_id = str(uuid.uuid4())
    results[request_id] = "Processing"

    # Run analysis in a separate thread (using threading or multiprocessing)
    def run_analysis_thread():
        run_analysis(url, request_id)

    analysis_thread = threading.Thread(target=run_analysis_thread)
    analysis_thread.start()

    return jsonify({'message': message, 'request_id': request_id})

@app.route("/result/<request_id>", methods=['GET'])
def get_result(request_id):
    result = results.get(request_id)
    if result is None:
        return jsonify({'error': 'Invalid request ID'}), 404
    elif result == "Processing":
        return jsonify({'status': 'Processing'}), 202
    else:
        return jsonify({'result': result})

def run_analysis(url, request_id):
    try:
        inputs = {'user_URL': url}
        crewResult = EcovestiV2Crew().crew().kickoff(inputs=inputs)

        # Save the result to the in-memory storage
        results[request_id] = crewResult
    except Exception as e:
        results[request_id] = f"An error occurred: {e}"

# Run with Flask development server (for easier debugging)
if __name__ == '__main__':
    app.run(debug=True)
