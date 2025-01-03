if [ "$1" = "run" ]; then
    ./build/rsa
else
    mkdir -p build
    g++ -g3 -O3 main.cpp prime_generator.cpp rsa.cpp -lgmpxx -lgmp -o build/rsa
fi