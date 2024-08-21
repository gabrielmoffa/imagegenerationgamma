from PIL import Image, ImageDraw, ImageFont
import csv
from moviepy.editor import ImageClip, concatenate_videoclips
from datetime import datetime

# Read event data from CSV file
def read_events_from_csv(csv_file):
    events = []
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            events.append(row)
    return events

# Convert a date string to the day of the week
def get_day_of_week(date_str, year='2024'):
    try:
        # Append the year to the date string
        date_str_with_year = f"{date_str} {year}"
        date_obj = datetime.strptime(date_str_with_year, '%d %B %Y')  # Adjust format if needed
        return date_obj.strftime('%A')  # Full day name (e.g., 'Monday')
    except ValueError:
        return 'Unknown Day'

# Create a vertical image for each day
def create_day_images(events):
    days = {}  # Dictionary to hold events for each day
    generated_images = []  # List to store the paths of generated images
    for event in events:
        date = event['Date']
        if date not in days:
            days[date] = []  # Initialize empty list for the day
        days[date].append(event)

    for date, events_for_day in days.items():
        # Create a blank image
        width, height = 1080, 1920  # Insta story format
        image = Image.new("RGBA", (width, height), color=(255, 255, 255, 255))
        
        # Load the background image
        background = Image.open("background.png").convert("RGBA")
        
        # Composite the background onto the image
        image = Image.alpha_composite(image, background)

        draw = ImageDraw.Draw(image)

        # Get the day of the week
        day_of_week = get_day_of_week(date)

        # Draw day of the week centered
        font_title = ImageFont.truetype("Montserrat-Regular.ttf", 60)  # Adjust font as needed
        text = f"{day_of_week}'s Events:"
        text_bbox = draw.textbbox((0, 0), text, font=font_title)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = (width - text_width) / 2
        draw.text((text_x, 180), text, fill=(72, 45, 2, 255), font=font_title)

        # Draw the date centered
        font_date = ImageFont.truetype("Montserrat-Regular.ttf", 38)  # Adjust font as needed
        date_text = f"Date: {date}"
        date_text_bbox = draw.textbbox((0, 0), date_text, font=font_date)
        date_text_width = date_text_bbox[2] - date_text_bbox[0]
        date_text_x = (width - date_text_width) / 2
        draw.text((date_text_x, 250), date_text, fill=(72, 45, 2, 255), font=font_date)

        # Draw event titles and times
        y = 380  # Initial y-coordinate
        font_event = ImageFont.truetype("Montserrat-Regular.ttf", 39)  # Adjust font as needed
        for event in events_for_day:
            event_info = f"• {event['Event title']} - {event['Time']}"
            draw.text((30, y), event_info, fill=(72, 45, 2, 255), font=font_event)
            y += 70  # Increase y-coordinate for the next event

        # Save the image
        image_path = f"{date}_events.png"
        image.save(image_path)
        generated_images.append(image_path)

    return generated_images

# Create video from generated images
def create_video(image_paths, output_path="output_video.mp4"):
    clips = [ImageClip(img).set_duration(2) for img in image_paths]  # Display each image for 2 seconds
    video = concatenate_videoclips(clips, method="compose")
    video.write_videofile(output_path, fps=24)

if __name__ == "__main__":
    csv_file_path = "Events Newsletter - Soc.csv"  # Update with your actual CSV file path
    events_data = read_events_from_csv(csv_file_path)
    generated_images = create_day_images(events_data)
    
    # Create the video
    create_video(generated_images)
    print("Images and video generated successfully!")
