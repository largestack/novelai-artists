# NovelAI Artist Gallery Generator

This tool generates a static website showcasing images created by NovelAI using different artist styles.

## Prerequisites

- Python 3.7 or higher
- A NovelAI account with API access
- Pillow (PIL Fork)
- Requests

## Setup

1. Install the required Python packages:

```bash
pip install -r requirements.txt
```

2. Set up authentication (choose one method):
   - Create a `.env` file with your NovelAI persistent token (recommended):
     ```
     NAI_PERSISTENT_TOKEN=your_persistent_token_here
     # OR
     NAI_PERSISTENT_API_KEY=your_persistent_token_here  # Alternative variable name
     ```
   - You can create a template .env file by running:
     ```bash
     python generate_site.py --create-env-template
     ```
   - Alternatively, you can provide an API key via command line or let the script prompt you for credentials

3. Prepare your input files:
   - `artists.txt` - A text file with one artist name per line
   - `prompts.json` - A JSON file with prompt data (see format below)
   - `template.prompt` - A text file with the prompt template

## Input File Formats

### artists.txt
```
Claude Monet
Vincent van Gogh
Leonardo da Vinci
...
```

### prompts.json
```json
[
  {
    "prompt_main": "A serene landscape with mountains in the background and a calm lake",
    "prompt_characters": ["person sitting by the lake", "small boat on the water"]
  },
  {
    "prompt_main": "A bustling city street at night with neon lights and rain",
    "prompt_characters": ["person with umbrella", "street vendor"]
  }
]
```

### template.prompt
```
{prompt}, artist:{artist}, detailed artwork, high quality, masterpiece
```

## Usage

Run the generator script:

```bash
python generate_site.py
```

You can run the script in different ways:

```bash
# Use credentials from .env file (recommended)
python generate_site.py

# Provide an API key directly
python generate_site.py --api-key YOUR_API_TOKEN

# Skip image generation and just build the website
python generate_site.py --no-generate

# Create a template .env file
python generate_site.py --create-env-template
```

### Authentication Methods (in order of priority)

1. Command-line API key (`--api-key`)
2. Persistent token from `.env` file (`NAI_PERSISTENT_TOKEN` or `NAI_PERSISTENT_API_KEY`)
3. Cached credentials from previous login
4. Interactive prompt for email/password

## Output

The script will:
1. Generate images for each artist-prompt combination
2. Create a static website in the `./output` directory
3. Generate thumbnails and optimize images

## Deploying to Vercel

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

3. Deploy the site:
```bash
vercel --prod
```

## Website Features

- Random sorting of images by default
- Option to group images by artist
- Infinite scroll loading
- Lightbox for enlarged images
- Display of full prompts when clicking on images
- Responsive design for mobile and desktop
- Copy artist style to clipboard by clicking on artist names
- Grid layout with 3 images per row
- SVG logo in the header
- Seed information displayed for each image

## License

MIT
