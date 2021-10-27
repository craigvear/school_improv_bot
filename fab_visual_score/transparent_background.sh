for file in *.gif; do convert "$file" -transparent white format png "$file"; done
