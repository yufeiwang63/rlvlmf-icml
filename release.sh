cd ..
mkdir -p vlm-reward-release
rsync -avrz --exclude-from=.gitignore --exclude=vlm-reward-release . ../vlm-reward-release/