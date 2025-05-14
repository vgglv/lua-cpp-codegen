#pragma once
#include "Vector2.hpp"

namespace game {
    class GameObject {
    public:
        GameObject() = default;
        ~GameObject() = default;

        void setXY(const Vector2& vec);
        [[nodiscard]] Vector2 getXY() const;

    private:
        float x;
        float y;
    };
}