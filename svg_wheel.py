import math
import os
import xml.etree.ElementTree as et

from utils import create_dir

HEADERS = b"""<?xml version=\"1.0\" standalone=\"no\"?>
<?xml-stylesheet href="../wheel.css" type="text/css"?>
<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\"
\"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">
"""

PATH_TEMPLATE = """
M {start_outer_x},{start_outer_y}
A{outer_radius},{outer_radius} 0 0 1 {end_outer_x},{end_outer_y}
L {start_inner_x},{start_inner_y}
A{inner_radius},{inner_radius} 0 0 0 {end_inner_x},{end_inner_y}
Z
"""

FRACTION_LINE = 80
OFFSET = 20
PADDING = 10
RADIUS = 180
CENTER = PADDING + RADIUS
TAU = 2 * math.pi


def annular_sector_path(start, stop):
    inner_radius = RADIUS // 2
    outer_radius = RADIUS
    cos_stop = math.cos(stop)
    cos_start = math.cos(start)
    sin_stop = math.sin(stop)
    sin_start = math.sin(start)

    points = {
        "inner_radius": inner_radius,
        "outer_radius": outer_radius,
        "start_outer_x": CENTER + outer_radius * cos_start,
        "start_outer_y": CENTER + outer_radius * sin_start,
        "end_outer_x": CENTER + outer_radius * cos_stop,
        "end_outer_y": CENTER + outer_radius * sin_stop,
        "start_inner_x": CENTER + inner_radius * cos_stop,
        "start_inner_y": CENTER + inner_radius * sin_stop,
        "end_inner_x": CENTER + inner_radius * cos_start,
        "end_inner_y": CENTER + inner_radius * sin_start,
    }
    return PATH_TEMPLATE.format(**points)


def add_annular_sector(wheel, start, stop, style_class):
    return et.SubElement(
        wheel,
        "path",
        d=annular_sector_path(start=start, stop=stop),
        attrib={"class": style_class},
    )


def angles(index, total):
    start = index * TAU / total
    stop = (index + 1) * TAU / total

    return start - TAU / 4, stop - TAU / 4


def add_fraction(wheel, packages, total, version):
    text_attributes = {
        "class": "wheel-text",
        "text-anchor": "middle",
        "dominant-baseline": "central",
        "font-size": str(2 * OFFSET),
        "font-family": '"Helvetica Neue",Helvetica,Arial,sans-serif',
    }

    # Packages with some sort of wheel
    wheel_packages = sum(
        1 if package[version]["dropped_support"] == "yes" else 0 for package in packages
    )

    packages_with_wheels = et.SubElement(
        wheel,
        "text",
        x=str(CENTER),
        y=str(CENTER - OFFSET),
        attrib=text_attributes,
    )
    packages_with_wheels.text = f"{wheel_packages}"

    title = et.SubElement(packages_with_wheels, "title")
    percentage = f"{wheel_packages / float(total):.0%}"
    title.text = percentage

    # Dividing line
    et.SubElement(
        wheel,
        "line",
        x1=str(CENTER - FRACTION_LINE // 2),
        y1=str(CENTER),
        x2=str(CENTER + FRACTION_LINE // 2),
        y2=str(CENTER),
        attrib={"class": "wheel-line", "stroke-width": "2"},
    )

    # Total packages
    total_packages = et.SubElement(
        wheel,
        "text",
        x=str(CENTER),
        y=str(CENTER + OFFSET),
        attrib=text_attributes,
    )
    total_packages.text = f"{total}"

    title = et.SubElement(total_packages, "title")
    title.text = percentage


def generate_svg_wheel(packages, total, versions):
    for version in versions:
        wheel = et.Element(
            "svg",
            viewBox=f"0 0 {2 * CENTER} {2 * CENTER}",
            version="1.1",
            xmlns="http://www.w3.org/2000/svg",
        )

        for index, result in enumerate(packages):
            start, stop = angles(index, total)
            sector = add_annular_sector(
                wheel, start=start, stop=stop, style_class=result[version]["css_class"]
            )
            title = et.SubElement(sector, "title")
            title.text = f"{result['name']} {result[version]['icon']}"

        add_fraction(wheel, packages, total, version)

        create_dir(version)
        wheel_svg = os.path.join(version, "wheel.svg")
        wheel_png = os.path.join(version, "wheel.png")
        wheel_og_png = os.path.join(version, "wheel-og.png")
        with open(wheel_svg, "wb") as svg:
            svg.write(HEADERS)
            svg.write(et.tostring(wheel))

        # Install with: npm install svgexport
        os.system(f"./node_modules/.bin/svgexport {wheel_svg} {wheel_png} 32:32")
        os.system(f"./node_modules/.bin/svgexport {wheel_svg} {wheel_og_png} 630:630")
