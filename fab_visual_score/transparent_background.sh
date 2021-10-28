for file in *.png; do convert "$file" -transparent white "$file"; done
