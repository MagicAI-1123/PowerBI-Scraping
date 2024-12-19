import requests

def get_seasons(base_url, headers):
    # First request to get seasons
    headers['RequestId'] = '8576e693-6a70-e10b-7c45-1cb8c9991c11'
    payload1 = {
        "version": "1.0.0",
        "queries": [{
            "Query": {
                "Commands": [{
                    "SemanticQueryDataShapeCommand": {
                        "Query": {
                            "Version": 2,
                            "From": [{"Name": "p", "Entity": "powerbi", "Type": 0}],
                            "Select": [
                                {
                                    "Column": {
                                        "Expression": {"SourceRef": {"Source": "p"}},
                                        "Property": "season_name"
                                    },
                                    "Name": "powerbi.season_name"
                                }
                            ],
                            "OrderBy": [{
                                "Direction": 1,
                                "Expression": {
                                    "Column": {
                                        "Expression": {"SourceRef": {"Source": "p"}},
                                        "Property": "season_name"
                                    }
                                }
                            }]
                        },
                        "Binding": {
                            "Primary": {"Groupings": [{"Projections": [0]}]},
                            "DataReduction": {
                                "DataVolume": 3,
                                "Primary": {"Window": {"Count": 1000}}
                            },
                            "Version": 1
                        },
                        "ExecutionMetricsKind": 1
                    }
                }]
            },
            "QueryId": "",
            "ApplicationContext": {
                "DatasetId": "1d2bbb0f-45d4-4b35-97d4-d1731ec3a68e",
                "Sources": [{
                    "ReportId": "7ac5ac0f-c9d0-4cc7-9e8f-1ecacf94583f",
                    "VisualId": "16e2addb4bd8b3da5819"
                }]
            }
        }],
        "cancelQueries": [],
        "modelId": 1338582
    }
    response = requests.post(f"{base_url}?synchronous=true", headers=headers, json=payload1)
    return response.json()
