"""
Flask application with agent pipeline orchestration.
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv

from agents import GeneratorAgent, ReviewerAgent, GeneratorInput, PipelineResponse
from utils import LLMClient

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='ui', static_url_path='')
CORS(app)  # Enable CORS for frontend-backend communication

# Initialize LLM client and agents
llm_client = LLMClient()
generator = GeneratorAgent(llm_client)
reviewer = ReviewerAgent(llm_client)

# Maximum refinement attempts (per assessment requirements)
MAX_REFINEMENT_ATTEMPTS = 1


@app.route('/')
def index():
    """Serve the main UI."""
    return send_from_directory('ui', 'index.html')


@app.route('/api/generate', methods=['POST'])
def generate_content():
    """
    Generate educational content with agent pipeline.
    
    Request Body:
        {
            "grade": int (1-12),
            "topic": str
        }
    
    Response:
        {
            "generator_output": {...},
            "reviewer_feedback": {...},
            "final_output": {...},
            "refinement_occurred": bool
        }
    """
    try:
        # Validate input
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Create and validate input
        try:
            input_data = GeneratorInput(
                grade=data.get('grade'),
                topic=data.get('topic')
            )
        except Exception as e:
            return jsonify({"error": f"Invalid input: {str(e)}"}), 400
        
        # Step 1: Generate initial content
        print(f"[Generator] Creating content for Grade {input_data.grade}: {input_data.topic}")
        generator_output = generator.generate(input_data)
        
        # Step 2: Review content
        print(f"[Reviewer] Evaluating content...")
        reviewer_feedback = reviewer.evaluate(
            grade=input_data.grade,
            topic=input_data.topic,
            content=generator_output
        )
        
        # Step 3: Refine if needed (max 1 attempt)
        refinement_occurred = False
        final_output = generator_output
        
        if reviewer_feedback.status == "fail":
            print(f"[Reviewer] Content failed review. Refining...")
            
            # Create refinement input with feedback
            refinement_input = GeneratorInput(
                grade=input_data.grade,
                topic=input_data.topic,
                feedback=reviewer_feedback.feedback
            )
            
            # Generate refined content
            final_output = generator.generate(refinement_input)
            refinement_occurred = True
            print(f"[Generator] Refinement complete")
        else:
            print(f"[Reviewer] Content passed review")
        
        # Build response
        response = PipelineResponse(
            generator_output=generator_output,
            reviewer_feedback=reviewer_feedback,
            final_output=final_output,
            refinement_occurred=refinement_occurred
        )
        
        return jsonify(response.model_dump()), 200
        
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"Starting Ekalavya Agent on http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
