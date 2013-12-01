#qpy:console

__author__ = 'Michael Malloy'

######################################
# Google Directions API
# Dependencies: elementtree, xml_dict
#
#
#
######################################

import sys
import urllib2
from elementtree.ElementTree import parse
import xmldict

baseUrl = 'https://maps.googleapis.com/maps/api/directions/xml?'

def generateHTML(xmlData):
    with open('directions.html', 'w') as html:

        print xmlData['DirectionsResponse']['status']
        print xmlData['DirectionsResponse']['route']
        print xmlData['DirectionsResponse']['route']['leg']

        print xmlData['DirectionsResponse']['route']['leg']['start_address']
        print xmlData['DirectionsResponse']['route']['leg']['end_address']
        print xmlData['DirectionsResponse']['route']['leg']['distance']['text']
        print xmlData['DirectionsResponse']['route']['leg']['duration']['text']

        html.write('<table border="1" cellpadding="5">')
        html.write('<caption><h3>')
        html.write(xmlData['DirectionsResponse']['route']['leg']['start_address'])
        html.write(' To ')
        html.write(xmlData['DirectionsResponse']['route']['leg']['end_address'])
        html.write('</h3></caption>')

        html.write('<tr>')
        html.write('<th width="5%">')
        html.write('Distance')
        html.write('</th>')
        html.write('<th width="5%">')
        html.write('Estimated Time')
        html.write('</th>')
        html.write('<th width="10%">')
        html.write('Start Destination')
        html.write('</th>')
        html.write('<th width="10%">')
        html.write('End Destination')
        html.write('</th>')
        html.write('</tr>')

        html.write('<tr>')
        html.write('<td>')
        html.write(xmlData['DirectionsResponse']['route']['leg']['distance']['text'])
        html.write('</td>')
        html.write('<td>')
        html.write(xmlData['DirectionsResponse']['route']['leg']['duration']['text'])
        html.write('</td>')
        html.write('<td>')
        html.write(xmlData['DirectionsResponse']['route']['leg']['start_address'] + '. ')
        html.write('</td>')
        html.write('<td>')
        html.write(xmlData['DirectionsResponse']['route']['leg']['end_address'] + '. ')
        html.write('</td>')
        html.write('</tr>')
        html.write('</table>')

        html.write('<table border="1" cellpadding="5">')
        html.write('<caption><h3>')
        html.write('Directions')
        html.write('</h3></caption>')

        html.write('<tr>')
        html.write('<th width="5%">')
        html.write('Distance')
        html.write('</th>')
        html.write('<th width="10%">')
        html.write('Duration')
        html.write('</th>')
        html.write('<th width=""75%>')
        html.write('Instructions')
        html.write('</th>')
        html.write('</tr>')

        for i in range(len(xmlData['DirectionsResponse']['route']['leg']['step'])):
            print xmlData['DirectionsResponse']['route']['leg']['step'][i]['distance']['text']
            print xmlData['DirectionsResponse']['route']['leg']['step'][i]['duration']['text']
            print xmlData['DirectionsResponse']['route']['leg']['step'][i]['html_instructions']
            
            html.write('<tr>')
            html.write('<td bgcolor="lightgrey">')
            html.write(xmlData['DirectionsResponse']['route']['leg']['step'][i]['distance']['text'] + ' ')
            html.write('</td>')
            html.write('<td bgcolor="lightgrey">')
            html.write(xmlData['DirectionsResponse']['route']['leg']['step'][i]['duration']['text'] + ' ')
            html.write('</td>')
            html.write('<td bgcolor="lightgrey">')
            html.write(xmlData['DirectionsResponse']['route']['leg']['step'][i]['html_instructions'] + ' ')
            html.write('</td>')
            html.write('</tr>')

        html.write('</table>')

def printDirections(xmlData):

    print xmlData['DirectionsResponse']['status']
    print xmlData['DirectionsResponse']['route']
    print xmlData['DirectionsResponse']['route']['leg']

    print xmlData['DirectionsResponse']['route']['leg']['start_address']
    print xmlData['DirectionsResponse']['route']['leg']['end_address']
    print xmlData['DirectionsResponse']['route']['leg']['distance']['text']
    print xmlData['DirectionsResponse']['route']['leg']['duration']['text']

    for i in range(len(xmlData['DirectionsResponse']['route']['leg']['step'])):
        print xmlData['DirectionsResponse']['route']['leg']['step'][i]['distance']['text']
        print xmlData['DirectionsResponse']['route']['leg']['step'][i]['duration']['text']
        print xmlData['DirectionsResponse']['route']['leg']['step'][i]['html_instructions']

def wayPoints():
    pass

def makeURL(start, end, wayPoints):
    wpString  = ''

    if len(wayPoints) > 0:

        if len(wayPoints) > 1:
            for i in range(len(wayPoints)):
                wpString += 'via:' + wayPoints[i] + '|'
                if i == len(wayPoints)-1:
                    wpString += 'via:' + wayPoints[i]
        else:
            wpString = 'via:' + wayPoints[0]

        url = baseUrl + 'origin=' + start + '&' \
                    + 'destination=' + end + '&' \
                    + 'waypoints=' + wpString + '&' \
                    + 'sensor=' + 'false'
    else:
        url = baseUrl + 'origin=' + start + '&' \
                    + 'destination=' + end + '&' \
                    + 'sensor=' + 'false'
    print url
    return url

def XMLdictionary(xml_Data):
    return xmldict.xml_to_dict(xml_Data)

def parseXML(url):
    xml_p = parse(urllib2.urlopen(url)).getroot()
    return XMLdictionary(xml_p)

if __name__ =='__main__':

    # http://maps.googleapis.com/maps/api/directions/json?origin=Boston,MA&destination=Concord,MA&waypoints=Charlestown,MA|via:Lexington,MA&sensor=false
    waypoint = []
    wp = ''

    startDestination = str(raw_input('Start destination: '))
    endDestination = str(raw_input('End destination: '))

    while wp != 'none':
        wp = str(raw_input('Waypoints enter none otherwise: '))
        if wp != 'none':
            waypoint.append(wp)

    xml_d = parseXML(makeURL(startDestination, endDestination, waypoint))

    #---
    print xml_d
    printDirections(xml_d)
    generateHTML(xml_d)
