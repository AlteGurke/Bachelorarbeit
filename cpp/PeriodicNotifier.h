#pragma once

#include <functional>

namespace pearlrt {
    class PeriodicNotifier {
        private:
            unsigned short secondsRemaining;
        public:
            void RegisterCallback(std::function<void> callback);
            void ResetTimer();
    };
}