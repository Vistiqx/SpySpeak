import random
import os
import json
import csv
import sys
from io import StringIO

def load_words(filename):
    """
    Load words from a file, one word per line
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: Could not find the file '{filename}'")
        return []

def save_favorites(favorites, filename="favorites.txt"):
    """
    Save favorite codenames to a file
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for name in favorites:
                file.write(f"{name}\n")
        print(f"Successfully saved {len(favorites)} favorites to {filename}")
        return True
    except Exception as e:
        print(f"Error saving favorites: {str(e)}")
        return False

def load_favorites(filename="favorites.txt"):
    """
    Load favorite codenames from a file
    """
    if not os.path.exists(filename):
        print(f"No favorites file found at {filename}")
        return []
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(f"Error loading favorites: {str(e)}")
        return []

def load_exclusions(filename="exclusions.txt"):
    """
    Load exclusion words from a file
    """
    if not os.path.exists(filename):
        return []
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return [line.strip().lower() for line in file if line.strip()]
    except Exception as e:
        print(f"Error loading exclusions: {str(e)}")
        return []

def get_available_themes():
    """
    Get list of available themes from themes directory
    """
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
    """
    Load adjectives and nouns for a specific theme
    """
    theme_dir = "themes"
    adj_file = os.path.join(theme_dir, f"{theme}_adj.txt")
    noun_file = os.path.join(theme_dir, f"{theme}_nouns.txt")
    
    if not os.path.exists(adj_file) or not os.path.exists(noun_file):
        print(f"Theme '{theme}' not found. Make sure both {adj_file} and {noun_file} exist.")
        return [], []
    
    adjectives = load_words(adj_file)
    nouns = load_words(noun_file)
    
    return adjectives, nouns

def filter_excluded_words(words, exclusions):
    """
    Filter out words that are in the exclusion list
    """
    if not exclusions:
        return words
    
    return [word for word in words if word.lower() not in exclusions]

def generate_codename(adjectives, nouns, count=1, exclusions=None, pattern="adj-noun", 
                 case_style="title", min_length=0, max_length=0, separator=" "):
    """
    Generate random codenames by combining adjectives and nouns
    with customizable patterns, case styles, and length constraints.
    
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
    
    Length constraints:
    - min_length: Minimum total characters (0 = no minimum)
    - max_length: Maximum total characters (0 = no maximum)
    """
    if not adjectives or not nouns:
        return ["Could not generate codename due to missing word lists"]
    
    # Filter out excluded words if needed
    if exclusions:
        adjectives = filter_excluded_words(adjectives, exclusions)
        nouns = filter_excluded_words(nouns, exclusions)
        
        if not adjectives or not nouns:
            return ["Could not generate codename: all words were excluded"]
    
    # Filter by length constraints if specified
    if min_length > 0:
        adjectives = [adj for adj in adjectives if len(adj) >= min_length]
        nouns = [noun for noun in nouns if len(noun) >= min_length]
    
    if max_length > 0:
        adjectives = [adj for adj in adjectives if len(adj) <= max_length]
        nouns = [noun for noun in nouns if len(noun) <= max_length]
    
    if not adjectives or not nouns:
        return ["Could not generate codename: no words meet the length criteria"]
    
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
    """
    Format codenames in various output formats
    """
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

def export_favorites(favorites, format_type, filename=None):
    """
    Export favorites in various formats
    """
    output = format_output(favorites, format_type)
    
    if filename:
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(output)
            print(f"Successfully exported {len(favorites)} favorites to {filename}")
        except Exception as e:
            print(f"Error exporting favorites: {str(e)}")
    
    return output

def display_help():
    """
    Display help information
    """
    print("\nCodename Generator Help:")
    print("-----------------------")
    print("Main Menu Options:")
    print("1. Generate a single codename - Creates one random codename")
    print("2. Generate multiple codenames - Creates multiple codenames")
    print("3. View favorites - Display your saved favorite codenames")
    print("4. Manage favorites - Add to, remove from, or export your favorites")
    print("5. Change settings - Modify application settings like theme or exclusions")
    print("6. Help - Display this help information")
    print("7. Exit - Quit the application")
    
    print("\nThemes:")
    print("The program supports themed word lists found in the 'themes' directory.")
    print("Each theme consists of two files: themename_adj.txt and themename_nouns.txt")
    
    print("\nExclusions:")
    print("You can create an 'exclusions.txt' file with words to exclude from codename generation.")
    print("Put one word per line in this file.")
    
    print("\nOutput Formats:")
    print("Codenames can be exported in text, JSON, CSV, and HTML formats.")
    
    print("\nCodename Patterns:")
    print("- adj-noun: Adjective + Noun (e.g., 'Brave Tiger')")
    print("- noun-noun: Noun + Noun (e.g., 'Forest Mountain')")
    print("- adj-adj-noun: Adjective + Adjective + Noun (e.g., 'Brave Silent Warrior')")
    print("- noun-adj: Noun + Adjective (e.g., 'Eagle Swift')")
    print("- adj-noun-number: Adjective + Noun + Number (e.g., 'Swift Eagle 42')")
    
    print("\nCase Styles:")
    print("- Title Case: First Letter Of Each Word Capitalized")
    print("- UPPERCASE: ALL LETTERS CAPITALIZED")
    print("- lowercase: all letters lowercase")
    print("- Sentence case: Only first letter capitalized")
    
    print("\nWord Length Limits:")
    print("You can set minimum and maximum length for words used in codenames.")
    print("This helps control the overall length of generated codenames.")
    
    print("\nSeparators:")
    print("You can choose different separators between words: space, hyphen, underscore, etc.")

def main():
    # Initialize variables
    favorites = []
    exclusions = []
    current_theme = None
    
    # Default configuration
    pattern = "adj-noun"
    case_style = "title"
    min_length = 0
    max_length = 0
    separator = " "
    
    # File paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    adj_file = os.path.join(current_dir, "adjectives.txt")
    noun_file = os.path.join(current_dir, "nouns.txt")
    exclusions_file = os.path.join(current_dir, "exclusions.txt")
    
    # Create themes directory if it doesn't exist
    themes_dir = os.path.join(current_dir, "themes")
    if not os.path.exists(themes_dir):
        os.makedirs(themes_dir)
        print(f"Created themes directory at {themes_dir}")
        print("You can add themed word lists in this directory.")
    
    # Check if files exist
    if not os.path.exists(adj_file):
        print(f"Error: '{adj_file}' not found. Please make sure the file exists in the current directory.")
        return
    
    if not os.path.exists(noun_file):
        print(f"Error: '{noun_file}' not found. Please make sure the file exists in the current directory.")
        return
    
    # Load word lists
    print("Loading word lists...")
    adjectives = load_words(adj_file)
    nouns = load_words(noun_file)
    
    if not adjectives:
        print(f"Error: No adjectives loaded from {adj_file}")
        return
        
    if not nouns:
        print(f"Error: No nouns loaded from {noun_file}")
        return
    
    # Load exclusions if they exist
    if os.path.exists(exclusions_file):
        exclusions = load_exclusions(exclusions_file)
        print(f"Loaded {len(exclusions)} excluded words")
        
        # Apply exclusions
        adjectives = filter_excluded_words(adjectives, exclusions)
        nouns = filter_excluded_words(nouns, exclusions)
    
    # Load favorites if they exist
    favorites_file = os.path.join(current_dir, "favorites.txt")
    if os.path.exists(favorites_file):
        favorites = load_favorites(favorites_file)
        print(f"Loaded {len(favorites)} favorites")
    
    print(f"Loaded {len(adjectives)} adjectives and {len(nouns)} nouns")
    
    # Generate a sample codename immediately to verify functionality
    sample_codename = generate_codename(adjectives, nouns)[0]
    print(f"Sample codename: {sample_codename}")
    
    # Basic UI loop
    while True:
        try:
            print("\nCodename Generator Options:")
            print("1. Generate a single codename")
            print("2. Generate multiple codenames")
            print("3. View favorites")
            print("4. Manage favorites")
            print("5. Change settings")
            print("6. Help")
            print("7. Exit")
            
            choice = input("Enter your choice (1-7): ")
            
            if choice == '1':
                # Generate a single codename with current settings
                codename = generate_codename(
                    adjectives, nouns, 
                    pattern=pattern, 
                    case_style=case_style, 
                    min_length=min_length, 
                    max_length=max_length, 
                    separator=separator,
                    exclusions=exclusions
                )[0]
                print(f"\nYour codename is: {codename}")
                
                # Ask if user wants to save to favorites
                save_choice = input("Add this to favorites? (y/n): ").lower()
                if save_choice == 'y':
                    favorites.append(codename)
                    save_favorites(favorites, favorites_file)
            
            elif choice == '2':
                try:
                    count = int(input("How many codenames do you want to generate? "))
                    if count < 1:
                        print("Please enter a positive number")
                        continue
                    
                    format_type = "text"
                    format_choice = input("Output format (text/json/csv/html) [text]: ").lower()
                    if format_choice in ['json', 'csv', 'html']:
                        format_type = format_choice
                        
                    codenames = generate_codename(
                        adjectives, nouns, count,
                        pattern=pattern, 
                        case_style=case_style, 
                        min_length=min_length, 
                        max_length=max_length, 
                        separator=separator,
                        exclusions=exclusions
                    )
                    
                    # Format and display according to chosen format
                    output = format_output(codenames, format_type)
                    print("\nYour codenames are:")
                    print(output)
                    
                    # Ask if user wants to save to a file
                    save_choice = input("Save output to file? (y/n): ").lower()
                    if save_choice == 'y':
                        filename = input("Enter filename: ")
                        try:
                            with open(filename, 'w', encoding='utf-8') as file:
                                file.write(output)
                            print(f"Output saved to {filename}")
                        except Exception as e:
                            print(f"Error saving file: {str(e)}")
                    
                except ValueError:
                    print("Please enter a valid number")
            
            elif choice == '3':
                # View favorites
                if not favorites:
                    print("You have no saved favorites.")
                    continue
                
                print("\nYour favorite codenames:")
                for i, name in enumerate(favorites, 1):
                    print(f"{i}. {name}")
            
            elif choice == '4':
                # Manage favorites
                if not favorites:
                    print("You have no saved favorites.")
                    add_new = input("Would you like to add a new favorite? (y/n): ").lower()
                    if add_new == 'y':
                        new_name = input("Enter a codename to add to favorites: ")
                        favorites.append(new_name)
                        save_favorites(favorites, favorites_file)
                    continue
                
                print("\nFavorites Management:")
                print("1. Add a new favorite")
                print("2. Remove a favorite")
                print("3. Export favorites")
                print("4. Back to main menu")
                
                fav_choice = input("Enter your choice (1-4): ")
                
                if fav_choice == '1':
                    new_name = input("Enter a codename to add to favorites: ")
                    favorites.append(new_name)
                    save_favorites(favorites, favorites_file)
                
                elif fav_choice == '2':
                    print("\nYour favorite codenames:")
                    for i, name in enumerate(favorites, 1):
                        print(f"{i}. {name}")
                    
                    try:
                        remove_idx = int(input("Enter the number of the favorite to remove: ")) - 1
                        if 0 <= remove_idx < len(favorites):
                            removed = favorites.pop(remove_idx)
                            save_favorites(favorites, favorites_file)
                            print(f"Removed '{removed}' from favorites")
                        else:
                            print("Invalid number")
                    except ValueError:
                        print("Please enter a valid number")
                
                elif fav_choice == '3':
                    format_type = "text"
                    format_choice = input("Export format (text/json/csv/html) [text]: ").lower()
                    if format_choice in ['json', 'csv', 'html']:
                        format_type = format_choice
                    
                    filename = input("Enter export filename: ")
                    export_favorites(favorites, format_type, filename)
                
                elif fav_choice == '4':
                    continue
                
                else:
                    print("Invalid choice")
            
            elif choice == '5':
                # Change settings
                print("\nSettings:")
                print("1. Change theme")
                print("2. Manage exclusions")
                print("3. Configure codename pattern")
                print("4. Configure text case style")
                print("5. Configure word length limits")
                print("6. Configure separator")
                print("7. Back to main menu")
                
                settings_choice = input("Enter your choice (1-7): ")
                
                if settings_choice == '1':
                    # Change theme
                    themes = get_available_themes()
                    
                    if not themes:
                        print("No themes found. Would you like to create a new theme?")
                        create_theme = input("Create new theme? (y/n): ").lower()
                        if create_theme == 'y':
                            theme_name = input("Enter theme name: ")
                            os.makedirs(os.path.join(themes_dir, theme_name), exist_ok=True)
                            print(f"Created theme directory. Please add {theme_name}_adj.txt and {theme_name}_nouns.txt files.")
                        continue
                    
                    print("\nAvailable themes:")
                    print("0. Default (no theme)")
                    for i, theme in enumerate(themes, 1):
                        print(f"{i}. {theme}")
                    
                    try:
                        theme_choice = int(input("Enter theme number: "))
                        if theme_choice == 0:
                            # Reset to default
                            current_theme = None
                            adjectives = load_words(adj_file)
                            nouns = load_words(noun_file)
                            adjectives = filter_excluded_words(adjectives, exclusions)
                            nouns = filter_excluded_words(nouns, exclusions)
                            print("Switched to default word lists")
                        elif 1 <= theme_choice <= len(themes):
                            selected_theme = themes[theme_choice-1]
                            theme_adjectives, theme_nouns = load_themed_words(selected_theme)
                            
                            if theme_adjectives and theme_nouns:
                                current_theme = selected_theme
                                adjectives = filter_excluded_words(theme_adjectives, exclusions)
                                nouns = filter_excluded_words(theme_nouns, exclusions)
                                print(f"Switched to theme: {current_theme}")
                                print(f"Loaded {len(adjectives)} adjectives and {len(nouns)} nouns")
                        else:
                            print("Invalid theme number")
                    except ValueError:
                        print("Please enter a valid number")
                
                elif settings_choice == '2':
                    # Manage exclusions
                    print("\nExclusions Management:")
                    print("1. View current exclusions")
                    print("2. Add exclusion words")
                    print("3. Clear all exclusions")
                    print("4. Back to settings")
                    
                    excl_choice = input("Enter your choice (1-4): ")
                    
                    if excl_choice == '1':
                        if not exclusions:
                            print("No exclusions set.")
                        else:
                            print("\nCurrent exclusions:")
                            for i, word in enumerate(exclusions, 1):
                                print(f"{i}. {word}")
                    
                    elif excl_choice == '2':
                        new_exclusions = input("Enter words to exclude (comma separated): ")
                        new_words = [word.strip().lower() for word in new_exclusions.split(',')]
                        
                        for word in new_words:
                            if word and word not in exclusions:
                                exclusions.append(word)
                        
                        # Save exclusions to file
                        try:
                            with open(exclusions_file, 'w', encoding='utf-8') as file:
                                for word in exclusions:
                                    file.write(f"{word}\n")
                            print(f"Added {len(new_words)} words to exclusions")
                            
                            # Re-apply exclusions to current word lists
                            if current_theme:
                                theme_adjectives, theme_nouns = load_themed_words(current_theme)
                                adjectives = filter_excluded_words(theme_adjectives, exclusions)
                                nouns = filter_excluded_words(theme_nouns, exclusions)
                            else:
                                adjectives = load_words(adj_file)
                                nouns = load_words(noun_file)
                                adjectives = filter_excluded_words(adjectives, exclusions)
                                nouns = filter_excluded_words(nouns, exclusions)
                            
                            print(f"Updated to {len(adjectives)} adjectives and {len(nouns)} nouns after applying exclusions")
                            
                        except Exception as e:
                            print(f"Error saving exclusions: {str(e)}")
                    
                    elif excl_choice == '3':
                        confirm = input("Are you sure you want to clear all exclusions? (y/n): ").lower()
                        if confirm == 'y':
                            exclusions = []
                            if os.path.exists(exclusions_file):
                                os.remove(exclusions_file)
                            print("All exclusions cleared")
                            
                            # Reset word lists without exclusions
                            if current_theme:
                                adjectives, nouns = load_themed_words(current_theme)
                            else:
                                adjectives = load_words(adj_file)
                                nouns = load_words(noun_file)
                            
                            print(f"Updated to {len(adjectives)} adjectives and {len(nouns)} nouns after clearing exclusions")
                    
                    elif excl_choice == '4':
                        continue
                    
                    else:
                        print("Invalid choice")
                
                elif settings_choice == '3':
                    # Configure codename pattern
                    print("\nCodername Pattern:")
                    print("1. adj-noun (Adjective + Noun)")
                    print("2. noun-noun (Noun + Noun)")
                    print("3. adj-adj-noun (Adjective + Adjective + Noun)")
                    print("4. noun-adj (Noun + Adjective)")
                    print("5. adj-noun-number (Adjective + Noun + Number)")
                    
                    pattern_choice = input("Enter your choice (1-5): ")
                    if pattern_choice == '1':
                        pattern = "adj-noun"
                    elif pattern_choice == '2':
                        pattern = "noun-noun"
                    elif pattern_choice == '3':
                        pattern = "adj-adj-noun"
                    elif pattern_choice == '4':
                        pattern = "noun-adj"
                    elif pattern_choice == '5':
                        pattern = "adj-noun-number"
                    else:
                        print("Invalid choice, keeping current pattern")
                    
                    print(f"Pattern set to: {pattern}")
                
                elif settings_choice == '4':
                    # Configure text case style
                    print("\nText Case Style:")
                    print("1. Title Case (First Letter Of Each Word Capitalized)")
                    print("2. UPPERCASE (ALL LETTERS CAPITALIZED)")
                    print("3. lowercase (all letters lowercase)")
                    print("4. Sentence case (Only first letter capitalized)")
                    
                    case_choice = input("Enter your choice (1-4): ")
                    if case_choice == '1':
                        case_style = "title"
                    elif case_choice == '2':
                        case_style = "upper"
                    elif case_choice == '3':
                        case_style = "lower"
                    elif case_choice == '4':
                        case_style = "sentence"
                    else:
                        print("Invalid choice, keeping current case style")
                    
                    print(f"Case style set to: {case_style}")
                
                elif settings_choice == '5':
                    # Configure word length limits
                    try:
                        new_min = input("Enter minimum word length (0 for no minimum): ")
                        min_length = int(new_min) if new_min.isdigit() else 0
                        
                        new_max = input("Enter maximum word length (0 for no maximum): ")
                        max_length = int(new_max) if new_max.isdigit() else 0
                        
                        if min_length > 0 and max_length > 0 and min_length > max_length:
                            print("Error: Minimum length cannot be greater than maximum length")
                            min_length = 0
                            max_length = 0
                        
                        print(f"Word length limits set to: min={min_length}, max={max_length}")
                    except ValueError:
                        print("Invalid input. Using default values (no limits).")
                        min_length = 0
                        max_length = 0
                
                elif settings_choice == '6':
                    # Configure separator
                    print("\nSeparator Options:")
                    print("1. Space ( )")
                    print("2. Hyphen (-)")
                    print("3. Underscore (_)")
                    print("4. Dot (.)")
                    print("5. No separator")
                    print("6. Custom separator")
                    
                    sep_choice = input("Enter your choice (1-6): ")
                    if sep_choice == '1':
                        separator = " "
                    elif sep_choice == '2':
                        separator = "-"
                    elif sep_choice == '3':
                        separator = "_"
                    elif sep_choice == '4':
                        separator = "."
                    elif sep_choice == '5':
                        separator = ""
                    elif sep_choice == '6':
                        separator = input("Enter custom separator: ")
                    else:
                        print("Invalid choice, keeping current separator")
                    
                    print(f"Separator set to: '{separator}'")
                
                elif settings_choice == '7':
                    continue
                
                else:
                    print("Invalid choice")
            
            elif choice == '6':
                # Display help
                display_help()
            
            elif choice == '7':
                print("Thank you for using the Codename Generator. Goodbye!")
                break
                
            else:
                print("Invalid choice. Please enter a number from 1-7.")
                
        except KeyboardInterrupt:
            print("\nProgram interrupted. Exiting...")
            break

if __name__ == "__main__":
    print("Welcome to the Enhanced Random Codename Generator!")
    main()