import requests
from datetime import datetime, timedelta

def get_player_statistics(base_url, headers, season='2021', competition='Allsvenskan', start_date='2021-04-10', end_date='2021-04-11', match_label='Örebro-IFK Göteborg'):
    """Get detailed player statistics for a specific match"""
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
                            "Select": [
                                {
                                    "Aggregation": {
                                        "Expression": {
                                            "Column": {
                                                "Expression": {"SourceRef": {"Source": "p"}},
                                                "Property": "team_name"
                                            }
                                        },
                                        "Function": 3
                                    },
                                    "Name": "Min(powerbi.team_name)"
                                },
                                {
                                    "Aggregation": {
                                        "Expression": {
                                            "Column": {
                                                "Expression": {"SourceRef": {"Source": "p"}},
                                                "Property": "distance"
                                            }
                                        },
                                        "Function": 0
                                    },
                                    "Name": "Sum(powerbi.distance)"
                                },
                                {
                                    "Aggregation": {
                                        "Expression": {
                                            "Column": {
                                                "Expression": {"SourceRef": {"Source": "p"}},
                                                "Property": "highspeedruns_distance"
                                            }
                                        },
                                        "Function": 0
                                    },
                                    "Name": "Sum(powerbi.highspeedruns_distance)"
                                },
                                {
                                    "Aggregation": {
                                        "Expression": {
                                            "Column": {
                                                "Expression": {"SourceRef": {"Source": "p"}},
                                                "Property": "sprints_distance"
                                            }
                                        },
                                        "Function": 0
                                    },
                                    "Name": "Sum(powerbi.sprints_distance)"
                                },
                                {
                                    "Aggregation": {
                                        "Expression": {
                                            "Column": {
                                                "Expression": {"SourceRef": {"Source": "p"}},
                                                "Property": "highspeedruns_count"
                                            }
                                        },
                                        "Function": 0
                                    },
                                    "Name": "Sum(powerbi.highspeedruns_count)"
                                },
                                {
                                    "Aggregation": {
                                        "Expression": {
                                            "Column": {
                                                "Expression": {"SourceRef": {"Source": "p"}},
                                                "Property": "sprints_count"
                                            }
                                        },
                                        "Function": 0
                                    },
                                    "Name": "Sum(powerbi.sprints_count)"
                                },
                                {
                                    "Aggregation": {
                                        "Expression": {
                                            "Column": {
                                                "Expression": {"SourceRef": {"Source": "p"}},
                                                "Property": "max_speed_kmh"
                                            }
                                        },
                                        "Function": 3
                                    },
                                    "Name": "Min(powerbi.max_speed_kmh)"
                                },
                                {
                                    "Aggregation": {
                                        "Expression": {
                                            "Column": {
                                                "Expression": {"SourceRef": {"Source": "p"}},
                                                "Property": "max_speed_time"
                                            }
                                        },
                                        "Function": 3
                                    },
                                    "Name": "Min(powerbi.max_speed_time)"
                                },
                                {
                                    "Aggregation": {
                                        "Expression": {
                                            "Column": {
                                                "Expression": {"SourceRef": {"Source": "p"}},
                                                "Property": "max_speed_time_period"
                                            }
                                        },
                                        "Function": 3
                                    },
                                    "Name": "Min(powerbi.max_speed_time_period)"
                                },
                                {
                                    "Column": {
                                        "Expression": {"SourceRef": {"Source": "p"}},
                                        "Property": "Player Name"
                                    },
                                    "Name": "powerbi.Player Name"
                                },
                                {
                                    "Measure": {
                                        "Expression": {"SourceRef": {"Source": "p"}},
                                        "Property": "Playing Time"
                                    },
                                    "Name": "powerbi.Total Playing Time"
                                },
                                {
                                    "Measure": {
                                        "Expression": {"SourceRef": {"Source": "p"}},
                                        "Property": "Total HI Distance"
                                    },
                                    "Name": "powerbi.Total HI Distance"
                                }
                            ],
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
                                },
                                {
                                    "Condition": {
                                        "In": {
                                            "Expressions": [{
                                                "Column": {
                                                    "Expression": {"SourceRef": {"Source": "p"}},
                                                    "Property": "match_label"
                                                }
                                            }],
                                            "Values": [[{"Literal": {"Value": f"'{match_label}'"}}]]
                                        }
                                    }
                                }
                            ],
                            "OrderBy": [{
                                "Direction": 2,
                                "Expression": {
                                    "Aggregation": {
                                        "Expression": {
                                            "Column": {
                                                "Expression": {"SourceRef": {"Source": "p"}},
                                                "Property": "distance"
                                            }
                                        },
                                        "Function": 0
                                    }
                                }
                            }]
                        },
                        "Binding": {
                            "Primary": {"Groupings": [{"Projections": [0,1,2,3,4,5,6,7,8,9,10,11]}]},
                            "DataReduction": {"DataVolume": 3, "Primary": {"Window": {"Count": 500}}},
                            "Version": 1
                        },
                        "ExecutionMetricsKind": 1
                    }
                }]
            },
            "QueryId": "",
            "ApplicationContext": {
                "DatasetId": "1d2bbb0f-45d4-4b35-97d4-d1731ec3a68e",
                "Sources": [{"ReportId": "7ac5ac0f-c9d0-4cc7-9e8f-1ecacf94583f", "VisualId": "cdeff1eab52190d86ac2"}]
            }
        }],
        "cancelQueries": [],
        "modelId": 1338582
    }

    headers['RequestId'] = '21203bfc-4312-ec4a-3ffb-ca888b147c75'
    response = requests.post(
        f"{base_url}?synchronous=true",
        headers=headers,
        json=payload
    )
    
    players = []
    previous_player = {
        'Player Name': None,
        'Team': None,
        'Distance': None,
        'HS Distance': None,
        'Sprint Distance': None,
        'HS Runs': None,
        'Sprints': None,
        'Max Speed': None,
        'Timestamp': None,
        'Period': None,
        'Playing Time': None,
        'HI Distance': None
    }
    try:
        data = response.json()
        keys = ['Player Name', 'Team', 'Distance', 'HS Distance', 'Sprint Distance', 'HS Runs',
                    'Sprints', 'Max Speed', 'Timestamp', 'Period', 'Playing Time', 'HI Distance']
        if 'results' in data:
            result = data['results'][0]['result']
            if 'data' in result and 'dsr' in result['data']:
                dsr = result['data']['dsr']
                if 'DS' in dsr and len(dsr['DS']) > 0:
                    for item in dsr['DS'][0]['PH'][0]['DM0']:
                        # Get the schema info
                        schema = item.get('S', [])
                        
                        # Get the values array
                        values = item.get('C', [])
                        R = item.get('R', 0)  # Default to 4095 if R is not present
                        
                        # Convert R value to a binary mask, right-padded with zeros if needed
                        r_binary = format(R, '012b')[::-1]
                        # Note: 4095 is 111111111111 in binary (12 ones)
                        
                        print(r_binary)
                        
                        player = previous_player.copy()
                        
                        value_index = 0
                        for i, header in enumerate(keys):
                            if r_binary[i] == '0':
                                # Value exists in the values array
                                player[header] = values[value_index]
                                value_index += 1
                        
                        previous_player = player.copy()
                        
                        # Filter out None values
                        # player = {k: v for k, v in player.items() if v is not None}
                        players.append(player)
        
        headers = ['Player Name', 'Team', 'Playing Time', 'Distance', 'HS Distance', 'HS Runs',
                    'Sprint Distance', 'Sprints', 'Max Speed', 'Timestamp', 'Period', 'HI Distance']
        # Sort players by distance in descending order
        players.sort(key=lambda x: x.get('Distance', 0), reverse=True)
        
        
        for player in players:
            row = [str(player.get(h, '')) for h in headers]
            print('\t'.join(row))
            
    except Exception as e:
        print(f"Error parsing player statistics response: {e}")
        print(f"Raw response: {response.text}")
        
    return players
