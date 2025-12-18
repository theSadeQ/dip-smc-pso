#!/usr/bin/env python3
"""
Analyze Batch 08 citation coverage - identify missing claims.

This script compares the batch claims.json with ChatGPT's response
to find which claims are missing citations.
"""

import json
from pathlib import Path

# Load batch claims
batch_file = Path("D:/Projects/main/artifacts/research_batches/08_HIGH_implementation_general/claims.json")
with open(batch_file) as f:
    batch_data = json.load(f)

batch_claim_ids = [c['id'] for c in batch_data['claims']]

# Extract claim IDs from ChatGPT response (from user's message)
# Based on the 311 claims provided
chatgpt_claim_ids = [
    'CODE-IMPL-002', 'CODE-IMPL-003', 'CODE-IMPL-004', 'CODE-IMPL-005', 'CODE-IMPL-007',
    'CODE-IMPL-012', 'CODE-IMPL-013', 'CODE-IMPL-014', 'CODE-IMPL-015', 'CODE-IMPL-016',
    'CODE-IMPL-029', 'CODE-IMPL-032', 'CODE-IMPL-047', 'CODE-IMPL-052', 'CODE-IMPL-053',
    'CODE-IMPL-054', 'CODE-IMPL-055', 'CODE-IMPL-056', 'CODE-IMPL-057', 'CODE-IMPL-058',
    'CODE-IMPL-059', 'CODE-IMPL-060', 'CODE-IMPL-061', 'CODE-IMPL-062', 'CODE-IMPL-063',
    'CODE-IMPL-064', 'CODE-IMPL-066', 'CODE-IMPL-068', 'CODE-IMPL-069', 'CODE-IMPL-073',
    'CODE-IMPL-074', 'CODE-IMPL-075', 'CODE-IMPL-077', 'CODE-IMPL-078', 'CODE-IMPL-079',
    'CODE-IMPL-080', 'CODE-IMPL-081', 'CODE-IMPL-082', 'CODE-IMPL-083', 'CODE-IMPL-085',
    'CODE-IMPL-086', 'CODE-IMPL-090', 'CODE-IMPL-091', 'CODE-IMPL-106', 'CODE-IMPL-107',
    'CODE-IMPL-108', 'CODE-IMPL-109', 'CODE-IMPL-110', 'CODE-IMPL-111', 'CODE-IMPL-114',
    'CODE-IMPL-115', 'CODE-IMPL-117', 'CODE-IMPL-120', 'CODE-IMPL-121', 'CODE-IMPL-122',
    'CODE-IMPL-123', 'CODE-IMPL-132', 'CODE-IMPL-134', 'CODE-IMPL-135', 'CODE-IMPL-146',
    'CODE-IMPL-147', 'CODE-IMPL-150', 'CODE-IMPL-152', 'CODE-IMPL-155', 'CODE-IMPL-156',
    'CODE-IMPL-157', 'CODE-IMPL-158', 'CODE-IMPL-159', 'CODE-IMPL-167', 'CODE-IMPL-168',
    'CODE-IMPL-169', 'CODE-IMPL-173', 'CODE-IMPL-174', 'CODE-IMPL-175', 'CODE-IMPL-178',
    'CODE-IMPL-180', 'CODE-IMPL-181', 'CODE-IMPL-182', 'CODE-IMPL-183', 'CODE-IMPL-186',
    'CODE-IMPL-189', 'CODE-IMPL-190', 'CODE-IMPL-191', 'CODE-IMPL-192', 'CODE-IMPL-193',
    'CODE-IMPL-194', 'CODE-IMPL-195', 'CODE-IMPL-201', 'CODE-IMPL-204', 'CODE-IMPL-206',
    'CODE-IMPL-207', 'CODE-IMPL-209', 'CODE-IMPL-210', 'CODE-IMPL-213', 'CODE-IMPL-214',
    'CODE-IMPL-215', 'CODE-IMPL-216', 'CODE-IMPL-217', 'CODE-IMPL-218', 'CODE-IMPL-219',
    'CODE-IMPL-220', 'CODE-IMPL-221', 'CODE-IMPL-222', 'CODE-IMPL-223', 'CODE-IMPL-224',
    'CODE-IMPL-225', 'CODE-IMPL-226', 'CODE-IMPL-227', 'CODE-IMPL-228', 'CODE-IMPL-229',
    'CODE-IMPL-230', 'CODE-IMPL-231', 'CODE-IMPL-232', 'CODE-IMPL-233', 'CODE-IMPL-234',
    'CODE-IMPL-235', 'CODE-IMPL-236', 'CODE-IMPL-237', 'CODE-IMPL-238', 'CODE-IMPL-239',
    'CODE-IMPL-240', 'CODE-IMPL-241', 'CODE-IMPL-242', 'CODE-IMPL-243', 'CODE-IMPL-244',
    'CODE-IMPL-245', 'CODE-IMPL-246', 'CODE-IMPL-247', 'CODE-IMPL-248', 'CODE-IMPL-249',
    'CODE-IMPL-251', 'CODE-IMPL-252', 'CODE-IMPL-254', 'CODE-IMPL-255', 'CODE-IMPL-256',
    'CODE-IMPL-257', 'CODE-IMPL-258', 'CODE-IMPL-259', 'CODE-IMPL-260', 'CODE-IMPL-261',
    'CODE-IMPL-262', 'CODE-IMPL-263', 'CODE-IMPL-264', 'CODE-IMPL-265', 'CODE-IMPL-266',
    'CODE-IMPL-267', 'CODE-IMPL-268', 'CODE-IMPL-269', 'CODE-IMPL-270', 'CODE-IMPL-271',
    'CODE-IMPL-272', 'CODE-IMPL-273', 'CODE-IMPL-274', 'CODE-IMPL-275', 'CODE-IMPL-276',
    'CODE-IMPL-277', 'CODE-IMPL-278', 'CODE-IMPL-279', 'CODE-IMPL-280', 'CODE-IMPL-281',
    'CODE-IMPL-282', 'CODE-IMPL-283', 'CODE-IMPL-285', 'CODE-IMPL-288', 'CODE-IMPL-289',
    'CODE-IMPL-290', 'CODE-IMPL-291', 'CODE-IMPL-292', 'CODE-IMPL-293', 'CODE-IMPL-294',
    'CODE-IMPL-295', 'CODE-IMPL-296', 'CODE-IMPL-297', 'CODE-IMPL-298', 'CODE-IMPL-299',
    'CODE-IMPL-300', 'CODE-IMPL-301', 'CODE-IMPL-302', 'CODE-IMPL-303', 'CODE-IMPL-304',
    'CODE-IMPL-308', 'CODE-IMPL-312', 'CODE-IMPL-321', 'CODE-IMPL-322', 'CODE-IMPL-323',
    'CODE-IMPL-325', 'CODE-IMPL-326', 'CODE-IMPL-327', 'CODE-IMPL-328', 'CODE-IMPL-329',
    'CODE-IMPL-330', 'CODE-IMPL-331', 'CODE-IMPL-332', 'CODE-IMPL-333', 'CODE-IMPL-334',
    'CODE-IMPL-336', 'CODE-IMPL-338', 'CODE-IMPL-339', 'CODE-IMPL-340', 'CODE-IMPL-341',
    'CODE-IMPL-342', 'CODE-IMPL-343', 'CODE-IMPL-344', 'CODE-IMPL-345', 'CODE-IMPL-346',
    'CODE-IMPL-347', 'CODE-IMPL-348', 'CODE-IMPL-349', 'CODE-IMPL-350', 'CODE-IMPL-351',
    'CODE-IMPL-352', 'CODE-IMPL-353', 'CODE-IMPL-355', 'CODE-IMPL-357', 'CODE-IMPL-358',
    'CODE-IMPL-360', 'CODE-IMPL-361', 'CODE-IMPL-363', 'CODE-IMPL-366', 'CODE-IMPL-367',
    'CODE-IMPL-370', 'CODE-IMPL-373', 'CODE-IMPL-375', 'CODE-IMPL-376', 'CODE-IMPL-377',
    'CODE-IMPL-378', 'CODE-IMPL-379', 'CODE-IMPL-380', 'CODE-IMPL-382', 'CODE-IMPL-384',
    'CODE-IMPL-386', 'CODE-IMPL-387', 'CODE-IMPL-390', 'CODE-IMPL-393', 'CODE-IMPL-396',
    'CODE-IMPL-397', 'CODE-IMPL-399', 'CODE-IMPL-400', 'CODE-IMPL-402', 'CODE-IMPL-403',
    'CODE-IMPL-404', 'CODE-IMPL-405', 'CODE-IMPL-406', 'CODE-IMPL-407', 'CODE-IMPL-408',
    'CODE-IMPL-410', 'CODE-IMPL-411', 'CODE-IMPL-412', 'CODE-IMPL-414', 'CODE-IMPL-415',
    'CODE-IMPL-416', 'CODE-IMPL-420', 'CODE-IMPL-421', 'CODE-IMPL-422', 'CODE-IMPL-423',
    'CODE-IMPL-424', 'CODE-IMPL-428', 'CODE-IMPL-429', 'CODE-IMPL-430', 'CODE-IMPL-431',
    'CODE-IMPL-432', 'CODE-IMPL-437', 'CODE-IMPL-438', 'CODE-IMPL-440', 'CODE-IMPL-442',
    'CODE-IMPL-443', 'CODE-IMPL-444', 'CODE-IMPL-446', 'CODE-IMPL-447', 'CODE-IMPL-448',
    'CODE-IMPL-449', 'CODE-IMPL-450', 'CODE-IMPL-451', 'CODE-IMPL-452', 'CODE-IMPL-454',
    'CODE-IMPL-455', 'CODE-IMPL-458', 'CODE-IMPL-460', 'CODE-IMPL-471', 'CODE-IMPL-472',
    'CODE-IMPL-473', 'CODE-IMPL-474', 'CODE-IMPL-476', 'CODE-IMPL-477', 'CODE-IMPL-478',
    'CODE-IMPL-479', 'CODE-IMPL-480', 'CODE-IMPL-481', 'CODE-IMPL-482', 'CODE-IMPL-483',
    'CODE-IMPL-487', 'CODE-IMPL-488', 'CODE-IMPL-490', 'CODE-IMPL-491', 'CODE-IMPL-492',
    'CODE-IMPL-493', 'CODE-IMPL-494', 'CODE-IMPL-496', 'CODE-IMPL-498', 'CODE-IMPL-499',
    'CODE-IMPL-500', 'CODE-IMPL-501', 'CODE-IMPL-502', 'CODE-IMPL-503', 'CODE-IMPL-504',
    'CODE-IMPL-510', 'CODE-IMPL-512', 'CODE-IMPL-516', 'CODE-IMPL-517', 'CODE-IMPL-518',
    'CODE-IMPL-519'
]

# Find missing claims
missing_in_chatgpt = set(batch_claim_ids) - set(chatgpt_claim_ids)
extra_in_chatgpt = set(chatgpt_claim_ids) - set(batch_claim_ids)

print("=" * 80)
print("BATCH 08 COVERAGE ANALYSIS")
print("=" * 80)
print(f"Batch claims total: {len(batch_claim_ids)}")
print(f"ChatGPT response claims: {len(chatgpt_claim_ids)}")
print(f"Coverage: {len(chatgpt_claim_ids)}/{len(batch_claim_ids)} ({100*len(chatgpt_claim_ids)/len(batch_claim_ids):.1f}%)")
print()

if missing_in_chatgpt:
    print(f"[!] MISSING FROM CHATGPT: {len(missing_in_chatgpt)} claims")
    print("-" * 80)
    for claim_id in sorted(missing_in_chatgpt):
        # Find claim details
        claim = next(c for c in batch_data['claims'] if c['id'] == claim_id)
        print(f"  {claim_id}")
        print(f"    File: {claim['file_path']}")
        print(f"    Line: {claim['line_number']}")
        print(f"    Description: {claim['description'][:80]}...")
        print()
else:
    print("[OK] All batch claims covered in ChatGPT response!")

if extra_in_chatgpt:
    print(f"[!] EXTRA IN CHATGPT (not in batch): {len(extra_in_chatgpt)} claims")
    print("-" * 80)
    for claim_id in sorted(extra_in_chatgpt):
        print(f"  {claim_id}")
else:
    print("[OK] No extra claims in ChatGPT response")

print()
print("=" * 80)
