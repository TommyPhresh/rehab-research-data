'''
Test grants.gov data source
'''
import sys, os
# The path to packages on the C: drive
c_path = 'C:\\Users\\ThomasRich\\AppData\\Local\\Packages\\PythonSoftwareFoundation.python.3.13_qbz5n2kfra8p0\\localcache\\local-packages\\Python313\\site-packages'

# Add the path to the Python system path
if c_path not in sys.path:
    sys.path.append(c_path)

import unittest
from unittest.mock import patch, Mock, call
import json
from datetime import datetime

from scripts.pull_grants import METADATA

MOCK_GRANT_NEW_1 = {"id": "360499", "number": "HHS-2026-ACL-NIDILRR-REGE-0212", "title": "Rehabilitation Engineering Research Centers (RERC) Program: RERC on AI-Driven Assistive And Rehabilitation Technologies", "agencyCode": "HHS-ACL", "agency": "Administration for Community Living", "openDate": "09/05/2025", "closeDate": "", "oppStatus": "forecasted", "docType": "forecast", "cfdaList": ["93.433"]}
MOCK_GRANT_NEW_2 = {"id": "360527", "numbers": "HHS-2026-ACL-NIDILRR-IFST-0206", "title": "Field Initiated Projects Program: Minority-Serving Institutions (MSI) - Development", "agencyCode": "HHS-ACL", "agency": "Administration for Community Living", "openDate": "09/05/2025", "closeDate": "", "oppStatus": "forecasted", "docType": "forecasted", "cfdaList": ["93.433"]}
MOCK_GRANT_OLD = {"id": "360559", "number": "ED-GRANTS-091225-001", "title": "Office of Elementary and Secondary Education (OESE): Innovation and Early Learning Programs: Education Innovation and Research (EIR) Program Expansion Grants Assistance Listing Number 84.411A", "agencyCode": "ED", "agency": "Department of Education", "openDate": "03/07/2021", "closeDate": "10/14/2025", "oppStatus": "posted", "docType": "synopsis", "cfdaList": ["84.411"]}
MOCK_GRANT_BORDER = {"id": "314279", "number": "95332419N0001", "title": "Partnerships with MCC Program", "agencyCode": "MCC", "agency": "Millennium Challenge Corporation", "openDate": "03/14/2024", "closeDate": "03/31/2027", "oppStatus": "posted", "docType": "synopsis", "cfdaList": ["85.002"]}
MOCK_RESPONSE_PG1 = {
            "errorcode": 0, "msg": "Webservice Succeeds", "token": "gfiobrgobuwjfeiuwdfsdbai",
            "data": {
                "searchParams": {"resultType": "json", "searchOnly": False, "oppNum": "", "cfda": "", "sortBy": "", "oppStatuses": "forecasted|posted", "startRecordNum": 0, "eligibilities": "", "fundingIntruments": "", "fundingCategories": "", "agencies": "", "rows": 100, "keyword": "rehabilitation", "keywordEncoded": True},
                "hitCount": 96, "startRecord": 0,
                "oppHits": [MOCK_GRANT_NEW_1, MOCK_GRANT_NEW_2],
                "oppStatusOptions": [{"label": "posted", "value": "posted", "count": 77},
                                     {"label": "closed", "value": "closed", "count": 1366},
                                     {"label": "archived", "value": "archived", "count": 10617},
                                     {"label": "forecasted", "value": "forecasted", "count": 19}],
                "dateStatusOptions": [{"label": "Posted Date - Last 2 Weeks", "value": "14", "count": 9},
                                      {"label": "Posted Date - Last 3 Weeks", "value": "21", "count": 12},
                                      {"label": "Posted Date - Last 4 Weeks", "value": "28", "count": 16},
                                      {"label": "Posted Date - Last 5 Weeks", "value": "35", "count": 34},
                                      {"label": "Posted Date - Last 6 Weeks", "value": "42", "count": 37},
                                      {"label": "Posted Date - Last 7 Weeks", "value": "49", "count": 37},
                                      {"label": "Posted Date - Last 8 Weeks", "value": "56", "count": 39}
                                    ],
                "suggestion": "",
                "eligibilities": [{"label": "City or township government", "value": "02", "count": 32},
                                  {"label": "County governments", "value": "01", "count": 32},
                                  {"label": "For profit organizations other than small businesses", "value": "22", "count": 19},
                                  {"label": "Independent school districts", "value": "05", "count": 14},
                                  {"label": "Individuals", "value": "21", "count": 4},
                                  {"label": "Native American tribal governments (Federally recognized)", "value": "07", "count": 42},
                                  {"label": "Native American tribal organizations (other than Federally recognized tribal governments", "value": "11", "count": 26},
                                  {"label": "Nonprofits having a 501(c)(3) status with the IRS, other than institutions of higher education", "value": "12", "count": 38},
                                  {"label": "Nonprofits that do not have a 501(c)(3) status with the IRS, other than institutions of higher education", "value": "13", "count": 26},
                                  {"label": "Others (see text field entitled 'Additional Information on Eligibility' for clarification", "value": "25", "count": 47},
                                  {"label": "Private institutions of higher education", "value": "20", "count": 34},
                                  {"label": "Public and State controlled institutions of higher education", "value": "06", "count": 36},
                                  {"label": "Public housing authorities/Indian housing authorities", "value": "08", "count": 12},
                                  {"label": "Small businesses", "value": "23", "count": 25},
                                  {"label": "Special district governments", "value": "04", "count": 28},
                                  {"label": "State governments", "value": "00", "count": 39},
                                  {"label": "Unrestricted (i.e., open to any type of entity above), subject to clarification in text field entitled 'Additional Information on Eligibility'", "value": "99", "count": 17}
                                ],
                "fundingCategories": [{"label": "Agriculture", "value": "AG", "count": 2},
                                      {"label": "Business and Commerce", "value": "BC", "count": 3},
                                      {"label": "Community Development", "value": "CD", "count": 5},
                                      {"label": "Education", "value": "ED", "count": 9},
                                      {"label": "Employment, Labor and Training", "value": "ELT", "count": 5},
                                      {"label": "Energy", "value": "EN", "count": 1},
                                      {"label": "Environment", "value": "ENV", "count": 6},
                                      {"label": "Health", "value": "HL", "count": 15},
                                      {"label": "Housing", "value": "HO", "count": 4},
                                      {"label": "Humanities", "value": "HU", "count": 4},
                                      {"label": "Income Security and Social Services", "value": "ISS", "count": 2},
                                      {"label": "Natural Resources", "value": "NR", "count": 4},
                                      {"label": "Other (see text field entitled 'Explanation of Other Category of Funding Activity' for clarification)", "value": "O", "count": 10},
                                      {"label": "Regional Development", "value": "RD", "count": 1},
                                      {"label": "Science and Technology and other Research and Development", "value": "ST", "count": 38},
                                      {"label": "Transportation", "value": "T", "count": 5}
                                    ],
                "fundingInstruments": [{"label": "Cooperative Agreement", "value": "CA", "count": 31},
                                       {"label": "Grant", "value": "G", "count": 76},
                                       {"label": "Other", "value": "O", "count": 9},
                                       {"label": "Procurement Contract", "value": "PC", "count": 9}
                                    ],
                "agencies": [{'subAgencyOptions': [{'label': 'Rural Business-Cooperative Service ', 'value': 'USDA-RBCS', 'count': 1}, {'label': 'Rural Utilities Service', 'value': 'USDA-RUS', 'count': 3}], 'label': 'Department of Agriculture', 'value': 'USDA', 'count': 4}, {'subAgencyOptions': [{'label': 'DOC NOAA - ERA Production', 'value': 'DOC-DOCNOAAERA', 'count': 1}, {'label': 'Economic Development Administration', 'value': 'DOC-EDA', 'count': 4}], 'label': 'Department of Commerce', 'value': 'DOC', 'count': 5}, {'subAgencyOptions': [{'label': 'ACC-APG-Aberdeen Division A', 'value': 'DOD-AMC-ACCAPGADA', 'count': 1}, {'label': 'Air Force -- Research Lab', 'value': 'DOD-AFRL', 'count': 5}, {'label': 'DARPA - Biological Technologies Office', 'value': 'DOD-DARPA-BTO', 'count': 1}, {'label': 'DARPA - Defense Sciences Office', 'value': 'DOD-DARPA-DSO', 'count': 2}, {'label': 'Dept. of the Army -- USAMRAA', 'value': 'DOD-AMRAA', 'count': 3}, {'label': 'National Geospatial-Intelligence Agency ', 'value': 'DOD-NGIA', 'count': 1}, {'label': 'NAVAIR', 'value': 'DOD-ONR-AIR', 'count': 1}, {'label': 'NSWC Dahlgren', 'value': 'DOD-ONR-SEA-N00178', 'count': 1}, {'label': 'Washington Headquarters Services', 'value': 'DOD-WHS', 'count': 2}], 'label': 'Department of Defense', 'value': 'DOD', 'count': 17}, {'subAgencyOptions': [], 'label': 'Department of Education', 'value': 'ED', 'count': 4}, {'subAgencyOptions': [{'label': 'Administration for Children and Families - ORR', 'value': 'HHS-ACF-ORR', 'count': 2}, {'label': 'Administration for Community Living', 'value': 'HHS-ACL', 'count': 15}, {'label': 'Centers for Disease Control and Prevention - ERA', 'value': 'HHS-CDC-HHSCDCERA', 'count': 3}, {'label': 'Centers for Medicare & Medicaid Services', 'value': 'HHS-CMS', 'count': 1}, {'label': 'National Institutes of Health', 'value': 'HHS-NIH11', 'count': 8}, {'label': 'Office of the National Coordinator', 'value': 'HHS-OS-ONC', 'count': 1}], 'label': 'Department of Health and Human Services', 'value': 'HHS', 'count': 30}, {'subAgencyOptions': [], 'label': 'Department of Housing and Urban Development', 'value': 'HUD', 'count': 5}, {'subAgencyOptions': [{'label': 'Employment and Training Administration', 'value': 'DOL-ETA', 'count': 1}], 'label': 'Department of Labor', 'value': 'DOL', 'count': 1}, {'subAgencyOptions': [{'label': 'Bureau of Population Refugees and Migration', 'value': 'DOS-PRM', 'count': 1}, {'label': 'Office to Monitor-Combat Trafficking in Persons', 'value': 'DOS-GTIP', 'count': 1}], 'label': 'Department of State', 'value': 'DOS', 'count': 2}, {'subAgencyOptions': [{'label': 'Bureau of Reclamation', 'value': 'DOI-BOR', 'count': 1}, {'label': 'Fish and Wildlife Service', 'value': 'DOI-FWS', 'count': 6}, {'label': 'National Park Service', 'value': 'DOI-NPS', 'count': 3}], 'label': 'Department of the Interior', 'value': 'DOI', 'count': 10}, {'subAgencyOptions': [{'label': '69A345 Office of the Under Secretary for Policy', 'value': 'DOT-DOT X-50', 'count': 1}, {'label': 'DOT - FAA Aviation Research Grants', 'value': 'DOT-FAA-FAA ARG', 'count': 1}, {'label': 'DOT - Federal Railroad Administration', 'value': 'DOT-FRA', 'count': 1}, {'label': 'DOT Federal Highway Administration ', 'value': 'DOT-FHWA', 'count': 1}, {'label': 'DOT-Federal Motor Carrier Safety Administration', 'value': 'DOT-FMCSA', 'count': 1}], 'label': 'Department of Transportation', 'value': 'DOT', 'count': 5}, {'subAgencyOptions': [{'label': 'Construction of State Home Facilities', 'value': 'VA-CSHF', 'count': 1}], 'label': 'Department of Veterans Affairs', 'value': 'VA', 'count': 1}, {'subAgencyOptions': [], 'label': 'Millennium Challenge Corporation', 'value': 'MCC', 'count': 1}, {'subAgencyOptions': [], 'label': 'National Endowment for the Humanities', 'value': 'NEH', 'count': 4}, {'subAgencyOptions': [], 'label': 'U.S. National Science Foundation', 'value': 'NSF', 'count': 7}],
                "accessKey": "", "errorMsgs": []
                }
            }

MOCK_RESPONSE_PG2 = {
            "errorcode": 0, "msg": "Webservice Succeeds", "token": "gfiobrgobuwjfeiuwdfsdbai",
            "data": {
                "searchParams": {"resultType": "json", "searchOnly": False, "oppNum": "", "cfda": "", "sortBy": "", "oppStatuses": "forecasted|posted", "startRecordNum": 0, "eligibilities": "", "fundingIntruments": "", "fundingCategories": "", "agencies": "", "rows": 100, "keyword": "rehabilitation", "keywordEncoded": True}, 
                "hitCount": 96, "startRecord": 0,
                "oppHits": [MOCK_GRANT_BORDER, MOCK_GRANT_OLD],
                "oppStatusOptions": [{"label": "posted", "value": "posted", "count": 77}, 
                                     {"label": "closed", "value": "closed", "count": 1366},
                                     {"label": "archived", "value": "archived", "count": 10617},
                                     {"label": "forecasted", "value": "forecasted", "count": 19}],
                "dateStatusOptions": [{"label": "Posted Date - Last 2 Weeks", "value": "14", "count": 9},
                                      {"label": "Posted Date - Last 3 Weeks", "value": "21", "count": 12},
                                      {"label": "Posted Date - Last 4 Weeks", "value": "28", "count": 16},
                                      {"label": "Posted Date - Last 5 Weeks", "value": "35", "count": 34},
                                      {"label": "Posted Date - Last 6 Weeks", "value": "42", "count": 37},
                                      {"label": "Posted Date - Last 7 Weeks", "value": "49", "count": 37},
                                      {"label": "Posted Date - Last 8 Weeks", "value": "56", "count": 39}
                                    ],
                "suggestion": "",
                "eligibilities": [{"label": "City or township government", "value": "02", "count": 32},
                                  {"label": "County governments", "value": "01", "count": 32},
                                  {"label": "For profit organizations other than small businesses", "value": "22", "count": 19},
                                  {"label": "Independent school districts", "value": "05", "count": 14},
                                  {"label": "Individuals", "value": "21", "count": 4},
                                  {"label": "Native American tribal governments (Federally recognized)", "value": "07", "count": 42},
                                  {"label": "Native American tribal organizations (other than Federally recognized tribal governments", "value": "11", "count": 26},
                                  {"label": "Nonprofits having a 501(c)(3) status with the IRS, other than institutions of higher education", "value": "12", "count": 38},
                                  {"label": "Nonprofits that do not have a 501(c)(3) status with the IRS, other than institutions of higher education", "value": "13", "count": 26},
                                  {"label": "Others (see text field entitled 'Additional Information on Eligibility' for clarification", "value": "25", "count": 47},
                                  {"label": "Private institutions of higher education", "value": "20", "count": 34},
                                  {"label": "Public and State controlled institutions of higher education", "value": "06", "count": 36},
                                  {"label": "Public housing authorities/Indian housing authorities", "value": "08", "count": 12},
                                  {"label": "Small businesses", "value": "23", "count": 25},
                                  {"label": "Special district governments", "value": "04", "count": 28},
                                  {"label": "State governments", "value": "00", "count": 39},
                                  {"label": "Unrestricted (i.e., open to any type of entity above), subject to clarification in text field entitled 'Additional Information on Eligibility'", "value": "99", "count": 17}
                                ],
                "fundingCategories": [{"label": "Agriculture", "value": "AG", "count": 2},
                                      {"label": "Business and Commerce", "value": "BC", "count": 3},
                                      {"label": "Community Development", "value": "CD", "count": 5},
                                      {"label": "Education", "value": "ED", "count": 9},
                                      {"label": "Employment, Labor and Training", "value": "ELT", "count": 5},
                                      {"label": "Energy", "value": "EN", "count": 1},
                                      {"label": "Environment", "value": "ENV", "count": 6},
                                      {"label": "Health", "value": "HL", "count": 15},
                                      {"label": "Housing", "value": "HO", "count": 4},
                                      {"label": "Humanities", "value": "HU", "count": 4},
                                      {"label": "Income Security and Social Services", "value": "ISS", "count": 2},
                                      {"label": "Natural Resources", "value": "NR", "count": 4},
                                      {"label": "Other (see text field entitled 'Explanation of Other Category of Funding Activity' for clarification)", "value": "O", "count": 10},
                                      {"label": "Regional Development", "value": "RD", "count": 1},
                                      {"label": "Science and Technology and other Research and Development", "value": "ST", "count": 38},
                                      {"label": "Transportation", "value": "T", "count": 5}
                                    ],
                "fundingInstruments": [{"label": "Cooperative Agreement", "value": "CA", "count": 31},
                                       {"label": "Grant", "value": "G", "count": 76},
                                       {"label": "Other", "value": "O", "count": 9},
                                       {"label": "Procurement Contract", "value": "PC", "count": 9}
                                    ],
                "agencies": [{'subAgencyOptions': [{'label': 'Rural Business-Cooperative Service ', 'value': 'USDA-RBCS', 'count': 1}, {'label': 'Rural Utilities Service', 'value': 'USDA-RUS', 'count': 3}], 'label': 'Department of Agriculture', 'value': 'USDA', 'count': 4}, {'subAgencyOptions': [{'label': 'DOC NOAA - ERA Production', 'value': 'DOC-DOCNOAAERA', 'count': 1}, {'label': 'Economic Development Administration', 'value': 'DOC-EDA', 'count': 4}], 'label': 'Department of Commerce', 'value': 'DOC', 'count': 5}, {'subAgencyOptions': [{'label': 'ACC-APG-Aberdeen Division A', 'value': 'DOD-AMC-ACCAPGADA', 'count': 1}, {'label': 'Air Force -- Research Lab', 'value': 'DOD-AFRL', 'count': 5}, {'label': 'DARPA - Biological Technologies Office', 'value': 'DOD-DARPA-BTO', 'count': 1}, {'label': 'DARPA - Defense Sciences Office', 'value': 'DOD-DARPA-DSO', 'count': 2}, {'label': 'Dept. of the Army -- USAMRAA', 'value': 'DOD-AMRAA', 'count': 3}, {'label': 'National Geospatial-Intelligence Agency ', 'value': 'DOD-NGIA', 'count': 1}, {'label': 'NAVAIR', 'value': 'DOD-ONR-AIR', 'count': 1}, {'label': 'NSWC Dahlgren', 'value': 'DOD-ONR-SEA-N00178', 'count': 1}, {'label': 'Washington Headquarters Services', 'value': 'DOD-WHS', 'count': 2}], 'label': 'Department of Defense', 'value': 'DOD', 'count': 17}, {'subAgencyOptions': [], 'label': 'Department of Education', 'value': 'ED', 'count': 4}, {'subAgencyOptions': [{'label': 'Administration for Children and Families - ORR', 'value': 'HHS-ACF-ORR', 'count': 2}, {'label': 'Administration for Community Living', 'value': 'HHS-ACL', 'count': 15}, {'label': 'Centers for Disease Control and Prevention - ERA', 'value': 'HHS-CDC-HHSCDCERA', 'count': 3}, {'label': 'Centers for Medicare & Medicaid Services', 'value': 'HHS-CMS', 'count': 1}, {'label': 'National Institutes of Health', 'value': 'HHS-NIH11', 'count': 8}, {'label': 'Office of the National Coordinator', 'value': 'HHS-OS-ONC', 'count': 1}], 'label': 'Department of Health and Human Services', 'value': 'HHS', 'count': 30}, {'subAgencyOptions': [], 'label': 'Department of Housing and Urban Development', 'value': 'HUD', 'count': 5}, {'subAgencyOptions': [{'label': 'Employment and Training Administration', 'value': 'DOL-ETA', 'count': 1}], 'label': 'Department of Labor', 'value': 'DOL', 'count': 1}, {'subAgencyOptions': [{'label': 'Bureau of Population Refugees and Migration', 'value': 'DOS-PRM', 'count': 1}, {'label': 'Office to Monitor-Combat Trafficking in Persons', 'value': 'DOS-GTIP', 'count': 1}], 'label': 'Department of State', 'value': 'DOS', 'count': 2}, {'subAgencyOptions': [{'label': 'Bureau of Reclamation', 'value': 'DOI-BOR', 'count': 1}, {'label': 'Fish and Wildlife Service', 'value': 'DOI-FWS', 'count': 6}, {'label': 'National Park Service', 'value': 'DOI-NPS', 'count': 3}], 'label': 'Department of the Interior', 'value': 'DOI', 'count': 10}, {'subAgencyOptions': [{'label': '69A345 Office of the Under Secretary for Policy', 'value': 'DOT-DOT X-50', 'count': 1}, {'label': 'DOT - FAA Aviation Research Grants', 'value': 'DOT-FAA-FAA ARG', 'count': 1}, {'label': 'DOT - Federal Railroad Administration', 'value': 'DOT-FRA', 'count': 1}, {'label': 'DOT Federal Highway Administration ', 'value': 'DOT-FHWA', 'count': 1}, {'label': 'DOT-Federal Motor Carrier Safety Administration', 'value': 'DOT-FMCSA', 'count': 1}], 'label': 'Department of Transportation', 'value': 'DOT', 'count': 5}, {'subAgencyOptions': [{'label': 'Construction of State Home Facilities', 'value': 'VA-CSHF', 'count': 1}], 'label': 'Department of Veterans Affairs', 'value': 'VA', 'count': 1}, {'subAgencyOptions': [], 'label': 'Millennium Challenge Corporation', 'value': 'MCC', 'count': 1}, {'subAgencyOptions': [], 'label': 'National Endowment for the Humanities', 'value': 'NEH', 'count': 4}, {'subAgencyOptions': [], 'label': 'U.S. National Science Foundation', 'value': 'NSF', 'count': 7}],
                "accessKey": "", "errorMsgs": []
                }
            }

MOCK_RESPONSE_EMPTY = {
            "errorcode": 0, "msg": "Webservice Succeeds", "token": "gfiobrgobuwjfeiuwdfsdbai",
            "data": {
                "searchParams": {"resultType": "json", "searchOnly": False, "oppNum": "", "cfda": "", "sortBy": "", "oppStatuses": "forecasted|posted", "startRecordNum": 0, "eligibilities": "", "fundingIntruments": "", "fundingCategories": "", "agencies": "", "rows": 100, "keyword": "rehabilitation", "keywordEncoded": True}, 
                "hitCount": 1, "startRecord": 0,
                "oppHits": [],
                "oppStatusOptions": [{"label": "posted", "value": "posted", "count": 77},
                                     {"label": "closed", "value": "closed", "count": 1366},
                                     {"label": "archived", "value": "archived", "count": 10617},
                                     {"label": "forecasted", "value": "forecasted", "count": 19}],
                "dateStatusOptions": [{"label": "Posted Date - Last 2 Weeks", "value": "14", "count": 9},
                                      {"label": "Posted Date - Last 3 Weeks", "value": "21", "count": 12},
                                      {"label": "Posted Date - Last 4 Weeks", "value": "28", "count": 16},
                                      {"label": "Posted Date - Last 5 Weeks", "value": "35", "count": 34},
                                      {"label": "Posted Date - Last 6 Weeks", "value": "42", "count": 37},
                                      {"label": "Posted Date - Last 7 Weeks", "value": "49", "count": 37},
                                      {"label": "Posted Date - Last 8 Weeks", "value": "56", "count": 39}
                                    ],
                "suggestion": "",
                "eligibilities": [{"label": "City or township government", "value": "02", "count": 32},
                                  {"label": "County governments", "value": "01", "count": 32},
                                  {"label": "For profit organizations other than small businesses", "value": "22", "count": 19},
                                  {"label": "Independent school districts", "value": "05", "count": 14},
                                  {"label": "Individuals", "value": "21", "count": 4},
                                  {"label": "Native American tribal governments (Federally recognized)", "value": "07", "count": 42},
                                  {"label": "Native American tribal organizations (other than Federally recognized tribal governments", "value": "11", "count": 26},
                                  {"label": "Nonprofits having a 501(c)(3) status with the IRS, other than institutions of higher education", "value": "12", "count": 38},
                                  {"label": "Nonprofits that do not have a 501(c)(3) status with the IRS, other than institutions of higher education", "value": "13", "count": 26},
                                  {"label": "Others (see text field entitled 'Additional Information on Eligibility' for clarification", "value": "25", "count": 47},
                                  {"label": "Private institutions of higher education", "value": "20", "count": 34},
                                  {"label": "Public and State controlled institutions of higher education", "value": "06", "count": 36},
                                  {"label": "Public housing authorities/Indian housing authorities", "value": "08", "count": 12},
                                  {"label": "Small businesses", "value": "23", "count": 25},
                                  {"label": "Special district governments", "value": "04", "count": 28},
                                  {"label": "State governments", "value": "00", "count": 39},
                                  {"label": "Unrestricted (i.e., open to any type of entity above), subject to clarification in text field entitled 'Additional Information on Eligibility'", "value": "99", "count": 17}
                                ],
                "fundingCategories": [{"label": "Agriculture", "value": "AG", "count": 2},
                                      {"label": "Business and Commerce", "value": "BC", "count": 3},
                                      {"label": "Community Development", "value": "CD", "count": 5},
                                      {"label": "Education", "value": "ED", "count": 9},
                                      {"label": "Employment, Labor and Training", "value": "ELT", "count": 5},
                                      {"label": "Energy", "value": "EN", "count": 1},
                                      {"label": "Environment", "value": "ENV", "count": 6},
                                      {"label": "Health", "value": "HL", "count": 15},
                                      {"label": "Housing", "value": "HO", "count": 4},
                                      {"label": "Humanities", "value": "HU", "count": 4},
                                      {"label": "Income Security and Social Services", "value": "ISS", "count": 2},
                                      {"label": "Natural Resources", "value": "NR", "count": 4},
                                      {"label": "Other (see text field entitled 'Explanation of Other Category of Funding Activity' for clarification)", "value": "O", "count": 10},
                                      {"label": "Regional Development", "value": "RD", "count": 1},
                                      {"label": "Science and Technology and other Research and Development", "value": "ST", "count": 38},
                                      {"label": "Transportation", "value": "T", "count": 5}
                                    ],
                "fundingInstruments": [{"label": "Cooperative Agreement", "value": "CA", "count": 31},
                                       {"label": "Grant", "value": "G", "count": 76},
                                       {"label": "Other", "value": "O", "count": 9},
                                       {"label": "Procurement Contract", "value": "PC", "count": 9}
                                    ],
                "agencies": [{'subAgencyOptions': [{'label': 'Rural Business-Cooperative Service ', 'value': 'USDA-RBCS', 'count': 1}, {'label': 'Rural Utilities Service', 'value': 'USDA-RUS', 'count': 3}], 'label': 'Department of Agriculture', 'value': 'USDA', 'count': 4}, {'subAgencyOptions': [{'label': 'DOC NOAA - ERA Production', 'value': 'DOC-DOCNOAAERA', 'count': 1}, {'label': 'Economic Development Administration', 'value': 'DOC-EDA', 'count': 4}], 'label': 'Department of Commerce', 'value': 'DOC', 'count': 5}, {'subAgencyOptions': [{'label': 'ACC-APG-Aberdeen Division A', 'value': 'DOD-AMC-ACCAPGADA', 'count': 1}, {'label': 'Air Force -- Research Lab', 'value': 'DOD-AFRL', 'count': 5}, {'label': 'DARPA - Biological Technologies Office', 'value': 'DOD-DARPA-BTO', 'count': 1}, {'label': 'DARPA - Defense Sciences Office', 'value': 'DOD-DARPA-DSO', 'count': 2}, {'label': 'Dept. of the Army -- USAMRAA', 'value': 'DOD-AMRAA', 'count': 3}, {'label': 'National Geospatial-Intelligence Agency ', 'value': 'DOD-NGIA', 'count': 1}, {'label': 'NAVAIR', 'value': 'DOD-ONR-AIR', 'count': 1}, {'label': 'NSWC Dahlgren', 'value': 'DOD-ONR-SEA-N00178', 'count': 1}, {'label': 'Washington Headquarters Services', 'value': 'DOD-WHS', 'count': 2}], 'label': 'Department of Defense', 'value': 'DOD', 'count': 17}, {'subAgencyOptions': [], 'label': 'Department of Education', 'value': 'ED', 'count': 4}, {'subAgencyOptions': [{'label': 'Administration for Children and Families - ORR', 'value': 'HHS-ACF-ORR', 'count': 2}, {'label': 'Administration for Community Living', 'value': 'HHS-ACL', 'count': 15}, {'label': 'Centers for Disease Control and Prevention - ERA', 'value': 'HHS-CDC-HHSCDCERA', 'count': 3}, {'label': 'Centers for Medicare & Medicaid Services', 'value': 'HHS-CMS', 'count': 1}, {'label': 'National Institutes of Health', 'value': 'HHS-NIH11', 'count': 8}, {'label': 'Office of the National Coordinator', 'value': 'HHS-OS-ONC', 'count': 1}], 'label': 'Department of Health and Human Services', 'value': 'HHS', 'count': 30}, {'subAgencyOptions': [], 'label': 'Department of Housing and Urban Development', 'value': 'HUD', 'count': 5}, {'subAgencyOptions': [{'label': 'Employment and Training Administration', 'value': 'DOL-ETA', 'count': 1}], 'label': 'Department of Labor', 'value': 'DOL', 'count': 1}, {'subAgencyOptions': [{'label': 'Bureau of Population Refugees and Migration', 'value': 'DOS-PRM', 'count': 1}, {'label': 'Office to Monitor-Combat Trafficking in Persons', 'value': 'DOS-GTIP', 'count': 1}], 'label': 'Department of State', 'value': 'DOS', 'count': 2}, {'subAgencyOptions': [{'label': 'Bureau of Reclamation', 'value': 'DOI-BOR', 'count': 1}, {'label': 'Fish and Wildlife Service', 'value': 'DOI-FWS', 'count': 6}, {'label': 'National Park Service', 'value': 'DOI-NPS', 'count': 3}], 'label': 'Department of the Interior', 'value': 'DOI', 'count': 10}, {'subAgencyOptions': [{'label': '69A345 Office of the Under Secretary for Policy', 'value': 'DOT-DOT X-50', 'count': 1}, {'label': 'DOT - FAA Aviation Research Grants', 'value': 'DOT-FAA-FAA ARG', 'count': 1}, {'label': 'DOT - Federal Railroad Administration', 'value': 'DOT-FRA', 'count': 1}, {'label': 'DOT Federal Highway Administration ', 'value': 'DOT-FHWA', 'count': 1}, {'label': 'DOT-Federal Motor Carrier Safety Administration', 'value': 'DOT-FMCSA', 'count': 1}], 'label': 'Department of Transportation', 'value': 'DOT', 'count': 5}, {'subAgencyOptions': [{'label': 'Construction of State Home Facilities', 'value': 'VA-CSHF', 'count': 1}], 'label': 'Department of Veterans Affairs', 'value': 'VA', 'count': 1}, {'subAgencyOptions': [], 'label': 'Millennium Challenge Corporation', 'value': 'MCC', 'count': 1}, {'subAgencyOptions': [], 'label': 'National Endowment for the Humanities', 'value': 'NEH', 'count': 4}, {'subAgencyOptions': [], 'label': 'U.S. National Science Foundation', 'value': 'NSF', 'count': 7}],
                "accessKey": "", "errorMsgs": []
                }
            }

MOCK_LAST_REFRESH = "2024-03-14"

class TestFetchData(unittest.TestCase):
    '''
    Tests fetch_data happy path AND ensures correct termination
    '''
    @patch('scripts.pull_grants.requests.post')
    def test_fetch_data_happy(self, mock_post):
        mock_response_pg1 = Mock()
        mock_response_pg1.status_code = 200
        mock_response_pg1.json.return_value = MOCK_RESPONSE_PG1

        mock_response_pg2 = Mock()
        mock_response_pg2.status_code = 200
        mock_response_pg2.json.return_value = MOCK_RESPONSE_PG2

        mock_post.side_effect = [mock_response_pg1, mock_response_pg2]

        grants = METADATA['fetch_fn'](METADATA['search_terms'], MOCK_LAST_REFRESH)

        self.assertEqual(mock_post.call_count, 2)
        self.assertEqual(len(grants), 2)
        self.assertNotIn(MOCK_GRANT_BORDER, grants)
        self.assertEqual(grants[0]['id'], '360499')
        self.assertEqual(grants[1]['id'], '360527')

    '''
    Tests fetch_data edge case: no results
    '''
    @patch('scripts.pull_grants.requests.post')
    def test_fetch_data_no_results(self, mock_post):
        mock_response_pg1 = Mock()
        mock_response_pg1.status_code = 200
        mock_response_pg1.json.return_value = MOCK_RESPONSE_PG1

        mock_response_pg2 = Mock()
        mock_response_pg2.status_code = 200
        mock_response_pg2.json.return_value = MOCK_RESPONSE_EMPTY

        mock_post.side_effect = [mock_response_pg1, mock_response_pg2]
        grants = METADATA['fetch_fn'](METADATA['search_terms'], MOCK_LAST_REFRESH)

        self.assertEqual(mock_post.call_count, 2)
        self.assertEqual(len(grants), 2)
       


