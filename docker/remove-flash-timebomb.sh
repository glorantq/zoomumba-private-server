#!/usr/bin/env bash

# From: https://aur.archlinux.org/cgit/aur.git/tree/PKGBUILD?h=flashplugin-debug

plugin_file="$1";
shift;
# From https://cache.tehsausage.com/flash/defuse.txt
time_bomb_trigger='\x40\x46\x3E\x6F\x77\x42'
if grep "$(printf "$time_bomb_trigger")" "$plugin_file"; then
  echo "Found flash player EOL time bomb in ${plugin_file}. Removing it..."
  bbe -o "${plugin_file}.patched" -e "s/\x00\x00${time_bomb_trigger}/\x00\x00\x00\x00\x00\x00\xF8\x7F/" "$plugin_file"
  mv "${plugin_file}.patched" "$plugin_file"
  sync
  echo "Removed flash player EOL time bomb from ${plugin_file}"
else
  echo "Did not find flash player EOL time bomb in ${plugin_file}."
fi
