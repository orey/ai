import os
from pathlib import Path
import re

import sys
sys.path.append('.')
from openai_api_server import AI_Session


CSV_HEADERS = [
    "Contract_ID", "Document_Type", "Signature_Year", "Nation", 
    "Helicopter_Model", "Configuration_Variant", "Contract_Phase", 
    "Total_Unit_Count", "Unit_Acquisition_Price_EUR", "Initial_Spares_Value_EUR", 
    "Tools_GSE_Value_EUR", "Delivery_Date_Lot1", "Delivery_Date_Final", 
    "Warranty_Hours", "Warranty_Years", "Availability_Target_Pct", 
    "Mission_Capable_Rate_Pct", "MTBF_Hours", "MTTR_Hours", 
    "Contract_Type_ISS", "Labor_Rate_Engineer_EUR", "Hourly_Rate_Technician_EUR", 
    "Spare_Parts_Model", "Overhaul_Cycle_Hours", "Inventory_Responsibility", 
    "FSR_Response_Hrs", "Effective_Date", "Initial_Term_Years", 
    "Option_Years_Available", "Option_Exercise_Authority", 
    "LD_Penalty_Percent_Per_Day", "Performance_Penalty_Cap_Percent", 
    "Inflation_Index", "Currency", "Payment_Milestones", 
    "Warranty_Post_Acceptance_Months", "Liability_Cap_EUR", 
    "Governing_Law", "Dispute_Forum", "Security_Classification", 
    "NATO_STANAG_Reference", "Offset_Requirement_Percent", 
    "Export_Control_License_ID", "Engine_Model_Type", "Engine_Manufacturer", 
    "Number_of_Engines", "Takeoff_Power_Horsepower", "ECU_Type", 
    "Avionics_Suite_Vendor", "Avionics_Architecture", "Weapons_Pylons_Count", 
    "Compatible_Weapons_List", "Integrated_Sensor_Type", 
    "Countermeasures_System", "Mission_Computer_Model"
]



SESSION = AI_Session("test")


def extract_keywords_from_file(filepath, top_n=50):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
        params1 = [ 
            "You are a helpful assistant, always answering in json format.",
            f"You are provided with the following keys:\n{CSV_HEADERS}.\n With the following text, find the values corresponding to the keys | {text} |",
            ""
        ]
        response1 = SESSION.ask(*params1, streaming = False)
        print(response1)
        input("wait")
            
    return []



def main():
    # Example usage
    directory = 'C:\\ct\\c\\'  # Change to your directory path
    top_n = 50       # Number of keywords per file

    f_k = {} # {id1: [file : [kw1, kw2, ...]], ... }
    global_keywords = {} # {kw1 : 12, kw2 : 45, ... }
    index = {} # {kw1: [id1,id2,], ...}

    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                print(f"Treating: , id = {count}, {file}", flush=True)
                filepath = os.path.join(root, file)
                keywords = extract_keywords_from_file(filepath, top_n)
                # 1. record file id, file and keywords
                f_k[count] = [file, keywords]
                # 2. count keywords
                for k in keywords:
                    if k in global_keywords:
                        global_keywords[k] += 1
                    else:
                        global_keywords[k] = 1
                # 3 create the index
                for k in keywords:
                    if k in index:
                        index[k].append(count)
                    else:
                        index[k] = [count]
                # 4.go to next file
                count += 1
    print(f"Nb of files treated: {count}, nb of files in f_k: {len(f_k)}")
    print(f"Nb of global keywords: {len(global_keywords)}")
    print(f"Index\n{index}")
    


if __name__ == '__main__':
    main()
    
