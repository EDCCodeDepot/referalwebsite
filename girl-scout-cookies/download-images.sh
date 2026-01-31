#!/bin/bash
# Download Girl Scout Cookie images from Little Brownie Bakers
# Run this script from the girl-scout-cookies directory

mkdir -p images

echo "Downloading cookie images..."

curl -sL -o images/thin-mints.png "https://www.littlebrowniebakers.com/wp-content/uploads/2023/12/Thin-Mints.png"
echo "✓ Thin Mints"

curl -sL -o images/samoas.png "https://www.littlebrowniebakers.com/wp-content/uploads/2023/12/Samoas.png"
echo "✓ Samoas"

curl -sL -o images/tagalongs.png "https://www.littlebrowniebakers.com/wp-content/uploads/2023/12/Tagalongs.png"
echo "✓ Tagalongs"

curl -sL -o images/do-si-dos.png "https://www.littlebrowniebakers.com/wp-content/uploads/2023/12/Do-si-dos.png"
echo "✓ Do-si-dos"

curl -sL -o images/trefoils.png "https://www.littlebrowniebakers.com/wp-content/uploads/2023/12/Trefoils.png"
echo "✓ Trefoils"

curl -sL -o images/lemonades.png "https://www.littlebrowniebakers.com/wp-content/uploads/2023/12/Lemonades.png"
echo "✓ Lemonades"

curl -sL -o images/lemon-ups.png "https://www.littlebrowniebakers.com/wp-content/uploads/2023/12/Lemon-Ups.png"
echo "✓ Lemon-Ups"

curl -sL -o images/adventurefuls.png "https://www.littlebrowniebakers.com/wp-content/uploads/2023/12/Adventurefuls.png"
echo "✓ Adventurefuls"

curl -sL -o images/toffee-tastic.png "https://www.littlebrowniebakers.com/wp-content/uploads/2023/12/Toffee-tastic.png"
echo "✓ Toffee-tastic"

curl -sL -o images/caramel-chocolate-chip.png "https://www.littlebrowniebakers.com/wp-content/uploads/2023/12/Caramel-Chocolate-Chip.png"
echo "✓ Caramel Chocolate Chip"

curl -sL -o images/smores.png "https://www.littlebrowniebakers.com/wp-content/uploads/2023/12/Smores.png"
echo "✓ S'mores"

echo ""
echo "Done! All images downloaded to ./images/"
echo "Now run: git add images/ && git commit -m 'Add cookie images' && git push"
