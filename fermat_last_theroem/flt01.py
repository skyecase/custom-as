
import os
import requests
from io import BytesIO
from PIL import Image
from manim import *
import numpy as np
import wikipedia
import re
from bs4 import BeautifulSoup

def search_and_download_mathematician_portraits(mathematician_names, output_folder="mathematician_portraits"):
    """
    Search for mathematicians on Wikipedia, find their main page, and download the first portrait image

    Args:
        mathematician_names: List of mathematician names
        output_folder: Directory to save the portraits

    Returns:
        List of file paths to the downloaded portraits
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    portrait_paths = []

    for name in mathematician_names:
        file_path = os.path.join(output_folder, f"{name}.jpg")
        portrait_paths.append(file_path)

        # Skip download if file already exists
        if os.path.exists(file_path):
            print(f"Portrait for {name} already exists at {file_path}")
            continue

        try:
            # Step 1: Search for the mathematician on Wikipedia
            search_results = wikipedia.search(name + " mathematician")
            if not search_results:
                print(f"No Wikipedia results found for {name}")
                continue

            # Get the page title that most likely corresponds to the mathematician
            page_title = search_results[0]
            print(f"Found Wikipedia page: {page_title}")

            # Step 2: Get the Wikipedia page
            wiki_page = wikipedia.page(page_title, auto_suggest=False)

            # Step 3: Extract the HTML content of the page
            response = requests.get(wiki_page.url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Step 4: Find the first image in the infobox (typically the portrait)
            infobox = soup.find('table', {'class': 'infobox'})
            img_url = None

            if infobox:
                img_tag = infobox.find('img')
                if img_tag and 'src' in img_tag.attrs:
                    img_src = img_tag['src']
                    # Convert relative URL to absolute URL if needed
                    if img_src.startswith('//'):
                        img_url = 'https:' + img_src
                    else:
                        img_url = img_src

            # If no image found in infobox, try to find first image in article
            if not img_url:
                first_image = soup.find('img')
                if first_image and 'src' in first_image.attrs:
                    img_src = first_image['src']
                    if img_src.startswith('//'):
                        img_url = 'https:' + img_src
                    else:
                        img_url = img_src

            if not img_url:
                print(f"No image found for {name}")
                continue

            # Step 5: Download the image
            img_response = requests.get(img_url)
            if img_response.status_code == 200:
                # Process and save the image
                img = Image.open(BytesIO(img_response.content))

                # Convert to RGB if RGBA (for PNG images)
                if img.mode == 'RGBA':
                    img = img.convert('RGB')

                # Crop to square focusing on face (center crop)
                width, height = img.size
                size = min(width, height)
                left = (width - size) // 2
                top = (height - size) // 2
                right = left + size
                bottom = top + size
                img = img.crop((left, top, right, bottom))

                # Resize to consistent dimensions
                img = img.resize((300, 300))

                # Save the processed image
                img.save(file_path)
                print(f"Successfully downloaded portrait for {name}")
            else:
                print(f"Failed to download image for {name}: HTTP {img_response.status_code}")

        except Exception as e:
            print(f"Error processing portrait for {name}: {str(e)}")
            if file_path in portrait_paths:
                portrait_paths.remove(file_path)

    return portrait_paths

class TheoremThumbnail(Scene):
    def construct(self):
        # Set background color to pure black
        self.camera.background_color = BLACK

        # Create the blackboard
        board = Rectangle(
            height=5,
            width=9,
            fill_color="#123456",
            fill_opacity=1,
            stroke_color=GOLD,
            stroke_width=6
        )

        # Create the theorem text
        theorem_equation = MathTex(r"a^n + b^n = c^n", font_size=80)
        theorem_text = Tex(r"has no positive\\integer solutions for", font_size=50)
        n_condition = MathTex(r"n > 2", font_size=70)

        # Arrange theorem components
        theorem_group = VGroup(theorem_equation, theorem_text, n_condition).arrange(DOWN, buff=0.3)
        theorem_group.move_to(board.get_center())

        # List of mathematicians
        mathematician_names = ["Fermat", "Euler", "Gauss", "Germain",
                              "Dirichlet", "Kummer", "Taniyama", "Wiles", "Taylor"]

        # Download portraits by searching Wikipedia
        portrait_paths = search_and_download_mathematician_portraits(mathematician_names)

        # Create portrait frames with images
        portrait_width = 0.8
        portrait_frames = VGroup()
        portrait_images = Group()


        for i, name in enumerate(mathematician_names):
            # Create frame
            frame = Rectangle(
                width=portrait_width,
                height=1.2*portrait_width,
                stroke_color=GOLD_E,
                stroke_width=2,
                fill_color=GREY_D,
                fill_opacity=1
            )
            portrait_frames.add(frame)

            # Add portrait image if available
            file_path = os.path.join("mathematician_portraits", f"{name}.jpg")
            if os.path.exists(file_path):
                # Use ImageMobject to display the portrait
                portrait = ImageMobject(file_path)
                # Scale to fit within the frame with a small margin
                portrait.height = frame.height * 0.9
                portrait.move_to(frame.get_center())
                portrait_images.add(portrait)

        # Arrange portrait frames horizontally above the board
        portrait_frames.arrange(RIGHT, buff=0.1)
        portrait_frames.next_to(board, UP, buff=0.5)

        # Ensure images are positioned within their frames
        for i, portrait in enumerate(portrait_images):
            portrait.move_to(portrait_frames[i].get_center())

        # Add labels for mathematicians
        mathematician_labels = VGroup()
        for i, name in enumerate(mathematician_names):
            label = Text(name, font_size=12)
            label.next_to(portrait_frames[i], DOWN, buff=0.1)
            mathematician_labels.add(label)

        # Add all elements to the scene
        self.add(board, theorem_equation, theorem_text, n_condition, portrait_frames)

        # Add the portrait images
        for portrait in portrait_images:
            self.add(portrait)

        # Add mathematician labels
        self.add(mathematician_labels)

        # Add subtle chalk texture effect to the theorem text
        for element in [theorem_equation, theorem_text, n_condition]:
            element.set_color(WHITE)
            element.set_stroke(WHITE, width=0.5, opacity=0.3)

if __name__ == "__main__":
    # Command line: manim -p -qh thumbnail_script.py TheoremThumbnail
    # This will render in high quality (-qh) and play the result (-p)
    scene = TheoremThumbnail()
    scene.render()
