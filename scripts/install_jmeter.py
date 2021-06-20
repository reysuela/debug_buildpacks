#!/usr/bin/env python
import urllib2
import tarfile
import sys
import os

def dlfile(url, install_dir):
    dlfile_fullpath = os.path.join(install_dir, os.path.basename(url))
    try:
        f = urllib2.urlopen(url)
        print("downloading " + url)
        
        if not os.path.exists(install_dir):
            os.mkdir(install_dir)

        with open(dlfile_fullpath, "wb") as local_file:
            local_file.write(f.read())

        if not os.path.isfile(dlfile_fullpath):
            return None
        print("jmeter tgz file saved in {0}".format(dlfile_fullpath))

    except urllib2.HTTPError, e:
        print "HTTP Error:", e.code, url
    except urllib2.URLError, e:
        print "URL Error:", e.reason, url
    return dlfile_fullpath

def extract_tar(fname):
    output_directory = os.path.dirname(fname)
    if fname.endswith("tar.gz") or fname.endswith("tgz"):
        tar = tarfile.open(fname, "r:gz")
        tar.extractall(output_directory)
        tar.close()
    elif fname.endswith("tar"):
        tar = tarfile.open(fname, "r:")
        tar.extractall(os.path.dirname(fname))
        tar.close()
    print("tar gz file extracted to {0}".format(output_directory))

def install_jmeter(install_dir):
    # for now only 5.4.1 is supported. Will prob enhance this in the future
    url = "https://apache.inspire.net.nz/jmeter/binaries/apache-jmeter-5.4.1.tgz"
    jmeter_tgz = dlfile(url, install_dir)

    if not jmeter_tgz:
        print("jmeter tgz not found")
        sys.exit(1)
    
    # extract
    extract_tar(jmeter_tgz)

def install_openjdk(install_dir):
    # for now using fixed version of adoptOpenJDK
    url = "https://github.com/AdoptOpenJDK/openjdk8-binaries/releases/download/jdk8u292-b10/OpenJDK8U-jdk_x64_linux_hotspot_8u292b10.tar.gz"

    openjdk = dlfile(url, install_dir)

    if not openjdk:
        print("jmeter tgz not found")
        sys.exit(1)

    # extract
    extract_tar(openjdk)

if __name__ == '__main__':
    build_path = sys.argv[1]
    cache_path = sys.argv[2]
    deps_path = sys.argv[3]
    index = sys.argv[4]
    install_jmeter(os.path.join(build_path, "jmeter"))
    sys.exit(0)
