import os
import argparse
from cairosvg import svg2png

SVG_PATH = "svg"

if __name__ == "__main__":
    parser = argparse.ArgumentParser("convert svg icons to png icons")
    parser.add_argument("path")
    args = parser.parse_args()


    for path, dirnames, filenames in os.walk(os.path.join(args.path, SVG_PATH)):
        for svg_filename in filenames:
            for size in (32, 48, 64):
                svg2png(
                    url=os.path.join(args.path, SVG_PATH, svg_filename),
                    write_to=os.path.join(args.path, f"png_{size}", svg_filename.split('.')[0] + '.png'),
                    output_width=size,
                    output_height=size
                )
                

