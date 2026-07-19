"""
Visualization Generator for Multilingual VLM Benchmark
Generates automatic overlays, bounding boxes, polygons, reading-order arrows, and color legends.
"""

import json
import os
from PIL import Image, ImageDraw, ImageFont

def draw_legend(draw, font, colors, position=(10, 10)):
    y_offset = position[1]
    for label, color in colors.items():
        draw.rectangle([position[0], y_offset, position[0] + 20, y_offset + 20], fill=color)
        if font:
            draw.text((position[0] + 30, y_offset), label, fill="white", font=font)
        y_offset += 25

def generate_visualization(image_path, annotation_path, output_path):
    img = Image.open(image_path).convert("RGBA")
    
    # Create an overlay for transparency
    overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = None

    with open(annotation_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Color definitions
    colors = {
        "Hindi": (255, 0, 0, 180),     # Red
        "English": (0, 0, 255, 180),   # Blue
        "Default": (0, 255, 0, 180),   # Green
        "Polygon": (255, 165, 0, 120), # Orange transparent
        "Arrow": (0, 255, 255, 255)    # Cyan
    }
    
    regions = data.get("ocr_regions", [])
    centers = {}

    for region in regions:
        region_id = region.get("region_id")
        bbox = region.get("bbox")
        polygon = region.get("polygon")
        lang = region.get("language", "Default")
        
        color = colors.get(lang, colors["Default"])

        if polygon:
            # Render polygon
            poly_tuples = [tuple(p) for p in polygon]
            draw.polygon(poly_tuples, outline=color, width=3)
        elif bbox:
            # Render bbox
            draw.rectangle(bbox, outline=color, width=4)

        # Calculate center for reading order arrows
        if bbox:
            cx = (bbox[0] + bbox[2]) / 2
            cy = (bbox[1] + bbox[3]) / 2
            centers[region_id] = (cx, cy)
            
            # Draw label
            label_text = f"{region_id} ({lang})"
            if font:
                draw.text((bbox[0], max(0, bbox[1] - 25)), label_text, fill=color, font=font)

    # Draw reading order arrows based on relationships or sequence
    relationships = data.get("relationships", {})
    text_flow = relationships.get("text_flow", [])
    
    if not text_flow:
        # Fallback to reading_order attribute
        regions_sorted = sorted([r for r in regions if "reading_order" in r], key=lambda x: x["reading_order"])
        text_flow = [r["region_id"] for r in regions_sorted]

    for i in range(len(text_flow) - 1):
        r1 = text_flow[i]
        r2 = text_flow[i+1]
        if r1 in centers and r2 in centers:
            # Draw arrow line
            draw.line([centers[r1], centers[r2]], fill=colors["Arrow"], width=3)

    # Draw legend
    legend_colors = {k: v for k, v in colors.items() if k != "Default"}
    draw_legend(draw, font, legend_colors)

    # Combine with original image
    out_img = Image.alpha_composite(img, overlay)
    out_img.convert("RGB").save(output_path)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate Grounding Visualizations")
    parser.add_argument("--image", required=True, help="Path to input image")
    parser.add_argument("--annotation", required=True, help="Path to annotation.json")
    parser.add_argument("--output", required=True, help="Path to save visualization.png")
    args = parser.parse_args()
    
    generate_visualization(args.image, args.annotation, args.output)
    print(f"Visualization saved to {args.output}")
