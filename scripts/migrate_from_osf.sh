#!/usr/bin/env bash
# One-time migration: download every file that was stored in git-annex (on the
# OSF special remote, node rfzjy) at the last DataLad commit, and verify each
# one against the size and MD5 encoded in its annex key.
#
# This does not need DataLad or git-annex: annex keys are the file names on
# OSF, and the pointer files are still readable from git history.
#
# Usage: scripts/migrate_from_osf.sh <output_dir> [git_ref]
#
# Files are written to <output_dir>/<original repository path>.
# Requires: git, curl, perl (with JSON::PP), and md5sum or md5.
set -euo pipefail

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <output_dir> [git_ref]" >&2
    exit 1
fi

out_dir="$1"
ref="${2:-2727a5f}"
osf_node="rfzjy"
repo_root="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"

mkdir -p "${out_dir}"
out_dir="$(cd "${out_dir}" && pwd)"

if command -v md5sum > /dev/null 2>&1; then
    md5_of() { md5sum "$1" | cut -d' ' -f1; }
else
    md5_of() { md5 -q "$1"; }
fi

work_dir="$(mktemp -d)"
trap 'rm -rf "${work_dir}"' EXIT

# 1. Map annex key -> OSF download URL, following the API's pagination.
url="https://api.osf.io/v2/nodes/${osf_node}/files/osfstorage/?page%5Bsize%5D=100"
: > "${work_dir}/osf_index.tsv"
while [ -n "${url}" ]; do
    curl -fsSL "${url}" > "${work_dir}/page.json"
    perl -MJSON::PP -0777 -ne '
        my $d = decode_json($_);
        for my $x (@{ $d->{data} }) {
            next unless $x->{attributes}{kind} eq "file";
            print "$x->{attributes}{name}\t$x->{links}{download}\n";
        }
    ' "${work_dir}/page.json" >> "${work_dir}/osf_index.tsv"
    url="$(perl -MJSON::PP -0777 -ne '
        my $d = decode_json($_);
        print($d->{links}{next} // "");
    ' "${work_dir}/page.json")"
done

# 2. Find annex pointer files at the given ref (their blobs are short and
#    contain ".git/annex/objects/").
git -C "${repo_root}" ls-tree -r -l "${ref}" | while read -r _mode obj_type blob size path; do
    if [ "${obj_type}" != "blob" ] || [ "${size}" -ge 300 ]; then
        continue
    fi

    content="$(git -C "${repo_root}" cat-file -p "${blob}")"
    case "${content}" in
        *annex/objects/*) printf '%s\t%s\n' "${path}" "${content}" ;;
    esac
done > "${work_dir}/pointers.tsv"

n_files="$(wc -l < "${work_dir}/pointers.tsv")"
echo "Found ${n_files} annexed files at ${ref}"

# 3. Download and verify each file.
n_failed=0
while IFS=$'\t' read -r path pointer; do
    key="$(basename "${pointer}")"
    expected_size="$(printf '%s' "${key}" | sed -E 's/^MD5E-s([0-9]+)--.*/\1/')"
    expected_md5="$(printf '%s' "${key}" | sed -E 's/^MD5E-s[0-9]+--([0-9a-f]{32}).*/\1/')"
    download_url="$(awk -F'\t' -v k="${key}" '$1 == k { print $2; exit }' "${work_dir}/osf_index.tsv")"

    if [ -z "${download_url}" ]; then
        echo "MISSING on OSF: ${path} (${key})" >&2
        n_failed=$((n_failed + 1))
        continue
    fi

    target="${out_dir}/${path}"
    mkdir -p "$(dirname "${target}")"
    if [ -f "${target}" ] \
        && [ "$(wc -c < "${target}" | tr -d ' ')" = "${expected_size}" ] \
        && [ "$(md5_of "${target}")" = "${expected_md5}" ]; then
        echo "ok (cached) ${path}"
        continue
    fi

    curl -fsSL --retry 3 -o "${target}.part" "${download_url}"
    actual_size="$(wc -c < "${target}.part" | tr -d ' ')"
    actual_md5="$(md5_of "${target}.part")"
    if [ "${actual_size}" != "${expected_size}" ] || [ "${actual_md5}" != "${expected_md5}" ]; then
        echo "CHECKSUM MISMATCH: ${path}" >&2
        rm -f "${target}.part"
        n_failed=$((n_failed + 1))
        continue
    fi

    mv "${target}.part" "${target}"
    echo "ok ${path}"
done < "${work_dir}/pointers.tsv"

if [ "${n_failed}" -gt 0 ]; then
    echo "${n_failed} file(s) failed" >&2
    exit 1
fi

echo "All ${n_files} files downloaded and verified in ${out_dir}"
