import requests

def get_competitions_by_season(base_url, headers, season='2021', date='2021-04-10'):
    """Get competitions for specific season after given date"""
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
                            "IncludeEmptyGroups": True,
                            "Version": 1
                        },
                        "ExecutionMetricsKind": 1
                    }
                }]
            },
            "QueryId": "",
            "ApplicationContext": {
                "DatasetId": "1d2bbb0f-45d4-4b35-97d4-d1731ec3a68e",
                "Sources": [{"ReportId": "7ac5ac0f-c9d0-4cc7-9e8f-1ecacf94583f", "VisualId": "7697ca1c75784b2c0080"}]
            }
        }],
        "cancelQueries": [],
        "modelId": 1338582
    }

    # Update RequestId for this specific request
    headers['RequestId'] = 'ed365db7-c8aa-1f16-d31e-30774d6f52f2'
    
    response = requests.post(f"{base_url}?synchronous=true",
                            headers=headers,
                            json=payload)
    
    competitions = []
    try:
        data = response.json()
        for item in data['results'][0]['result']['data']['dsr']['DS'][0]['PH'][0]['DM0']:
            competitions.append(item['G0'])
    except Exception as e:
        print(f"Error parsing competitions response: {e}")
        
    return competitions
