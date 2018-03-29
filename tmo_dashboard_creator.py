import json
import requests

# Global Variablesht
gbl_protocol = "https://"
gbl_port = "443"

# Format is username@account
gbl_username = ""
gbl_password = ""
gbl_dashboard_name = "KEVIN_FULL_DASHBOARD"
#gbl_username = "user1@customer1"
#gbl_password = "App3!"
#gbl_dashboard_name = "KEVINB_TEST"
gbl_account_name = "tmo-npe"
gbl_saas_base_url = ".saas.appdynamics.com:"

gbl_application_url = gbl_protocol + gbl_account_name + gbl_saas_base_url + gbl_port + "/controller/rest/applications?output=json"

print("Starting Application..")
print("Script Params:")
print("\tUsername      : " + gbl_username)
print("\tDashboard Name: " + gbl_dashboard_name)
print("\tAccount Name  : " + gbl_account_name)
# Stores the application name and the app id
gbl_app_name_dict = {}
# Get the applications
r = requests.get(gbl_application_url, auth=(gbl_username, gbl_password))
jsonPayload = json.loads(r.text)



# Store the name so it can be sorted.
sorted_name_list = []


print("\nFound " + str(len(jsonPayload)) + " Apps..")
# loop through the app names and sort it..
for app_object in jsonPayload:
    app_name = app_object["name"]
    app_id = app_object["id"]
    gbl_app_name_dict[app_name] = app_id
    sorted_name_list.append(app_name)

# Sort the application names in alphabetical order.
sorted_name_list.sort()

#
dashboard_object = {
            "schemaVersion": None,
            "dashboardFormatVersion": "4.0",
            "name": "" + gbl_dashboard_name + "",
            "description": None,
            "properties": None,
            "templateEntityType": "APPLICATION_COMPONENT_NODE",
            "associatedEntityTemplates": None,
            "minutesBeforeAnchorTime": -1,
            "startDate": None,
            "endDate": None,
            "refreshInterval": 120000,
            "backgroundColor": 15395562,
            "color": 15395562,
            "height": 10000,
            "width": 1920,
            "canvasType": "CANVAS_TYPE_GRID",
            "layoutType": "",
            "widgetTemplates":[],
            "template": False,
            "warRoom": False
        }

num_apps = len(sorted_name_list)
app_counter = 0

x_coordinate = 0
y_coordinate = 0
widget_counter = 0
expression_payload = None

global_tier_counter = 0
# THIS FOR CREATING EXPRESSION_OBJECTS
def addExpression(obj, tier_counter, num_total_tiers,json_object):
    if "expression1" in obj.keys():

        addExpression(obj["expression1"], tier_counter, num_total_tiers, json_object)
    else:
            if tier_counter == (num_total_tiers - 3):
                obj["expression1"] = newTemplateObject()
                obj["expression1"]["REPLACE_ME"] = json_object
            elif tier_counter == (num_total_tiers - 2):
                obj["expression2"] = json_object
            else:
                 obj["expression1"] = newTemplateObject()
                 obj["expression1"]["expression2"] = json_object


def newTemplateObject():
    t = {
        "metricExpressionType": "Boolean",
        "operator": {
            "type": "PLUS"
        },
    }
    return t


for sorted_app_name in sorted_name_list:
    obj = {}

    #if sorted_app_name == "Billing":
    #    print("STOP")
    # Get the AppId..This is needed to look up the tiers.
    app_id = str(gbl_app_name_dict[sorted_app_name])


    #CFS-Credit-Origination-MLAB01
    tier_rest_url = gbl_protocol + gbl_account_name + gbl_saas_base_url + gbl_port + "/controller/rest/applications/" + sorted_app_name + "/tiers?output=json"

    #'824'
    print(sorted_app_name)
    tier_counter = 0
    r = requests.get(tier_rest_url, auth=(gbl_username, gbl_password))
    tier_payload = json.loads(r.text)
    tier_json_payload = []



    # This is for the x and y positioning
    mod = widget_counter % 2

    if mod == 0:
        widget_counter +=1
        x_coordinate = 0
    elif mod == 1:
        widget_counter += 1
        x_coordinate = 5


    #print("\tCOORDINATES: x=" + str(x_coordinate) + " y=" + str(y_coordinate))
    #if app_counter == 4:
    #    print("STOP")

    # This means we are on the second row..


    graph_widget_object = {
            "widgetType": "GraphWidget",
            "title": "" + sorted_app_name + " Total Agents",
            "height": 3,
            "width": 5,
            "minHeight": 0,
            "minWidth": 0,
            "x": x_coordinate,
            "y": y_coordinate,
            "label": None,
            "description": None,
            "drillDownUrl": None,
            "useMetricBrowserAsDrillDown": True,
            "drillDownActionType": None,
            "backgroundColor": 16777215,
            "backgroundColors": None,
            "backgroundColorsStr": "16777215,16777215",
            "color": 4210752,
            "fontSize": 12,
            "useAutomaticFontSize": False,
            "borderEnabled": False,
            "borderThickness": 0,
            "borderColor": 14408667,
            "backgroundAlpha": 1,
            "showValues": False,
            "formatNumber": None,
            "numDecimals": 0,
            "removeZeros": None,
            "compactMode": False,
            "showTimeRange": False,
            "renderIn3D": False,
            "showLegend": None,
            "legendPosition": "POSITION_BOTTOM",
            "legendColumnCount": 1,
            "startTime": None,
            "endTime": None,
            "minutesBeforeAnchorTime": 15,
            "isGlobal": True,
            "propertiesMap": None,
            "dataSeriesTemplates": [],
            "verticalAxisLabel": None,
            "hideHorizontalAxis": None,
            "horizontalAxisLabel": None,
            "axisType": "LINEAR",
            "stackMode": None,
            "multipleYAxis": None,
            "customVerticalAxisMin": None,
            "customVerticalAxisMax": None,
            "showEvents": None,
            "interpolateDataGaps": False,
            "showAllTooltips": None,
            "staticThresholdList": [],
            "eventFilterTemplate": None
        }

    # This means we are on the second row..
    if widget_counter == 2:
        x_coordinate = 0
        y_coordinate += 3
        widget_counter = 0



    app_agent_graphic_object = {
                    "seriesType": "LINE",
                    "metricType": "OTHER",
                    "showRawMetricName": False,
                    "colorPalette": None,
                    "name": "Series 1",
                    "metricMatchCriteriaTemplate": {
                        "entityMatchCriteria": None,

                        "rollupMetricData": False,
                        "expressionString": "",
                        "useActiveBaseline": False,
                        "sortResultsAscending": False,
                        "maxResults": 20,
                        "evaluationScopeType": None,
                        "baselineName": None,
                        "applicationName": "" + sorted_app_name + "",
                        "metricDisplayNameStyle": "DISPLAY_STYLE_AUTO",
                        "metricDisplayNameCustomFormat": None
                    },
                    "axisPosition": "LEFT"
                }

    # This is the total number of tiers in the app
    num_total_tiers = 0
    for object in tier_payload:
        if object["name"] == "bill_charges_ms_v1_appdynamics":
            print("STOP")
        if object["numberOfNodes"] > 0:
            tier_json_payload.append(object)
            num_total_tiers += 1

    num_total_tiers = len(tier_json_payload)
    print("\t Found " + str(num_total_tiers) + "tiers")

    if num_total_tiers == 0:
        dashboard_object["widgetTemplates"].append(graph_widget_object)
    # used to store the string to add up the entities {expression1} + {expression2} etc..
    expression_string = ""
    app_counter += 1
    expression_holder = []

    for tier_object in tier_json_payload:
        tier_name = tier_object["name"]

        expression_display_name = "a" + str(tier_counter + 1)
       # expression_display_name = tier_name
        # Hacky but entity does not need a "+" in front of it.
        if tier_counter == 0:
            expression_string = "{" + expression_display_name + "}"
        else:
            expression_string += "+{" + expression_display_name + "}"
        # Create the expression payload which uses the tier name to grab a tier and it's app availability

        expression_payload = {
            "metricExpressionType": "Absolute",
            "functionType": "VALUE",
            "displayName": "" + expression_display_name + "",
            "inputMetricText": False,
            "inputMetricPath": None,
            "metricPath": "Application Infrastructure Performance|" + tier_name + "|Agent|App|Availability",
            "scopeEntity": {
                "applicationName": "" + sorted_app_name + "",
                "entityName": "" + tier_name + "",
                "entityType":"APPLICATION_COMPONENT",
                "scopingEntityType": None,
                "scopingEntityName": None,
                "subtype": None
            }
        }

        # THIS IS REALLY GROSS CODING
        if num_total_tiers <= 3 and num_total_tiers > 0:
            if tier_counter == 0:
                obj["expression1"] = expression_payload
                if num_total_tiers == 1:
                    app_agent_graphic_object["metricMatchCriteriaTemplate"]["metricExpressionTemplate"] = {}
                    app_agent_graphic_object["metricMatchCriteriaTemplate"]["metricExpressionTemplate"] = expression_payload
            elif tier_counter == 1:
                obj["expression2"] = expression_payload

                if num_total_tiers == 2:
                    app_agent_graphic_object["metricMatchCriteriaTemplate"]["metricExpressionTemplate"] = {}
                    app_agent_graphic_object["metricMatchCriteriaTemplate"]["metricExpressionTemplate"] = obj
            elif tier_counter == 2:
                three_tier_obj = {}
                three_tier_obj["expression1"] = newTemplateObject()
                three_tier_obj["expression1"]["expression1"] = obj["expression1"]
                three_tier_obj["expression1"]["expression2"] = obj["expression2"]
                app_agent_graphic_object["metricMatchCriteriaTemplate"]["metricExpressionTemplate"] = {}
                app_agent_graphic_object["metricMatchCriteriaTemplate"]["metricExpressionTemplate"] = three_tier_obj
                app_agent_graphic_object["metricMatchCriteriaTemplate"]["metricExpressionTemplate"][
                "expression2"] = expression_payload
        else:
            if tier_counter == (num_total_tiers - 1):
                obj_str = json.dumps(obj)
                new_str = obj_str.replace("REPLACE_ME","expression1")
                obj = json.loads(new_str)
                app_agent_graphic_object["metricMatchCriteriaTemplate"]["metricExpressionTemplate"] = {}
                app_agent_graphic_object["metricMatchCriteriaTemplate"]["metricExpressionTemplate"] = obj
                app_agent_graphic_object["metricMatchCriteriaTemplate"]["metricExpressionTemplate"]["expression2"] = expression_payload
            else:
                addExpression(obj, tier_counter, num_total_tiers,expression_payload)

        tier_counter += 1
        if num_total_tiers == tier_counter:
            if num_total_tiers > 1:
                app_agent_graphic_object["metricMatchCriteriaTemplate"]["expressionString"] = expression_string
                app_agent_graphic_object["metricMatchCriteriaTemplate"]["metricExpressionTemplate"][
                    "metricExpressionType"] = "Boolean"
                app_agent_graphic_object["metricMatchCriteriaTemplate"]["metricExpressionTemplate"]["operator"] = {
                    "type": "PLUS"
                }
                graph_widget_object["dataSeriesTemplates"].append(app_agent_graphic_object)
                dashboard_object["widgetTemplates"].append(graph_widget_object)
                #if app_counter == 20:
                 #   print(json.dumps(dashboard_object, indent=3))
                 #   print("STOP")
            else:
                graph_widget_object["dataSeriesTemplates"].append(app_agent_graphic_object)
                dashboard_object["widgetTemplates"].append(graph_widget_object)
                #if app_counter == 20:
                #   print(json.dumps(dashboard_object,indent=3))
                #    print("STOP")

print("\n Script Finished!")
file_name = gbl_dashboard_name + "_dashboard.json"
print("Writing Output to file: " + file_name)
json_file_dump = open(file_name,"w")
json_file_dump.write(json.dumps(dashboard_object,indent=2))
print("\nAll Done!")














