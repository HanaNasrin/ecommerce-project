from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.text import slugify
from shop.models import Product
from PIL import Image, ImageDraw, ImageFont, ImageChops
import os


def _color_from_name(name):
    # simple deterministic color
    h = sum(ord(c) for c in name) % 360
    return (int(40 + (h % 200)), int(80 + (h % 120)), int(100 + (h % 120)))


class Command(BaseCommand):
    help = 'Generate PNG product images for products without images'

    def handle(self, *args, **options):
        media_root = settings.MEDIA_ROOT
        target_dir = os.path.join(media_root, 'products')
        os.makedirs(target_dir, exist_ok=True)

        products = Product.objects.all()
        font_path = None
        try:
            font = ImageFont.truetype('arial.ttf', 36)
        except Exception:
            font = ImageFont.load_default()

        for p in products:
            if p.image:
                # already has image
                continue

            name = p.name
            slug = slugify(name)
            filename = f'{slug}.png'
            path = os.path.join(target_dir, filename)

            # create structured (no-text) image: gradient background + shapes
            width, height = 800, 600

            base_color = _color_from_name(name)
            # derive a second color for gradient
            secondary = ((base_color[0] + 60) % 256, (base_color[1] + 30) % 256, (base_color[2] + 90) % 256)

            img = Image.new('RGBA', (width, height))
            # vertical gradient
            for y in range(height):
                t = y / (height - 1)
                r = int(base_color[0] * (1 - t) + secondary[0] * t)
                g = int(base_color[1] * (1 - t) + secondary[1] * t)
                b = int(base_color[2] * (1 - t) + secondary[2] * t)
                ImageDraw.Draw(img).line([(0, y), (width, y)], fill=(r, g, b, 255))

            draw = ImageDraw.Draw(img, 'RGBA')

            # add a few geometric shapes with semi-transparency
            cx = int(width * 0.75)
            cy = int(height * 0.25)
            radius = int(min(width, height) * 0.22)
            circle_color = (255 - base_color[0], 255 - base_color[1], 255 - base_color[2], 140)
            draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=circle_color)

            rect_w = int(width * 0.6)
            rect_h = int(height * 0.18)
            rx = int(width * 0.12)
            ry = int(height * 0.6)
            rect_color = (base_color[0], base_color[1], base_color[2], 170)
            draw.rectangle([rx, ry, rx + rect_w, ry + rect_h], fill=rect_color)

            stripe_color = (secondary[0], secondary[1], secondary[2], 60)
            step = 40
            for i in range(-height, width, step):
                draw.polygon([(i, 0), (i + step // 2, 0), (i + height + step // 2, height), (i + height, height)], fill=stripe_color)

            # subtle vignette (invert so edges darker)
            vignette = Image.new('L', (width, height), 0)
            vd = ImageDraw.Draw(vignette)
            max_r = int(max(width, height) / 2)
            for i in range(max_r):
                alpha = int(180 * (i / max_r))
                vd.ellipse([i, i, width - i, height - i], fill=alpha)
            inv = ImageChops.invert(vignette)
            img.putalpha(inv)

            # flatten to RGB and save
            final = Image.new('RGB', (width, height), (255, 255, 255))
            final.paste(img, mask=img.split()[3])
            final.save(path, format='PNG')

            # update product image field
            p.image = f'products/{filename}'
            p.save()

            self.stdout.write(self.style.SUCCESS(f'Generated image for {p.name} -> {p.image}'))
