import os
import glob
import pandas as pd
import xmltodict
from Evtx.Evtx import Evtx

def parse_evtx_directory_to_dataframe(directory_path):
    print(f"[*] Processing directory: {directory_path}")
    records = []
    evtx_files = glob.glob(os.path.join(directory_path, "**/*.evtx"), recursive=True)
    
    for filepath in evtx_files:
        print(f"[*] Parsing: {filepath}")
        try:
            with Evtx(filepath) as log:
                for record in log.records():
                    try:
                        xml_string = record.xml()
                        doc = xmltodict.parse(
                            xml_string, 
                            process_namespaces=True, 
                            namespaces={'http://schemas.microsoft.com/win/2004/08/events/event': None}
                        )
                        system_data = doc['Event']['System']
                        
                        row = {
                            'EventID': system_data.get('EventID'),
                            'TimeCreated': system_data['TimeCreated'].get('@SystemTime'),
                            'Computer': system_data.get('Computer'),
                            'Channel': system_data.get('Channel'),
                            'SourceFile': os.path.basename(filepath),
                            'RawXML': xml_string 
                        }
                        
                        if isinstance(row['EventID'], dict):
                            row['EventID'] = row['EventID'].get('#text')

                        records.append(row)
                    except Exception:
                        continue
        except Exception as e:
            print(f"[!] Failed to open {filepath}: {e}")
            continue

    df = pd.DataFrame(records)
    return df

if __name__ == "__main__":
    target_dir = "EVTX-ATTACK-SAMPLES/Discovery"
    df = parse_evtx_directory_to_dataframe(target_dir)
    
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)
    
    if not df.empty:
        print("\n[*] Transformation result sample:")
        print("-" * 80)
        print(df.drop(columns=['RawXML']).head(10).to_string(index=False))
        print("-" * 80)
        print(f"[*] Total dimensions: {df.shape[0]} rows, {df.shape[1]} columns.")
    else:
        print("[!] DataFrame is empty.")
