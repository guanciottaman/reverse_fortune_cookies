import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont, ImageTk
import io
import random
import math

from customtkinter.windows.widgets.image.ctk_image import CTkImage

class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Reverse Fortune Cookies")
        self.geometry("1080x720")
        self.font = ctk.CTkFont("JosJosefinSans-Regular.ttf", size=24)
        
        self.fortunes = [
            "Tomorrow will be just as mediocre as today.",
            "Your luck is taking a nap.",
            "The future is bleak, but hey, at least you’re consistent.",
            "You’ll find what you’re looking for… in a place you forgot.",
            "The only thing certain is uncertainty. And more uncertainty.",
            "Today is a great day to start a diet. Tomorrow is even better.",
            "Your next big break will come when you least expect it… like when you’re stuck in traffic.",
            "If life gives you lemons, just wait for the lemonade stand to pop up.",
            "The stars are aligning in your favor, but they forgot to check your calendar.",
            "You will soon discover a hidden talent. It might be the ability to ignore alarm clocks.",
            "Someone will surprise you with a gift. Spoiler: It’s not a time machine.",
            "Today you will learn the value of patience. Preferably before you run out of coffee.",
            "An unexpected encounter will lead to a great opportunity, like a free coffee at the corner cafe.",
            "Your creativity will soon shine brightly. Just try not to set off any fire alarms.",
            "You will achieve greatness. At least, in the eyes of your cat.",
            "Prepare for a whirlwind of activity. Or maybe just a very busy day at the office.",
            "A new adventure awaits you. It might involve a detour to the nearest snack bar.",
            "You will soon receive a pleasant surprise. Hopefully not from an unexpected bill.",
            "Your future looks bright, but remember to wear sunglasses.",
            "You will find what you’re looking for. But first, you might have to look for your keys.",
            "The best way to predict the future is to invent it. Or just consult a crystal ball.",
            "You’ll soon be the recipient of a mysterious gift. It might just be a coupon for free pizza.",
            "Your next great idea will come to you in the most unexpected place… like the shower.",
            "You will soon find yourself in a situation where your patience will be tested. Brace yourself for traffic jams.",
            "Someone will soon make you an offer you can’t refuse. Probably because it's a free dessert.",
            "You will soon receive an exciting phone call. Maybe it's from a long-lost friend or a telemarketer.",
            "A surprise is waiting for you just around the corner. If you’re walking, be careful not to trip.",
            "You’ll have a lucky day soon, but it might involve an unplanned nap or two.",
            "An opportunity will soon come your way. It might be as simple as finding the last slice of cake.",
            "Prepare for a change. It might be as minor as a new hairstyle or as major as a new coffee flavor.",
            "The next few days will be full of pleasant surprises. Or at least fewer traffic tickets.",
            "A new acquaintance will soon bring you joy. Or at least a good story to tell.",
            "You’ll soon discover a new hobby. It might involve knitting, painting, or binge-watching documentaries.",
            "Your positivity will attract good things. Just don’t be surprised if it attracts a few mosquitoes too.",
            "You will soon achieve something you’ve been working on. It might be a personal record in binge-watching."
        ]
        
        self.cookie_image_path = "cookieopen.png"
        self.cookie_image_label = ctk.CTkLabel(self, text="")
        self.cookie_image_label.pack(pady=20)
        
        self.fortune_button = ctk.CTkButton(self, width=200, height=40, text="Crack Cookie",
           command=self.display_fortune, font=self.font)
        self.fortune_button.pack(pady=10)

        self.display_fortune()  # Show initial fortune
    
    def draw_curved_text_on_cookie(self, cookie_image_path, text, font_size=18, max_chars_per_line=30, vertical_padding=70):
        # Load the cookie image
        cookie_image = Image.open(cookie_image_path).convert("RGBA")
        draw = ImageDraw.Draw(cookie_image)
    
        # Define the font and size
        try:
            font = ImageFont.truetype("JosefinSans-Regular.ttf", font_size)  # Ensure the font file is accessible
        except IOError:
            font = ImageFont.load_default()
    
        # Split the text into lines
        lines = self.wrap_text(text, max_chars_per_line)
        
        # Calculate text height and position
        total_text_height = sum(self.get_text_height(draw, line, font) for line in lines)
        width, height = cookie_image.size
        center_x = width / 2
        start_y = (height - total_text_height) / 2 + vertical_padding
        
        # Draw curved text on the image
        for i, line in enumerate(lines):
            # Subtle curve effect
            curve_offset = 5 * math.sin(i / len(lines) * math.pi)  # Slight vertical offset
            text_width, text_height = self.get_text_size(draw, line, font)
            x = (width - text_width) / 2  # Center the text horizontally
            y = start_y + i * (font_size + 5) + curve_offset
            
            draw.text((x, y), line, font=font, fill="black")
    
        # Convert to a format that CustomTkinter can use
        byte_io = io.BytesIO()
        cookie_image.save(byte_io, format='PNG')
        byte_io.seek(0)
    
        return byte_io
    
    def wrap_text(self, text, max_chars_per_line):
        lines = []
        words = text.split()
        current_line = ""

        for word in words:
            if len(current_line) + len(word) + 1 <= max_chars_per_line:
                current_line = f"{current_line} {word}".strip()
            else:
                lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def get_text_size(self, draw, text, font):
        """Calculate the width and height of the text."""
        bbox = draw.textbbox((0, 0), text, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        return width, height

    def get_text_height(self, draw, text, font):
        """Calculate the height of the text."""
        _, height = self.get_text_size(draw, text, font)
        return height

    def display_fortune(self):
        fortune = random.choice(self.fortunes)
        image_bytes = self.draw_curved_text_on_cookie(self.cookie_image_path, fortune)
        image = Image.open(image_bytes)
        ctk_image = CTkImage(image, size=(600, 600))

        # Update the image label with the new fortune
        self.cookie_image_label.configure(image=ctk_image)

if __name__ == "__main__":
    app = App()
    app.mainloop()
