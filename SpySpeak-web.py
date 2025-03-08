from flask import Flask, render_template, request, jsonify, send_from_directory
import random
import os
import json
import sys

# Add the current directory to the path so we can import our codename functions
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

# -------------------- Utility Functions ---------------------

def load_words(filename):
    """Load words from a file, one word per line"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            words = [line.strip() for line in file if line.strip()]
            return words
    except FileNotFoundError:
        app.logger.error(f"Error: Could not find the file '{filename}'")
        return []
    except Exception as e:
        app.logger.error(f"Error reading '{filename}': {str(e)}")
        return []

def load_exclusions(filename):
    """Load exclusion words from a file"""
    if not os.path.exists(filename):
        return []
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            words = [line.strip().lower() for line in file if line.strip()]
            return words
    except Exception as e:
        app.logger.error(f"Error reading exclusions from '{filename}': {str(e)}")
        return []

def filter_excluded_words(words, exclusions):
    """Filter out words that are in the exclusion list"""
    if not exclusions:
        return words
    
    return [word for word in words if word.lower() not in exclusions]

def load_themed_words(theme):
    """Load adjectives and nouns for a specific theme"""
    theme_dir = "themes"
    adj_file = os.path.join(theme_dir, f"{theme}_adj.txt")
    noun_file = os.path.join(theme_dir, f"{theme}_nouns.txt")
    
    if not os.path.exists(adj_file) or not os.path.exists(noun_file):
        app.logger.error(f"Theme '{theme}' not found. Make sure both {adj_file} and {noun_file} exist.")
        return [], []
    
    adjectives = load_words(adj_file)
    nouns = load_words(noun_file)
    
    return adjectives, nouns

def get_available_themes():
    """Get list of available themes from themes directory"""
    themes = []
    if not os.path.exists("themes"):
        return themes
    
    for item in os.listdir("themes"):
        if item.endswith("_adj.txt"):
            theme_name = item.replace("_adj.txt", "")
            # Check if corresponding noun file exists
            if os.path.exists(os.path.join("themes", f"{theme_name}_nouns.txt")):
                themes.append(theme_name)
    
    return themes

def generate_codename(adjectives, nouns, count=1, separator=' ', exclusions=None,
                     pattern="adj-noun", case_style="title", min_length=0, max_length=0):
    """Generate random codenames by combining adjectives and nouns with various patterns and formats"""
    # Filter out excluded words if needed
    if exclusions:
        adjectives = filter_excluded_words(adjectives, exclusions)
        nouns = filter_excluded_words(nouns, exclusions)
    
    if not adjectives:
        return {"error": "No valid adjectives available after applying exclusions"}
    
    if not nouns:
        return {"error": "No valid nouns available after applying exclusions"}
    
    # Filter by length constraints if specified
    if min_length > 0:
        adjectives = [adj for adj in adjectives if len(adj) >= min_length]
        nouns = [noun for noun in nouns if len(noun) >= min_length]
    
    if max_length > 0:
        adjectives = [adj for adj in adjectives if len(adj) <= max_length]
        nouns = [noun for noun in nouns if len(noun) <= max_length]
    
    if not adjectives:
        return {"error": "No adjectives meet the length criteria"}
    
    if not nouns:
        return {"error": "No nouns meet the length criteria"}
    
    codenames = []
    for _ in range(count):
        # Generate based on pattern
        if pattern == "adj-noun":
            adj = random.choice(adjectives)
            noun = random.choice(nouns)
            raw_name = f"{adj}{separator}{noun}"
        elif pattern == "noun-noun":
            noun1 = random.choice(nouns)
            noun2 = random.choice(nouns)
            raw_name = f"{noun1}{separator}{noun2}"
        elif pattern == "adj-adj-noun":
            adj1 = random.choice(adjectives)
            adj2 = random.choice(adjectives)
            noun = random.choice(nouns)
            raw_name = f"{adj1}{separator}{adj2}{separator}{noun}"
        elif pattern == "noun-adj":
            noun = random.choice(nouns)
            adj = random.choice(adjectives)
            raw_name = f"{noun}{separator}{adj}"
        elif pattern == "adj-noun-number":
            adj = random.choice(adjectives)
            noun = random.choice(nouns)
            number = random.randint(1, 999)
            raw_name = f"{adj}{separator}{noun}{separator}{number}"
        else:
            # Default to adj-noun if pattern is not recognized
            adj = random.choice(adjectives)
            noun = random.choice(nouns)
            raw_name = f"{adj}{separator}{noun}"
        
        # Apply case style
        if case_style == "upper":
            formatted_name = raw_name.upper()
        elif case_style == "lower":
            formatted_name = raw_name.lower()
        elif case_style == "sentence":
            formatted_name = raw_name.capitalize()
        else:  # Default to title case
            if separator == " ":
                formatted_name = " ".join(word.capitalize() for word in raw_name.split())
            else:
                formatted_name = separator.join(word.capitalize() for word in raw_name.split(separator))
        
        codenames.append(formatted_name)
    
    return codenames

# -------------------- Route Handlers ---------------------

@app.route('/')
def index():
    """Render the main web interface"""
    themes = get_available_themes()
    return render_template('index.html', themes=themes)

@app.route('/generate', methods=['POST'])
def generate():
    """Handle form submission from web interface"""
    try:
        # Get form data
        count = int(request.form.get('count', 1))
        theme = request.form.get('theme', 'default')
        pattern = request.form.get('pattern', 'adj-noun')
        case_style = request.form.get('case', 'title')
        separator = request.form.get('separator', ' ')
        min_length = int(request.form.get('min_length', 0))
        max_length = int(request.form.get('max_length', 0))
        
        # Load words
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        if theme != 'default':
            adjectives, nouns = load_themed_words(theme)
        else:
            adj_file = os.path.join(current_dir, "adjectives.txt")
            noun_file = os.path.join(current_dir, "nouns.txt")
            adjectives = load_words(adj_file)
            nouns = load_words(noun_file)
        
        # Load exclusions if they exist
        exclusions_file = os.path.join(current_dir, "exclusions.txt")
        exclusions = load_exclusions(exclusions_file) if os.path.exists(exclusions_file) else []
        
        # Generate codenames
        codenames = generate_codename(
            adjectives=adjectives,
            nouns=nouns,
            count=count,
            separator=separator,
            exclusions=exclusions,
            pattern=pattern,
            case_style=case_style,
            min_length=min_length,
            max_length=max_length
        )
        
        # Check if there was an error
        if isinstance(codenames, dict) and 'error' in codenames:
            return render_template('index.html', 
                                  error=codenames['error'],
                                  themes=get_available_themes())
        
        return render_template('index.html', 
                              codenames=codenames, 
                              count=count,
                              theme=theme,
                              pattern=pattern,
                              case=case_style,
                              separator=separator,
                              min_length=min_length,
                              max_length=max_length,
                              themes=get_available_themes())
    
    except Exception as e:
        app.logger.error(f"Error generating codenames: {str(e)}")
        return render_template('index.html', 
                              error=f"Error generating codenames: {str(e)}",
                              themes=get_available_themes())

@app.route('/api/codenames', methods=['GET'])
def api_generate():
    """REST API endpoint for generating codenames"""
    try:
        # Get query parameters
        count = int(request.args.get('count', 1))
        theme = request.args.get('theme', 'default')
        pattern = request.args.get('pattern', 'adj-noun')
        case_style = request.args.get('case', 'title')
        separator = request.args.get('separator', ' ')
        min_length = int(request.args.get('min_length', 0))
        max_length = int(request.args.get('max_length', 0))
        
        # Load words
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        if theme != 'default':
            adjectives, nouns = load_themed_words(theme)
        else:
            adj_file = os.path.join(current_dir, "adjectives.txt")
            noun_file = os.path.join(current_dir, "nouns.txt")
            adjectives = load_words(adj_file)
            nouns = load_words(noun_file)
        
        # Load exclusions if they exist
        exclusions_file = os.path.join(current_dir, "exclusions.txt")
        exclusions = load_exclusions(exclusions_file) if os.path.exists(exclusions_file) else []
        
        # Generate codenames
        codenames = generate_codename(
            adjectives=adjectives,
            nouns=nouns,
            count=count,
            separator=separator,
            exclusions=exclusions,
            pattern=pattern,
            case_style=case_style,
            min_length=min_length,
            max_length=max_length
        )
        
        # Check if there was an error
        if isinstance(codenames, dict) and 'error' in codenames:
            return jsonify({
                'success': False,
                'error': codenames['error']
            }), 400
        
        return jsonify({
            'success': True,
            'codenames': codenames,
            'count': count,
            'theme': theme,
            'pattern': pattern,
            'case': case_style,
            'separator': separator,
            'min_length': min_length,
            'max_length': max_length
        })
    
    except Exception as e:
        app.logger.error(f"API error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/themes', methods=['GET'])
def api_themes():
    """REST API endpoint for listing available themes"""
    themes = get_available_themes()
    return jsonify({
        'success': True,
        'themes': themes
    })

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Create the necessary directories when the server starts
def create_required_directories():
    """Create themes directory if it doesn't exist"""
    os.makedirs("themes", exist_ok=True)
    os.makedirs("static", exist_ok=True)
    os.makedirs("templates", exist_ok=True)

if __name__ == '__main__':
    create_required_directories()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)