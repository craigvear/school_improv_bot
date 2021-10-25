a=1
for i in images/*.png; do
	new=$(printf "%04d.png" "$a")
	mv -i -- "$i" "$new"
	let a=a+1
done
