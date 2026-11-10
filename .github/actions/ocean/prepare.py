"""Prepare ocean coverage for the PBF header extent, within Mercator coverage."""
import json
import subprocess
import sys

header = json.loads(subprocess.check_output(['osmium', 'fileinfo', '--json', sys.argv[1]]))['header']
boxes = header['boxes']
if not boxes or any(len(box) != 4 for box in boxes):
    raise ValueError('The regional PBF must declare its geographic bounds')
bounds = [min(box[0] for box in boxes), max(-85, min(box[1] for box in boxes)),
          max(box[2] for box in boxes), min(85, max(box[3] for box in boxes))]
subprocess.run([sys.executable, '.ocean-tools/coastline-polygons.py',
                '--land-shapefile', '.ocean-land/land-polygons-split-3857/land_polygons.shp',
                '--bounds=' + ','.join(map(str, bounds)), 'ocean.items'], check=True)
