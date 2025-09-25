# tests/mock_data.py

MOCK_API_RESPONSE_SINGLE_PAGE = {
    "nextPageToken": None,
    "studies": [
        {
            "protocolSection": {
                "identificationModule": {
                    "nctId": "NCT00000001",
                    "briefTitle": "A Study of Rehabilitation for Spinal Cord Injury",
                    "officialTitle": "Official Title of a Research Study on Post-Injury Physical Therapy",
                    "organization": {
                        "fullName": "National Institute of Health",
                        "class": "NIH"
                    }
                },
                "statusModule": {
                    "overallStatus": "RECRUITING",
                    "lastUpdatePostDateStruct": {
                        "date": "2024-09-25",
                        "type": "ACTUAL"
                    }
                },
                "sponsorCollaboratorsModule": {
                    "leadSponsor": {
                        "name": "Acme Pharmaceuticals",
                        "class": "INDUSTRY"
                    }
                },
                "descriptionModule": {
                    "briefSummary": "This study investigates the effectiveness of physical rehabilitation techniques in patients with spinal cord injuries.",
                    "detailedDescription": "A detailed, placebo-controlled clinical trial..."
                },
                "conditionsModule": {
                    "conditions": ["Spinal Cord Injuries", "Rehabilitation"]
                },
                "designModule": {
                    "studyType": "INTERVENTIONAL"
                },
                "armsInterventionsModule": {
                    "armGroups": [
                        {
                            "label": "Experimental",
                            "type": "EXPERIMENTAL",
                            "description": "Patients will receive daily physical therapy sessions."
                        }
                    ],
                    "interventions": [
                        {
                            "type": "BEHAVIORAL",
                            "name": "Physical Therapy",
                            "description": "Daily sessions focusing on muscle strengthening and mobility.",
                            "armGroupLabels": ["Experimental"]
                        }
                    ]
                },
                "eligibilityModule": {
                    "eligibilityCriteria": "Inclusion criteria: Age 18-65. Exclusion criteria: Pre-existing mobility issues.",
                    "sex": "ALL",
                    "minimumAge": "18 Years"
                },
                "contactsLocationsModule": {
                    "overallOfficials": [
                        {
                            "name": "John Doe",
                            "affiliation": "University of Research",
                            "role": "PRINCIPAL_INVESTIGATOR"
                        }
                    ],
                    "locations": [
                        {
                            "facility": "Research Hospital",
                            "city": "Boston",
                            "state": "Massachusetts",
                            "country": "United States"
                        }
                    ]
                }
            }
        }
    ],
    "totalCount": 1
}

# This data can be used to simulate a multi-page response.
# The first page has a nextPageToken, and the second does not.
MOCK_API_RESPONSE_MULTI_PAGE_1 = {
    "nextPageToken": "A_VALID_TOKEN_STRING",
    "studies": [
        {
            "protocolSection": {
                "identificationModule": {
                    "nctId": "NCT00000002",
                    "briefTitle": "Study on Occupational Therapy for Brain Injuries",
                }
            }
        }
    ]
}

MOCK_API_RESPONSE_MULTI_PAGE_2 = {
    "nextPageToken": None,
    "studies": [
        {
            "protocolSection": {
                "identificationModule": {
                    "nctId": "NCT00000003",
                    "briefTitle": "Rehabilitation Techniques for Post-Stroke Patients",
                }
            }
        }
    ]
}
