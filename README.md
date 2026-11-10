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
