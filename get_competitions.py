import requests

def get_competitions(base_url, headers, season='2021', date='2021-04-10'):
    """Get available competitions for given season and date"""
    payload = {
        "version": "1.0.0",
        "queries": [{
            "Query": {
                "Commands": [{
                    "SemanticQueryDataShapeCommand": {
                        "Query": {
                            "Version": 2,
                            "From": [{"Name": "p", "Entity": "powerbi", "Type": 0}],
                            "Select": [{
                                "Column": {
                                    "Expression": {"SourceRef": {"Source": "p"}},
                                    "Property": "competition_name"
                                },
                                "Name": "powerbi.competition_name"
                            }],
                            "Where": [
                                {
                                    "Condition": {
                                        "In": {
                                            "Expressions": [{
                                                "Column": {
                                                    "Expression": {"SourceRef": {"Source": "p"}},
                                                    "Property": "season_name"
                                                }
                                            }],
                                            "Values": [[{"Literal": {"Value": f"'{season}'"}}]]
                                        }
                                    }
                                },
                                {
                                    "Condition": {
                                        "Comparison": {
                                            "ComparisonKind": 2,
                                            "Left": {
                                                "Column": {
                                                    "Expression": {"SourceRef": {"Source": "p"}},
                                                    "Property": "match_date_str"
                                                }
                                            },
                                            "Right": {
                                                "Literal": {"Value": f"datetime'{date}T00:00:00'"}
                                            }
                                        }
                                    }
                                }
                            ]
                        },
                        "Binding": {
                            "Primary": {"Groupings": [{"Projections": [0]}]},
                            "DataReduction": {"DataVolume": 3, "Primary": {"Window": {}}},
                            "Version": 1
                        }
                    }
                }]
            }
        }]
    }
    
    response = requests.post(f"{base_url}?synchronous=true", 
                            headers=headers,
                            json=payload)
    
    data = response.json()
    competitions = []
    try:
        for item in data['results'][0]['result']['data']['dsr']['DS'][0]['PH'][0]['DM0']:
            competitions.append(item['G0'])
    except:
        print("Error parsing competitions response")
        
    return competitions
