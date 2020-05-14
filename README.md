# IBM Cloud Brokerage Service - API Automation for core components
-----------------------------
This is the python code for IBM Cloud Brokerage Service core components.

To clone the Automation Git Repository using git, run the command
"git clone https://github.ibm.com/cloudMatrix-CAM/cam-core-api-automation.git".

### Features
1. All values are parameterized
2. Slack Integration - Test execution Reports are posted to Slack
3. Detailed Console Logs
4. Detailed logs report

### Pre-requisites
1. Python 2.7.10

### Before running the CAM UI Tests
---
```
a. Make sure settings.conf updated with slack channel details[Update the channel if you are running the tests for test development]
```

### How to Run CAM Tests
---
1. Run 'python auto_run.py <env> <api_key> <build_version>'
```
python cam_run.py qademo6 grav123 build_1945
```
2. Results will be displayed on configured slack channel[#cldmx-cam-testresult] and on console

### How to Add API Tests
---
```
a. Add test-cases in `api_tests.py`, use @assignOrder() annotation to assign a order and use client methods in `cam_client.py`to make api calls

b. Update the test category in api_client.py

Example :
API for getting the cost summary is : <env>:3277/camapi-1/costs/summary/<date>. Define the following client method in `cam_client.py`.


def get_cost_summary_data(self,date):                     #This method will be called in tests
    url = '%s/costs/summary/%s' % (self.endpoint,date)    #This is the API with customized parameter
    status, resp = self.get(url, headers=self.headers)    
    logger.info(pprint.pformat(resp))                     
    return status, resp

Following tests can be defined in `api_tests` with valid and invalid scenarios. Note that, for one API, we can define 'n' tests.

@assignOrder(44)
def CM_21991_test_get_cost_summary_valid_data(self):
    resp, body = self.cam_client.get_cost_summary_data(CostInvoiceEndDate)
    print resp
    passed = assertEqual(resp, 200)
    global status
    status['CAM-APITest'] = passed
    return passed

@assignOrder(45)
def CM_21991_test_get_cost_summary_invalidURL(self):
    resp, body = self.cam_client.get_invalidURL_data("costs/summaryinvalid/2016-08-01")
    print resp
    passed = assertEqual(resp, 400)
    global status
    status['CAM-APITest'] = passed
    return passed

@assignOrder(46)
def CM_21991_test_get_cost_summary_invalidDate(self):
    passed = False
    resp, body = self.cam_client.get_cost_summary_data("Invalid")
    print resp
    passOfResponseCode = assertEqual(resp, 400)
    if(passOfResponseCode):
        passofDate = "Invalid Path variable - date should be in format yyyy-MM-dd." == body["message"]
        if passOfResponseCode and passofDate:
            passed = True
    global status
    status['CAM-APITest'] = passed
    return passed
```

### Example automated scenario - Tagging life cycle
```
Search and find tags - First search and validate the existance of the Tag key and value
Create tags - Create the Tag key and value
Search and find tags - Validate that created Tag exists
Apply tags  - Apply Tags to assets
Search and find tags - Validate that created Tag associated with the assets
Remove tags - Remove the Tag from associated assets
Search and find tags - - Validate that associated Tag is removed from the assets
```
### How to debug or run a specific test
Configure the test_case parameter in settings.conf, with required tests
Example :
```
test_case=CAM_test_data,CM_21698_test_get_cost_in_month_date_invalidDate
```
