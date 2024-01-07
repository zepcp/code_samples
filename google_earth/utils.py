def to_kml(label: str, latitude: str, longitude: str):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
    <name>{label}.kmz</name>
    <Schema name="kmzs - Folha1 (1)" id="S_kmzs___Folha1__1__SSSSI">
        <SimpleField type="string" name="Latitude"><displayName>&lt;b&gt;Latitude&lt;/b&gt;</displayName>
</SimpleField>
        <SimpleField type="string" name="Longitude"><displayName>&lt;b&gt;Longitude&lt;/b&gt;</displayName>
</SimpleField>
        <SimpleField type="string" name="Name"><displayName>&lt;b&gt;Name&lt;/b&gt;</displayName>
</SimpleField>
        <SimpleField type="string" name="Description"><displayName>&lt;b&gt;Description&lt;/b&gt;</displayName>
</SimpleField>
        <SimpleField type="int" name="Icon"><displayName>&lt;b&gt;Icon&lt;/b&gt;</displayName>
</SimpleField>
    </Schema>
    <Style id="normPointStyle">
        <IconStyle>
            <Icon>
                <href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href>
            </Icon>
        </IconStyle>
        <BalloonStyle>
            <text><![CDATA[<table border="0">
  <tr><td><b>Latitude</b></td><td>$[kmzs - Folha1 (1)/Latitude]</td></tr>
  <tr><td><b>Longitude</b></td><td>$[kmzs - Folha1 (1)/Longitude]</td></tr>
  <tr><td><b>Name</b></td><td>$[kmzs - Folha1 (1)/Name]</td></tr>
  <tr><td><b>Description</b></td><td>$[kmzs - Folha1 (1)/Description]</td></tr>
  <tr><td><b>Icon</b></td><td>$[kmzs - Folha1 (1)/Icon]</td></tr>
</table>
]]></text>
        </BalloonStyle>
    </Style>
    <Style id="hlightPointStyle">
        <IconStyle>
            <Icon>
                <href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle_highlight.png</href>
            </Icon>
        </IconStyle>
        <BalloonStyle>
            <text><![CDATA[<table border="0">
  <tr><td><b>Latitude</b></td><td>$[kmzs - Folha1 (1)/Latitude]</td></tr>
  <tr><td><b>Longitude</b></td><td>$[kmzs - Folha1 (1)/Longitude]</td></tr>
  <tr><td><b>Name</b></td><td>$[kmzs - Folha1 (1)/Name]</td></tr>
  <tr><td><b>Description</b></td><td>$[kmzs - Folha1 (1)/Description]</td></tr>
  <tr><td><b>Icon</b></td><td>$[kmzs - Folha1 (1)/Icon]</td></tr>
</table>
]]></text>
        </BalloonStyle>
    </Style>
    <StyleMap id="pointStyleMap">
        <Pair>
            <key>normal</key>
            <styleUrl>#normPointStyle</styleUrl>
        </Pair>
        <Pair>
            <key>highlight</key>
            <styleUrl>#hlightPointStyle</styleUrl>
        </Pair>
    </StyleMap>
    <Placemark>
        <name>{label}</name>
        <styleUrl>#pointStyleMap</styleUrl>
        <Style id="inline">
            <IconStyle>
                <color>ffe7ebef</color>
                <colorMode>normal</colorMode>
            </IconStyle>
            <LineStyle>
                <color>ffe7ebef</color>
                <colorMode>normal</colorMode>
            </LineStyle>
            <PolyStyle>
                <color>ffe7ebef</color>
                <colorMode>normal</colorMode>
            </PolyStyle>
        </Style>
        <ExtendedData>
            <SchemaData schemaUrl="#S_kmzs___Folha1__1__SSSSI">
                <SimpleData name="Latitude">38.74898889</SimpleData>
                <SimpleData name="Longitude">-8.969475</SimpleData>
                <SimpleData name="Name">{label}</SimpleData>
                <SimpleData name="Description">{label}</SimpleData>
                <SimpleData name="Icon">0</SimpleData>
            </SchemaData>
        </ExtendedData>
        <Point>
            <coordinates>{longitude},{latitude},0</coordinates>
        </Point>
    </Placemark>
</Document>
</kml>
"""
