# This is the install script for packages
# right now it starts with cd fs 
# that will be changed to whatever related to fake root

cd fs

# Actual start of the script
# I imagine at the begening it will check for all required folders
# but I created them manually rn as this is just some test

# I will also have to create a way to only allow certain commands
# and an option to use other commands with some extra text
# will make outputs more parsable


# Step 1, create files, starting with configs
echo "\$spark-parse-start creating-configs"
touch home/user/.spkcfg
echo "test-pkg: true" >> home/user/.spkcfg
echo "\$spark-parse-stop creating-configs"

echo "\$spark-parse-start creating-files"
mkdir usr/spk-pkg
echo "\$spark-parse-end creating-files"

# Copy shit over
echo "\$dep-start"
cp -R deps/bin fs/bin/
cp -R deps/usr/bin fs/usr/bin
echo "\$dep-end"


