x=$1

echo $1

filename=$(basename -- "$1")
echo $filename
extension="${filename##*.}"
echo $extension
filename="${filename%.*}"
echo $filename
