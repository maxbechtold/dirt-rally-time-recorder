if [ $# -eq 0 ]
  then
    echo "No arguments supplied, 'drX' expected"
    exit 1
fi

game=$1
echo "Building for $game"
rm -f dirtrally-lb.db
sqlite3 -batch -init resources/setup-${game}.sql dirtrally-lb.db .exit 
pyinstaller timerecord.spec --noconfirm --name timerecorder-${game}

cd dist/timerecorder-${game}
rm sqlite3.exe
mv list-laptimes.bat list-laptimes.sh
mv export-laptimes.bat export-laptimes.sh
# Reduce scripts to core parts
sed -i '1d;$d' *-laptimes.sh

# Remove the following if you like to keep the executable timerecord
rm -f *.pyd
rm -f **/*.pyd
rm -f *.zip
rm -f *.dll
rm -f *.so.*
rm -f *gnu.so*
rm -f timerecord*
cp -r ../../timerecorder .
