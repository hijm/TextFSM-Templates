import devpackage.DataProvider as DeviceDataProvider
import simplejson

dp = DeviceDataProvider.DeviceDataProvider(context)
ctype = DeviceDataProvider.CollectionType

def main():
    dp.job_execution_log("Executing the show interfaces summary script")
    
    # Capture script inputs
    #inputs = context.get("INPUTS")
    #parsed_json = simplejson.loads(inputs)
	
    pre_result = dp.get_fields_as_dict_list("show interfaces summary", ctype.PRE, "UP")
    post_result = dp.get_fields_as_dict_list("show interfaces summary", ctype.POST, "UP")
    print(pre_result)
    print(post_result)
	
    dp.job_execution_log("Analyzing show interfaces summary")
    
    # Get pre from command results
    preUP = ""
    for x in pre_result:
        preUP = x.get("UP")
        break

    # Get post from command results
    postUP = ""
    for x in post_result:
        postUP = x.get("UP")
        break
    
    dp.job_execution_log("UP Number in command " + preUP)
    dp.job_execution_log("UP Number in command " + postUP)

    # Determine post results
    passmsg = preUP + " less than or equal " + postUP
    errmsg = preUP + " grather than " + postUP
    if preUP <= postUP:
        dp.add_post_status_field("All Types", preUP, passmsg, "Passed")
        dp.publish_post_status(True, "Analysis Check passed")
    elif preUP > postUP:
        dp.add_post_status_field("All Types", preUP, errmsg, "Failed")
        dp.publish_post_status(False, "Analysis Check failed")
		
    json = dp.publish_status()
    return json