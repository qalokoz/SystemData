#!/bin/bash
# Set up GitHub API access token
TOKEN=<your GitHub API access token>
# Set up repository names
REPO_NAMES=("microservice1" "microservice2" "microservice3" "microservice4")
# Loop through repository names and create each repository
for i in "${REPO_NAMES[@]}"
do
   # Create repository
   curl -u <your GitHub username>:$TOKEN https://api.github.com/user/repos -d '{"name":"'$i'"}'
   # Clone repository locally
   git clone git@github.com:<your GitHub username>/$i.git
   # Add README file to repository
   echo "# $i" >> $i/README.md
   # Add and commit README file
   cd $i
   git add README.md
   git commit -m "Added README file"
   git push origin master
   cd ..
done
