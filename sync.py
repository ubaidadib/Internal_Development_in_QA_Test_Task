import os
import time
import hashlib

# Here is a Python program that synchronizes the contents of the source folder with the replica folder.
# It does this by comparing the contents of both folders, and making any necessary changes to the replica
#  folder to ensure that it is an exact copy of the source folder.

# The synchronization is performed periodically by using the time module to pause the program for a specified
#  amount of time between synchronizations.

# To calculate the MD5 hash of a file, the program uses the hashlib library.

def sync_folders(source, replica):
  # Compare the contents of the source and replica folders
  for root, dirs, files in os.walk(source):
    # Iterate through the files in the source folder
    for file in files:
      # Calculate the relative path of the file in both the source and replica folders
      source_path = os.path.join(root, file)
      replica_path = source_path.replace(source, replica, 1)

      # Check if the file exists in the replica folder
      if not os.path.exists(replica_path):
        # If the file does not exist in the replica folder, copy it from the source folder
        print(f"Copying {source_path} to {replica_path}")
        os.makedirs(os.path.dirname(replica_path), exist_ok=True)
        with open(source_path, "rb") as f_in:
          with open(replica_path, "wb") as f_out:
            f_out.write(f_in.read())
      else:
        # If the file exists in both folders, compare their contents
        with open(source_path, "rb") as f_in:
          source_content = f_in.read()
        with open(replica_path, "rb") as f_in:
          replica_content = f_in.read()

        # Calculate the MD5 hash of the contents of both files
        source_hash = hashlib.md5(source_content).hexdigest()
        replica_hash = hashlib.md5(replica_content).hexdigest()

        # If the hashes are different, update the replica file
        if source_hash != replica_hash:
          print(f"Updating {replica_path}")
          with open(replica_path, "wb") as f_out:
            f_out.write(source_content)

  # Iterate through the files in the replica folder
  for root, dirs, files in os.walk(replica):
    for file in files:
      # Calculate the relative path of the file in both the source and replica folders
      replica_path = os.path.join(root, file)
      source_path = replica_path.replace(replica, source, 1)

      # If the file does not exist in the source folder, delete it from the replica folder
      if not os.path.exists(source_path):
        print(f"Deleting {replica_path}")
        os.remove(replica_path)

# Set the source and replica folders
source = "path/to/source/folder"
replica = "path/to/replica/folder"
sync_folders(source, replica)
 