import subprocess
import sys
import requests

def ipfs_check():
    """
    Test if a local IPFS server (daemon) is running.
    If not, print an error and exit.
    """
    url = 'http://127.0.0.1:5001/webui/api/v0/version'
    try:
        r = requests.get(url)
    except Exception as e:
        print("IPFS server not running: " + str(e))
        sys.exit(1)

    if r.status_code != 200:
        print("IPFS server not running (status code: {}): ".format(r.status_code))
        sys.exit(1)

def get_ipfs_cid(content_path):
    """
    Call the external ipfs binary to get the CID for a file or directory.
    The command uses `--only-hash` so no data is actually uploaded (for testing).
    
    :param content_path: Path to the file or directory to be added.
    :return: A list of CIDs (one per file or directory added)
    """
    # Build the command string
    cmd = 'ipfs add -r --only-hash --quiet "{}"'.format(content_path)
    try:
        # Use subprocess.check_output to run the command.
        # shell=True is used because we pass the command as a string.
        cmd_out = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print("IPFS add failed for {}: {}".format(content_path, e))
        sys.exit(1)
    
    # Decode output and split into lines
    hash_str = cmd_out.decode("utf-8").strip()
    cids = hash_str.splitlines()
    return cids

def add_file_to_ipfs(content_path):
    """
    Add the given file (or directory) to the IPFS network using the external ipfs command.
    Unlike get_ipfs_cid, this function does not use the --only-hash flag and will actually
    store the data on IPFS.
    
    :param content_path: Path to the file or directory.
    :return: The CID(s) returned by ipfs add.
    """
    cmd = 'ipfs add -r --quiet "{}"'.format(content_path)
    try:
        cmd_out = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print("IPFS add failed for {}: {}".format(content_path, e))
        sys.exit(1)
    
    hash_str = cmd_out.decode("utf-8").strip()
    cids = hash_str.splitlines()
    return cids
