#include "GameObject.hpp"

namespace game {
    void GameObject::setXY(const Vector2& vec) {
        x = vec.x;
        y = vec.y;
    }

    Vector2 GameObject::getXY() const {
        return Vector2{x, y};
    }
}