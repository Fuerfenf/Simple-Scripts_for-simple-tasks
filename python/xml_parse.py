import xml.etree.ElementTree as ET


tree = ET.parse('test.xml')
root = tree.getroot()
tags = [elem.tag for elem in root.iter()]
for itm in tags:
    print(itm)