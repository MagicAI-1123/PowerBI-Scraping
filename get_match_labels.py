import requests
from datetime import datetime, timedelta

def get_match_labels(base_url, headers, season='2021', competition='Allsvenskan', start_date='2021-04-10', end_date='2021-04-11'):
    """Get match labels for specific season, competition and date range"""
    # The payload needs to be sent as a raw string with exact formatting
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
    end_date = (end_date_obj + timedelta(days=1)).strftime('%Y-%m-%d')
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
                                    "Property": "match_label"
                                },
                                "Name": "powerbi.match_label"
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
                                        "In": {
                                            "Expressions": [{
                                                "Column": {
                                                    "Expression": {"SourceRef": {"Source": "p"}},
                                                    "Property": "competition_name"
                                                }
                                            }],
                                            "Values": [[{"Literal": {"Value": f"'{competition}'"}}]]
                                        }
                                    }
                                },
                                {
                                    "Condition": {
                                        "And": {
                                            "Left": {
                                                "Comparison": {
                                                    "ComparisonKind": 2,
                                                    "Left": {
                                                        "Column": {
                                                            "Expression": {"SourceRef": {"Source": "p"}},
                                                            "Property": "match_date_str"
                                                        }
                                                    },
                                                    "Right": {
                                                        "Literal": {"Value": f"datetime'{start_date}T00:00:00'"}
                                                    }
                                                }
                                            },
                                            "Right": {
                                                "Comparison": {
                                                    "ComparisonKind": 3,
                                                    "Left": {
                                                        "Column": {
                                                            "Expression": {"SourceRef": {"Source": "p"}},
                                                            "Property": "match_date_str"
                                                        }
                                                    },
                                                    "Right": {
                                                        "Literal": {"Value": f"datetime'{end_date}T00:00:00'"}
                                                    }
                                                }
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
                "Sources": [{"ReportId": "7ac5ac0f-c9d0-4cc7-9e8f-1ecacf94583f", "VisualId": "eea8656d64076c3ed89a"}]
            }
        }],
        "cancelQueries": [],
        "modelId": 1338582
    }

    headers['RequestId'] = 'df603999-2cad-b21c-586b-eefc0581ab92'
    
    response = requests.post(
        f"{base_url}?synchronous=true",
        headers=headers,
        json=payload
    )
    
    matches = []
    try:
        data = response.json()
        if 'results' in data:
            result = data['results'][0]['result']
            if 'data' in result and 'dsr' in result['data']:
                dsr = result['data']['dsr']
                if 'DS' in dsr and len(dsr['DS']) > 0:
                    for item in dsr['DS'][0]['PH'][0]['DM0']:
                        if 'G0' in item:
                            matches.append({
                                'label': item['G0'],
                                'teams': item['G0'].split('-')
                            })
    except Exception as e:
        print(f"Error parsing match labels response: {e}")
    
    return matches
