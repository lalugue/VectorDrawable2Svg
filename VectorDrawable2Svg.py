"""
VectorDrawable2Svg
This script converts a VectorDrawable into an SVG file
Authors: Alessandro Lucchet, lalugue

Usage: Place an xml file in the same folder as this script, then run using:
python VectorDrawable2Svg.py <yourFile>.xml

"""

from xml.dom.minidom import *
import sys

# extracts all paths inside vdContainer and add them into svgContainer
def convertPaths(vdContainer,svgContainer,svgXml):
	vdPaths = vdContainer.getElementsByTagName('path')
	for vdPath in vdPaths:
		# only iterate in the first level
		if vdPath.parentNode == vdContainer:
			svgPath = svgXml.createElement('path')
			svgPath.attributes['d'] = vdPath.attributes['android:pathData'].value
			if vdPath.hasAttribute('android:fillColor'):
				svgPath.attributes['fill'] = vdPath.attributes['android:fillColor'].value
			else:
				svgPath.attributes['fill'] = 'none'
			if vdPath.hasAttribute('android:strokeLineJoin'):
				svgPath.attributes['stroke-linejoin'] = vdPath.attributes['android:strokeLineJoin'].value
			if vdPath.hasAttribute('android:strokeLineCap'):
				svgPath.attributes['stroke-linecap'] = vdPath.attributes['android:strokeLineCap'].value
			if vdPath.hasAttribute('android:strokeMiterLimit'):
				svgPath.attributes['stroke-miterlimit'] = vdPath.attributes['android:strokeMiterLimit'].value
			if vdPath.hasAttribute('android:strokeWidth'):
				svgPath.attributes['stroke-width'] = vdPath.attributes['android:strokeWidth'].value
			if vdPath.hasAttribute('android:strokeColor'):
				svgPath.attributes['stroke'] = vdPath.attributes['android:strokeColor'].value
			if vdPath.hasAttribute('android:fillAlpha'):
				svgPath.attributes['fill-opacity'] = vdPath.attributes['android:fillAlpha'].value
			if vdPath.hasAttribute('android:strokeAlpha'):
				svgPath.attributes['stroke-opacity'] = vdPath.attributes['android:strokeAlpha'].value
			svgContainer.appendChild(svgPath);
		
# define the function which converts a vector drawable to a svg
def convertVd(vdFilePath):

	# create svg xml
	svgXml = Document()
	svgNode = svgXml.createElement('svg')
	svgXml.appendChild(svgNode);

	# open vector drawable
	vdXml = parse(vdFilePath)
	vdNode = vdXml.getElementsByTagName('vector')[0]

	# setup basic svg info
	svgNode.attributes['xmlns'] = 'http://www.w3.org/2000/svg'
	svgNode.attributes['width'] = vdNode.attributes['android:viewportWidth'].value
	svgNode.attributes['height'] = vdNode.attributes['android:viewportHeight'].value
	svgNode.attributes['viewBox'] = '0 0 {} {}'.format(vdNode.attributes['android:viewportWidth'].value, vdNode.attributes['android:viewportHeight'].value)

	# iterate through all groups
	vdGroups = vdXml.getElementsByTagName('group')
	for vdGroup in vdGroups:
	
		# create the group
		svgGroup = svgXml.createElement('g')
		
		# setup attributes of the group
		if vdGroup.hasAttribute('android:translateX'):
			svgGroup.attributes['transform'] = 'translate({},{})'.format(vdGroup.attributes['android:translateX'].value,vdGroup.attributes['android:translateY'].value)
		
		# iterate through all paths inside the group
		convertPaths(vdGroup,svgGroup,svgXml)
			
		# append the group to the svg node
		svgNode.appendChild(svgGroup);

	# iterate through all svg-level paths
	convertPaths(vdNode,svgNode,svgXml)

	# write xml to file
	svgXml.writexml(open(vdFilePath[:-4] + '.svg', 'w'),indent="",addindent="  ",newl='\n')
	
# script begin
if len(sys.argv)>1:
	iterArgs = iter(sys.argv)
	next(iterArgs) #skip the first entry (it's the name of the script)
	for arg in iterArgs:
		convertVd(arg)
else:
	print("You have to pass me something")
	sys.exit()
