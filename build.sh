#!/usr/bin/env bash

function generate_files {
  python generate.py || return $?
  while read -r line; do
    git apply "$line" || return $?
  done <<< $(find ./patches -name "*.patch")
}

generate_files