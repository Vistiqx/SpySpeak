# SpySpeak

A Python application for crafting random operational identifiers for your classified projects. This application combines carefully selected nouns and adjectives to create authentic-sounding codenames used by intelligence agencies throughout, with advanced features for customization, organization, and deployment.

Generate names that sound like they came straight from intelligence briefings. From "Midnight Archer" to "Cobalt Sentinel," each codename maintains the perfect balance between memorability and professional gravity.

## Overview

This project contains three Python applications that generate creative codenames:

1. **Interactive Application** (`SpySpeak.py`): A feature-rich, menu-driven interface
2. **Command-line Tool** (`SpySpeak-cli.py`): A flexible command-line utility with extensive options
3. **Web Interface** (`SpySpeak-web.py`): A web server with both UI and REST API endpoints

All three applications randomly combine adjectives and nouns to create unique codenames like "Brave Tiger," "Silent Mountain," or "Quantum Falcon."

## Features

### Core Functionality
- Generate single or multiple codenames
- Combine adjectives and nouns from comprehensive word lists
- Clean, consistent output formatting

### Favorites Management
- Save particularly good codenames to a favorites file
- View, add, and remove favorites
- Export favorites to different formats

### Custom Word Categories (Themes)
- Support for themed word lists (sci-fi, fantasy, animals, etc.)
- Themes are stored in separate files in a `themes/` directory
- Command-line flag to select a specific theme (-t/--theme)

### Exclusion Lists
- Filter out inappropriate or unwanted words
- Simple text file with one word per line
- Automatically applied to all word lists

### Additional Output Formats
- **Text**: Simple list of codenames (default)
- **JSON**: Structured format for API integration
- **CSV**: Spreadsheet-compatible format
- **HTML**: Basic web page with formatted list

### Advanced Customization Options
- **Custom Formatting**: Control text case style (title case, UPPERCASE, lowercase, Sentence case)
- **Complex Patterns**: Generate different word combinations (adj-noun, noun-noun, adj-adj-noun, etc.)
- **Word Length Control**: Set minimum and maximum word lengths for more control over codename size
- **Custom Separators**: Choose different characters to separate words (space, hyphen, underscore, etc.)

### Web Interface & API
- User-friendly web interface with form controls
- REST API endpoints for programmatic access
- Support for all customization options
- Copy to clipboard functionality
- Responsive design that works on mobile and desktop

## Requirements

- Python 3.6 or higher
- Flask (for web interface only)

## Installation

1. Clone or download this repository:
   ```bash
   git clone https://github.com/Vistiqx/SpySpeak.git
   cd SpySpeak
   ```

2. Install required dependencies (for web interface):
   ```bash
   pip install -r requirements.txt
   ```

3. Prepare your word lists:
   - The repository comes with comprehensive `adjectives.txt` and `nouns.txt` files
   - You can create your own themed word lists as needed (see "Creating Themed Word Lists")

## File Structure

```
SpySpeak/
│
├── SpySpeak.py                          # Interactive application
├── SpySpeak-cli.py                      # Command-line tool
├── SpySpeak-web.py                      # Web server application
├── adjectives.txt                       # List of adjectives (one per line)
├── nouns.txt                            # List of nouns (one per line)
├── exclusions.txt                       # Words to exclude (optional)
├── favorites.txt                        # Saved favorite codenames (optional)
├── requirements.txt                     # Python dependencies
│
├── templates/                           # Directory for web templates
│   └── index.html                       # Main web interface template
│
├── static/                              # Directory for static web assets
│   └── favicon.ico                      # Favicon for web interface (optional)
│
├── themes/                              # Directory for themed word lists
│   ├── scifi_adj.txt                    # Sci-fi themed adjectives
│   ├── scifi_nouns.txt                  # Sci-fi themed nouns
│   ├── fantasy_adj.txt                  # Fantasy themed adjectives
│   └── fantasy_nouns.txt                # Fantasy themed nouns
│
└── README.md                            # This file
```

## Usage

### 1. Interactive Application

The interactive application provides a menu-driven interface with comprehensive options.

```bash
python SpySpeak.py
```

Follow the on-screen menu to:
1. Generate a single codename
2. Generate multiple codenames
3. View favorites
4. Manage favorites
5. Change settings (themes, exclusions, patterns, case styles, etc.)
6. Get help
7. Exit the application

#### Settings Options

- **Theme Selection**: Choose from available themes or use the default word lists
- **Exclusion Management**: View, add, or clear exclusion words
- **Pattern Configuration**: Choose between different word combinations
- **Case Style**: Select text formatting (Title Case, UPPERCASE, lowercase, Sentence case)
- **Word Length Limits**: Set minimum and maximum word lengths
- **Separator Configuration**: Choose or customize the separator between words

### 2. Command-line Tool

The command-line tool is designed for flexibility and automation, with clean output for integration with other tools.

```bash
python SpySpeak-cli.py [options]
```

#### Basic Options

| Option | Short | Long | Default | Description |
|--------|-------|------|---------|-------------|
| Adjectives file | `-a` | `--adjectives` | `adjectives.txt` | Path to adjectives file |
| Nouns file | `-n` | `--nouns` | `nouns.txt` | Path to nouns file |
| Count | `-c` | `--count` | `1` | Number of codenames to generate |
| Separator | `-s` | `--separator` | ` ` (space) | Separator between adjective and noun |
| Verbose | `-v` | `--verbose` | Off | Display diagnostic information |

#### Customization Options

| Option | Short | Long | Default | Description |
|--------|-------|------|---------|-------------|
| Pattern | `-p` | `--pattern` | `adj-noun` | Pattern for codename generation (adj-noun, noun-noun, adj-adj-noun, noun-adj, adj-noun-number) |
| Case style | | `--case` | `title` | Text case style (title, upper, lower, sentence) |
| Min length | | `--min-length` | `0` | Minimum length for words (0 for no minimum) |
| Max length | | `--max-length` | `0` | Maximum length for words (0 for no maximum) |

#### Output Options

| Option | Short | Long | Default | Description |
|--------|-------|------|---------|-------------|
| Format | `-f` | `--format` | `text` | Output format (text, json, csv, or html) |
| Output file | `-o` | `--output` | stdout | Write output to a file instead of screen |

#### Theme Options

| Option | Short | Long | Description |
|--------|-------|------|-------------|
| Theme | `-t` | `--theme` | Use specific theme from themes directory |
| List themes | | `--list-themes` | Display available themes and exit |

#### Exclusion Options

| Option | Short | Long | Default | Description |
|--------|-------|------|---------|-------------|
| Exclusions file | `-e` | `--exclusions` | `exclusions.txt` | Path to file with words to exclude |

#### Favorites Options

| Option | | Long | Default | Description |
|--------|---|------|---------|-------------|
| Favorites file | | `--favorites` | `favorites.txt` | Path to favorites file |
| List favorites | | `--list-favorites` | | Display saved favorites and exit |
| Add favorite | | `--add-favorite` | | Add a codename to favorites |
| Export favorites | | `--export-favorites` | | Export favorites to a file |

#### Examples

```bash
# Generate a single codename
python SpySpeak-cli.py

# Generate 5 codenames
python SpySpeak-cli.py -c 5

# Use a sci-fi theme
python SpySpeak-cli.py -t scifi

# Generate 10 codenames in JSON format
python SpySpeak-cli.py -c 10 -f json

# Save output to a file
python SpySpeak-cli.py -c 20 -o codenames.txt

# List all available themes
python SpySpeak-cli.py --list-themes

# View saved favorites
python SpySpeak-cli.py --list-favorites

# Add a codename to favorites
python SpySpeak-cli.py --add-favorite "Cosmic Voyager"

# Export favorites as HTML
python SpySpeak-cli.py --export-favorites favorites.html -f html

# Generate codenames with hyphen separator and exclude certain words
python SpySpeak-cli.py -c 5 -s "-" -e my_exclusions.txt

# Using different patterns and case styles
python SpySpeak-cli.py -p noun-noun --case upper
# Output: MOUNTAIN EAGLE

# Generate codenames with two adjectives and a noun
python SpySpeak-cli.py -p adj-adj-noun -c 3
# Output: Brave Silent Warrior

# Use numbered codenames in lowercase
python SpySpeak-cli.py -p adj-noun-number --case lower
# Output: swift eagle 42

# Only use words between 3-7 characters long
python SpySpeak-cli.py --min-length 3 --max-length 7
# Output: Bold Tiger
```

### 3. Web Interface

The web interface provides a user-friendly way to generate codenames and offers API endpoints for programmatic access.

```bash
# Start the web server
python SpySpeak-web.py
```

By default, the server will run on http://localhost:5000

#### Web UI

The web interface provides a simple form that allows you to:
- Specify the number of codenames to generate
- Choose from available themes
- Select patterns, case styles, and separators
- Set minimum and maximum word lengths
- Generate and view results instantly
- Copy individual codenames or all codenames to clipboard

#### REST API Endpoints

The web server also provides the following API endpoints:

##### Generate Codenames

```
GET /api/codenames
```

Query parameters:
- `count`: Number of codenames to generate (default: 1)
- `theme`: Theme to use (default: "default")
- `pattern`: Pattern to use (default: "adj-noun")
- `case`: Case style (default: "title")
- `separator`: Separator between words (default: " ")
- `min_length`: Minimum word length (default: 0)
- `max_length`: Maximum word length (default: 0)

Example request:
```
GET /api/codenames?count=5&theme=scifi&pattern=adj-noun-number&case=upper
```

Example response:
```json
{
  "success": true,
  "codenames": [
    "QUANTUM NEBULA 42",
    "GALACTIC ANDROID 156",
    "STELLAR MATRIX 7",
    "CYBERNETIC VORTEX 389",
    "BIONIC STARSHIP 254"
  ],
  "count": 5,
  "theme": "scifi",
  "pattern": "adj-noun-number",
  "case": "upper",
  "separator": " ",
  "min_length": 0,
  "max_length": 0
}
```

##### List Available Themes

```
GET /api/themes
```

Example response:
```json
{
  "success": true,
  "themes": ["scifi", "fantasy", "nature"]
}
```

## Creating Themed Word Lists

To create a custom theme:

1. Create a directory named `themes` in the same location as the script (if it doesn't exist already)
2. Create two files in this directory:
   - `themename_adj.txt` - containing themed adjectives (one per line)
   - `themename_nouns.txt` - containing themed nouns (one per line)

Example for a "fantasy" theme:
- `themes/fantasy_adj.txt` with fantasy-related adjectives
- `themes/fantasy_nouns.txt` with fantasy-related nouns

## Exclusion Lists

Create a file named `exclusions.txt` (or any name specified with `-e`) with words you want to exclude from codename generation, one word per line.

Example `exclusions.txt`:
```
bad
inappropriate
unwanted
```

## Troubleshooting

- **File not found errors**: Make sure all referenced files exist in the expected locations.
- **No themes found**: Create the `themes` directory and add properly named theme files.
- **No codenames generated**: Check that your word lists are not empty and that exclusions haven't filtered out all words.
- **Character encoding issues**: Ensure your text files are saved with UTF-8 encoding.
- **Web server errors**: Check that Flask is installed correctly (`pip install flask`).
- **Word length issues**: If you set min/max length constraints, ensure there are enough words that meet the criteria.

## Development

To enhance or modify this project:

1. Fork the repository
2. Make your changes
3. Run tests to ensure functionality still works
4. Create a pull request

## License

This project is open source and available under the MIT License.

## Acknowledgments

- The word lists are based on comprehensive English language resources
- This project was inspired by the need for creative project naming