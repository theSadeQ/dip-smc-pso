# Example from: docs\validation\simulation_result_validation.md
# Index: 23
# Runnable: True
# Hash: 3fe72c23

result = suite.validate(
    data,
    compare_groups=[group2],
    test_types=['effect_size_analysis']
)

effect_size = result.data['effect_size_analysis']
cohens_d = effect_size['cohens_d_group_0']['value']
interpretation = effect_size['cohens_d_group_0']['interpretation']