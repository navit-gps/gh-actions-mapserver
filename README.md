# Navit Map Server

Pre-built [Navit](https://github.com/navit-gps/navit) maps, automatically converted daily from [Geofabrik](https://download.geofabrik.de/) OSM extracts.

## Getting a map

Go to the [latest release](https://github.com/navit-gps/gh-actions-mapserver/releases/latest) and download the `.bin` file for your region.

Files are named `<continent>-<region>-<date>.bin`, for example:

```
europe-france-alsace-2026-03-18.bin
north-america-us-california-2026-03-18.bin
asia-japan-2026-03-18.bin
```

## Using the map in Navit

Place the downloaded `.bin` file somewhere on your device and point Navit to it in your `navit.xml`:

```xml
<mapset enabled="yes">
  <map type="binfile" enabled="yes" data="/path/to/your-region.bin"/>
</mapset>
```

## Updates

A new release is published every day. Check the [releases page](https://github.com/navit-gps/gh-actions-mapserver/releases) for the latest build for your region.

## Water coverage

Regional maps use full-resolution global land polygons from
https://osmdata.openstreetmap.de/data/land-polygons.html to prepare complete ocean
coverage. Every map in a run uses the same cached snapshot, checked by SHA-256.
A missing cache entry or invalid geometry fails that map conversion; it never
falls back to regional coastline inference. The snapshot is selected daily. Manual rebuilds append their workflow run ID
to the release tag, so they do not collide with the scheduled daily release.

Ocean coverage follows the PBF header bounds, clipped to 85 degrees north and
south. Inland water still comes from the regional OSM input. Maptool reports and
skips water relations with incomplete inner boundaries so they can be checked
against the full source data and corrected in OSM.

The land data is © OpenStreetMap contributors, available under the ODbL:
https://www.openstreetmap.org/copyright. Its README and source/output hashes remain
in the preparation directory alongside the generated water items.
