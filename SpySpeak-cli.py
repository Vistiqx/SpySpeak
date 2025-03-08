#!/usr/bin/env python3
import random
import argparse
import os
import sys
import json
import csv
from io import StringIO

def load_words(filename):
    """Load words from a file, one word per line"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            words = [line.strip() for line in file if line.strip()]
            if not words:
                sys.stderr.write(f"Warning: File '{filename}' exists but contains no usable words\n")
            return words
    except FileNotFoundError:
        sys.stderr.write(f"Error: Could not find the file '{filename}'\n")
        return []
    except Exception as e:
        sys.stderr.write(f"Error reading '{filename}': {str(e)}\n")
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
        sys.stderr.write(f"Error reading exclusions from '{filename}': {str(e)}\n")
        return []

def filter_excluded_words(words, exclusions):
    """Filter out words that are in the exclusion list"""
    if not exclusions:
        return words
    
    return [word for word in words if word.lower() not in exclusions]

def load_favorites(filename):
    """Load favorite codenames from a file"""
    if not os.path.exists(filename):
        return []
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as e:
        sys.stderr.write(f"Error loading favorites: {str(e)}\n")
        return []

def save_favorites(favorites, filename):
    """Save favorite codenames to a file"""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for name in favorites:
                file.write(f"{name}\n")
        return True
    except Exception as e:
        sys.stderr.write(f"Error saving favorites: {str(e)}\n")
        return False

def generate_codename(adjectives, nouns, count=1, separator=' ', exclusions=None,
                   pattern="adj-noun", case_style="title", min_length=0, max_length=0):
    """Generate random codenames by combining adjectives and nouns with various patterns and formats
    
    Patterns:
    - "adj-noun": Standard adjective-noun pair (default)
    - "noun-noun": Two random nouns
    - "adj-adj-noun": Two adjectives and a noun
    - "noun-adj": A noun followed by an adjective
    - "adj-noun-number": Adjective, noun, and a random number
    
    Case styles:
    - "title": Title Case (Default)
    - "upper": UPPERCASE
    - "lower": lowercase
    - "sentence": Sentence case (only first letter capitalized)
    """
    # Filter out excluded words if needed
    if exclusions:
        adjectives = filter_excluded_words(adjectives, exclusions)
        nouns = filter_excluded_words(nouns, exclusions)
    
    if not adjectives:
        sys.stderr.write("Error: No valid adjectives available after applying exclusions\n")
        sys.exit(1)
    
    if not nouns:
        sys.stderr.write("Error: No valid nouns available after applying exclusions\n")
        sys.exit(1)
    
    # Filter by length constraints if specified
    if min_length > 0:
        adjectives = [adj for adj in adjectives if len(adj) >= min_length]
        nouns = [noun for noun in nouns if len(noun) >= min_length]
    
    if max_length > 0:
        adjectives = [adj for adj in adjectives if len(adj) <= max_length]
        nouns = [noun for noun in nouns if len(noun) <= max_length]
    
    if not adjectives:
        sys.stderr.write("Error: No adjectives meet the length criteria\n")
        sys.exit(1)
    
    if not nouns:
        sys.stderr.write("Error: No nouns meet the length criteria\n")
        sys.exit(1)
    
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
            formatted_name = " ".join(word.capitalize() for word in raw_name.split(separator))
            if separator != " ":
                formatted_name = separator.join(word.capitalize() for word in raw_name.split(separator))
        
        codenames.append(formatted_name)
    
    return codenames

def format_output(codenames, format_type="text"):
    """Format codenames in various output formats"""
    if format_type == "json":
        return json.dumps({"codenames": codenames}, indent=2)
    
    elif format_type == "csv":
        output = StringIO()
        csv_writer = csv.writer(output)
        csv_writer.writerow(["Codename"])
        for name in codenames:
            csv_writer.writerow([name])
        return output.getvalue()
    
    elif format_type == "html":
        html = "<html>\n<head><title>Generated Codenames</title></head>\n<body>\n"
        html += "<h1>Generated Codenames</h1>\n<ul>\n"
        for name in codenames:
            html += f"  <li>{name}</li>\n"
        html += "</ul>\n</body>\n</html>"
        return html
    
    else:  # Default to plain text
        return "\n".join(codenames)

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

def load_themed_words(theme):
    """Load adjectives and nouns for a specific theme"""
    theme_dir = "themes"
    adj_file = os.path.join(theme_dir, f"{theme}_adj.txt")
    noun_file = os.path.join(theme_dir, f"{theme}_nouns.txt")
    
    if not os.path.exists(adj_file) or not os.path.exists(noun_file):
        sys.stderr.write(f"Theme '{theme}' not found. Make sure both {adj_file} and {noun_file} exist.\n")
        return [], []
    
    adjectives = load_words(adj_file)
    nouns = load_words(noun_file)
    
    return adjectives, nouns

def list_favorites(favorites_file):
    """List all saved favorites"""
    favorites = load_favorites(favorites_file)
    if not favorites:
        sys.stderr.write("No favorites found.\n")
        return
    
    for name in favorites:
        print(name)

def add_favorite(codename, favorites_file):
    """Add a codename to favorites"""
    favorites = load_favorites(favorites_file)
    if codename in favorites:
        sys.stderr.write(f"Codename '{codename}' is already in favorites.\n")
        return
    
    favorites.append(codename)
    if save_favorites(favorites, favorites_file):
        sys.stderr.write(f"Added '{codename}' to favorites.\n")

def export_favorites(favorites_file, output_file, format_type="text"):
    """Export favorites to a file in specified format"""
    favorites = load_favorites(favorites_file)
    if not favorites:
        sys.stderr.write("No favorites to export.\n")
        return
    
    output = format_output(favorites, format_type)
    
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(output)
        sys.stderr.write(f"Exported {len(favorites)} favorites to {output_file} in {format_type} format.\n")
    except Exception as e:
        sys.stderr.write(f"Error exporting favorites: {str(e)}\n")

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Generate random codenames from adjectives and nouns')
    
    # Basic options
    parser.add_argument('-a', '--adjectives', default='adjectives.txt', help='Path to adjectives file')
    parser.add_argument('-n', '--nouns', default='nouns.txt', help='Path to nouns file')
    parser.add_argument('-c', '--count', type=int, default=1, help='Number of codenames to generate')
    parser.add_argument('-s', '--separator', default=' ', help='Separator between adjective and noun')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show verbose output')
    
    # Output format options
    parser.add_argument('-f', '--format', choices=['text', 'json', 'csv', 'html'], default='text',
                      help='Output format (text, json, csv, or html)')
    parser.add_argument('-o', '--output', help='Output file (if not specified, prints to stdout)')
    
    # Theme options
    parser.add_argument('-t', '--theme', help='Use specific theme (themes must be in themes/ directory)')
    parser.add_argument('--list-themes', action='store_true', help='List available themes')
    
    # Exclusion options
    parser.add_argument('-e', '--exclusions', default='exclusions.txt', help='Path to exclusions file')
    
    # Pattern and formatting options
    parser.add_argument('-p', '--pattern', choices=['adj-noun', 'noun-noun', 'adj-adj-noun', 'noun-adj', 'adj-noun-number'],
                      default='adj-noun', help='Pattern for generating codenames')
    parser.add_argument('--case', choices=['title', 'upper', 'lower', 'sentence'],
                      default='title', help='Case style for generated codenames')
    parser.add_argument('--min-length', type=int, default=0, 
                      help='Minimum length for words (0 for no minimum)')
    parser.add_argument('--max-length', type=int, default=0,
                      help='Maximum length for words (0 for no maximum)')
    
    # Favorites options
    parser.add_argument('--favorites', default='favorites.txt', help='Path to favorites file')
    parser.add_argument('--list-favorites', action='store_true', help='List saved favorites')
    parser.add_argument('--add-favorite', help='Add a codename to favorites')
    parser.add_argument('--export-favorites', help='Export favorites to a file')
    
    args = parser.parse_args()
    
    # Create themes directory if it doesn't exist
    if not os.path.exists("themes"):
        if args.verbose:
            sys.stderr.write("Creating themes directory...\n")
        os.makedirs("themes", exist_ok=True)
    
    # List themes and exit if requested
    if args.list_themes:
        themes = get_available_themes()
        if not themes:
            sys.stderr.write("No themes available. Create theme files in the themes/ directory.\n")
        else:
            sys.stderr.write("Available themes:\n")
            for theme in themes:
                sys.stderr.write(f"- {theme}\n")
        return
    
    # List favorites and exit if requested
    if args.list_favorites:
        list_favorites(args.favorites)
        return
    
    # Add to favorites and exit if requested
    if args.add_favorite:
        add_favorite(args.add_favorite, args.favorites)
        return
    
    # Export favorites and exit if requested
    if args.export_favorites:
        export_format = args.format
        export_favorites(args.favorites, args.export_favorites, export_format)
        return
    
    # Resolve file paths for the main functionality
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load words based on theme or default files
    if args.theme:
        if args.verbose:
            sys.stderr.write(f"Loading theme '{args.theme}'...\n")
        adjectives, nouns = load_themed_words(args.theme)
        if not adjectives or not nouns:
            sys.exit(1)
    else:
        adj_path = os.path.join(script_dir, args.adjectives) if not os.path.isabs(args.adjectives) else args.adjectives
        noun_path = os.path.join(script_dir, args.nouns) if not os.path.isabs(args.nouns) else args.nouns
        
        # Display paths for debugging if verbose
        if args.verbose:
            sys.stderr.write(f"Loading adjectives from: {adj_path}\n")
            sys.stderr.write(f"Loading nouns from: {noun_path}\n")
        
        # Check if files exist
        if not os.path.exists(adj_path):
            sys.stderr.write(f"Error: Adjectives file '{adj_path}' not found.\n")
            sys.exit(1)
        
        if not os.path.exists(noun_path):
            sys.stderr.write(f"Error: Nouns file '{noun_path}' not found.\n")
            sys.exit(1)
        
        # Load word lists
        adjectives = load_words(adj_path)
        nouns = load_words(noun_path)
    
    # Load exclusions if specified
    exclusions = []
    if os.path.exists(args.exclusions):
        exclusions = load_exclusions(args.exclusions)
        if args.verbose and exclusions:
            sys.stderr.write(f"Loaded {len(exclusions)} exclusions\n")
    
    # Verify we have words
    if not adjectives:
        sys.stderr.write("Error: No adjectives loaded. Please check your adjectives file.\n")
        sys.exit(1)
    
    if not nouns:
        sys.stderr.write("Error: No nouns loaded. Please check your nouns file.\n")
        sys.exit(1)
    
    if args.verbose:
        sys.stderr.write(f"Loaded {len(adjectives)} adjectives and {len(nouns)} nouns\n")
    
    # Verify count is valid
    if args.count < 1:
        sys.stderr.write("Error: Count must be at least 1\n")
        sys.exit(1)
    
    # Validate word length restrictions
    if args.min_length > 0 and args.max_length > 0 and args.min_length > args.max_length:
        sys.stderr.write("Error: Minimum length cannot be greater than maximum length\n")
        sys.exit(1)
    
    # Generate codenames
    try:
        codenames = generate_codename(
            adjectives=adjectives, 
            nouns=nouns, 
            count=args.count, 
            separator=args.separator, 
            exclusions=exclusions,
            pattern=args.pattern,
            case_style=args.case,
            min_length=args.min_length,
            max_length=args.max_length
        )
        
        # Format output
        output = format_output(codenames, args.format)
        
        # Output to file or stdout
        if args.output:
            try:
                with open(args.output, 'w', encoding='utf-8') as file:
                    file.write(output)
                if args.verbose:
                    sys.stderr.write(f"Output written to {args.output}\n")
            except Exception as e:
                sys.stderr.write(f"Error writing to output file: {str(e)}\n")
                sys.exit(1)
        else:
            # Print to stdout
            print(output, end='')
    
    except Exception as e:
        sys.stderr.write(f"Error generating codenames: {str(e)}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()