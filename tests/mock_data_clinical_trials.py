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
                        "date": "2024-01-25",
                        "type": "ACTUAL"
                    },
                    "primaryCompletionDate": "2025-09-25",
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

MOCK_API_RESPONSE_SUPER_HAPPY = [
  {
    "protocolSection": {
      "identificationModule": {
        "nctId": "NCT00000001",
        "briefTitle": "A Phase III Trial for New Immunotherapy Drug",
        "organization": {
          "fullName": "Fallback University Org Name"
        }
      },
      "sponsorCollaboratorsModule": {
        "leadSponsor": {
          "name": "Global Pharma Research Institute",
          "class": "INDUSTRY"
        }
      },
      "statusModule": {
        "primaryCompletionDateStruct": {
          "date": "2025-09-25",
          "type": "ESTIMATED"
        },
        "completionDateStruct": {
          "date": "2026-01-31",
          "type": "ESTIMATED"
        }
      },
      "descriptionModule": {
        "briefSummary": "This study aims to assess the efficacy and safety of a novel immunotherapy drug in patients with advanced cancer."
        }
    }
  }
]

MOCK_API_RESPONSE_NO_ORG = [
  {
    "protocolSection": {
      "identificationModule": {
        "nctId": "NCT00000002",
        "briefTitle": "A Study of Gene Therapy in Pediatric Patients",
        "organization": {
          "fullName": "Pediatric Health Consortium"
        }
      },
      "sponsorCollaboratorsModule": {
      },
      "statusModule": {
        "primaryCompletionDateStruct": {
          "date": "2024-12-31"
        }
      },
      "descriptionModule": {
        "briefSummary": "Investigating a novel gene therapy approach."
      }
    }
  }
]

MOCK_API_RESPONSE_NO_PRIMARY_DATE = [
  {
    "protocolSection": {
      "identificationModule": {
        "nctId": "NCT00000003",
        "briefTitle": "Dietary Intervention for Metabolic Syndrome",
        "organization": {
          "fullName": "Fallback Org Name"
        }
      },
      "sponsorCollaboratorsModule": {
        "leadSponsor": {
          "name": "Academic Medical Center"
        }
      },
      "statusModule": {
        "completionDateStruct": {
          "date": "2027-06-15"
        }
      },
      "descriptionModule": {
        "briefSummary": "Assessing the impact of a low-carb diet on patients with metabolic syndrome."
      }
    }
  }
]

MOCK_API_RESPONSE_SHITTY_DATA = [
  {
    "protocolSection": {
      "identificationModule": {
        "briefTitle": "A Study with Minimal Information"
      },
      "statusModule": {
      },
      "descriptionModule": {
        "briefSummary": "This summary is present."
      }
    }
  }
]

MOCK_JSONL_CONTENT = (
    '{"id": "study1", "data": "A"}\n'
    '{"id": "study2", "data": "B"}'
)

MOCK_API_RESPONSE_MAIN = {
    "studies": [
        {
            "protocolSection": {
                "identificationModule": {
                    "nctId": "NCT99999999",
                    "briefTitle": "Integrated Pipeline Test Study",
                },
                "sponsorCollaboratorsModule": {
                    "leadSponsor": {
                        "organizationName": "Integration Corp"
                    }
                },
                "statusModule": {
                    "primaryCompletionDateStruct": {
                        "date": "2025-10-31"
                    }
                },
                "descriptionModule": {
                    "briefSummary": "A test to verify all components are working together."
                }
            }
        }
    ]
}

EXPECTED_TRANSFORMED_DATA = [{
    'name': 'Integrated Pipeline Test Study',
    'org': 'Integration Corp',
    'desc': 'A test to verify all components are working together.',
    'deadline': '2025-10-31',
    'link': 'https://clinicaltrials.gov/study/NCT99999999',
    'isGrant': False
}]
