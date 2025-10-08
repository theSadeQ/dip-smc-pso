# Example from: docs\factory\deprecation_management.md
# Index: 9
# Runnable: True
# Hash: 998a15b9

# Recommended deprecation timeline
   DEPRECATION_TIMELINE = {
       'minor_parameter_rename': '2 versions',      # INFO -> WARNING -> ERROR
       'parameter_restructure': '3 versions',       # INFO -> WARNING -> ERROR
       'major_interface_change': '4+ versions',     # Extended timeline
       'safety_critical_change': '6+ versions'      # Maximum timeline
   }