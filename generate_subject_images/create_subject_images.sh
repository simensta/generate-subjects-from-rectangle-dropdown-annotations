#!/bin/bash

path_manifest_file=$1
path_to_images=$2
echo $path_manifest_file

function createNotation {
  manifestLine=$1
  echo "createNotation"
  new_image_name=$(echo $manifestLine | cut -d "," -f 1)
  echo ">> Image Name: "$new_image_name

  sleep 2
  url=$(echo $manifestLine | cut -d "," -f 11)
  echo  ">> URL: "$url

  curl $url -o temp.jpg

  x=$(echo $manifestLine | cut -d "," -f 5)
  y=$(echo $manifestLine | cut -d "," -f 6)
  width=$(echo $manifestLine | cut -d "," -f 7)
  height=$(echo $manifestLine | cut -d "," -f 8)
  
  echo $x
  echo $y
  echo $width
  echo $height
  echo ""

  convert temp.jpg -crop $width"x"$height"+"$x"+"$y $path_to_images/$new_image_name

}

while read manifestLine; do
  echo "--------------------------------------------------------"
  echo "--------------------------------------------------------"
  createNotation "$manifestLine"
done <$path_manifest_file
