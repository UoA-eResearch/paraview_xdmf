#!/usr/bin/env python

from lxml import etree as ET
import sys
import os

DIMENSIONS = "128 128 128"

files = sys.argv[1:]

root = ET.Element("Xdmf", Version="2.0", nsmap={
  "xi": "http://www.w3.org/2001/XInclude"
})
dom = ET.SubElement(root, "Domain")
topo = ET.SubElement(dom, "Topology", name="topo", TopologyType="3DCoRectMesh", Dimensions=DIMENSIONS)
geo = ET.SubElement(dom, "Geometry", name="geo", Type="ORIGIN_DXDYDZ")
origin = ET.SubElement(geo, "DataItem", Format="XML", Dimensions="3").text = "0.0 0.0 0.0"
dxdydz = ET.SubElement(geo, "DataItem", Format="XML", Dimensions="3").text = "1.0 1.0 1.0"
ts = ET.SubElement(dom, "Grid", Name="TimeSeries", GridType="Collection", CollectionType="Temporal")

for f in files:
  base = os.path.basename(f)
  noext = os.path.splitext(base)[0]
  n = noext.split("_")[1]
  grid = ET.SubElement(ts, "Grid", GridType="Uniform", Name=n)
  time = ET.SubElement(grid, "Time", Value=n, Type="Single")
  toporef = ET.SubElement(grid, "Topology", Reference="/Xdmf/Domain/Topology[1]")
  georef = ET.SubElement(grid, "Geometry", Reference="/Xdmf/Domain/Geometry[1]")
  attr = ET.SubElement(grid, "Attribute", Name="scalars", Center="Node")
  data = ET.SubElement(attr, "DataItem", {
    "Format":"Binary",
    "DataType": "Float",
    "Precision": "4",
    "Endian": "Big",
    "Dimensions": DIMENSIONS
  }).text = f

print(ET.tostring(root, encoding='UTF-8', pretty_print=True, xml_declaration=True, doctype='<!DOCTYPE Xdmf SYSTEM "Xdmf.dtd" []>').decode())
