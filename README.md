# Spark
Spark is a simple "build from source" package installer.
## Supported platforms
- Any linux distro*
- IPhone (ISH and native)
- WSL
* - ditro's that don't use `sudo` must have commands ran with the `--no-sudo` argument.
## Screenshots
![Spark Preview Image](spark-preview.png)
![Spark Preview Image](spark-iphone.png)
## Installing
```
git clone https://github.com/HUSKI3/Spark.git
cd Spark
export PATH="$PWD:$PATH"
chmod a+x spark
```
## Setting up
```
(as root) spark -u
```

## Running
```
spark -h
or
(as root) spark -i nano 
```
