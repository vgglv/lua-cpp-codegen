#include <iostream>
#include "GameObject.hpp"
#include "Vector2.hpp"
#include "lua.hpp"


int main() {
    game::GameObject obj;
    obj.setXY(game::Vector2{5.f, 4.f});
    std::cout << "Hello world!\n";
    std::cout << "Object: [" << obj.getXY().x << ", " << obj.getXY().y << "]\n";
    
    return 0;
}