#!/bin/bash

set -e
set -u
set -o pipefail

function main() {
  if [[ "${CF_STACK:-}" != "cflinuxfs3" ]]; then
    echo "       **ERROR** Unsupported stack"
    echo "                 See https://docs.cloudfoundry.org/devguide/deploy-apps/stacks.html for more info"
    exit 1
  fi

  local version expected_sha dir
  version="5.4.1"
  expected_sha="4edae99881d1cdb5048987accbd02b3f3cdadea4a108d16d07fb1525ef612cf3"
  dir="/tmp/jmeter_${version}"

  mkdir -p "${dir}"

  if [[ ! -f "${dir}/bin/jmeter" ]]; then
    local url
    url="https://apache.inspire.net.nz/jmeter/binaries/apache-jmeter-${version}.tgz"

    echo "-----> Download jmeter ${version}"
    curl "${url}" \
      --silent \
      --location \
      --retry 15 \
      --retry-delay 2 \
      --output "/tmp/jmeter.tgz"

    local sha
    sha="$(shasum -a 256 /tmp/jmeter.tgz | cut -d ' ' -f 1)"

    if [[ "${sha}" != "${expected_sha}" ]]; then
      echo "       **ERROR** SHA256 mismatch: got ${sha}, expected ${expected_sha}"
      exit 1
    fi

    tar xzf "/tmp/jmeter.tgz" -C "${dir}" --strip-components 1
    rm "/tmp/jmeter.tgz"
  fi

  if [[ ! -f "${dir}/bin/jmeter" ]]; then
    echo "       **ERROR** Could not download jmeter"
    exit 1
  fi

  JMETER_HOME="${dir}"
  export JMETER_HOME
  export PATH=$PATH:JMETER_HOME/bin
}

main "${@:-}"