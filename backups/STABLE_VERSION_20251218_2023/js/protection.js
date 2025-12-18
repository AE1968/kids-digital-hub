/**
 * 🛡️ KIDS DIGITAL HUB - PROTECTION SYSTEM
 * Comprehensive security script to prevent copying, inspecting, and stealing content.
 */

(function () {
    'use strict';

    console.log("%c🛑 STOP! 🛑", "color: red; font-size: 40px; font-weight: bold;");
    console.log("%cThis is a protected zone. All code, images, and content are copyrighted properties of Kids Digital Hub.", "font-size: 16px;");

    // 1. DISABLE RIGHT CLICK (Context Menu)
    document.addEventListener('contextmenu', function (e) {
        e.preventDefault();
        return false;
    });

    // 2. DISABLE TEXT SELECTION & DRAGGING
    // Inject CSS to stop selection
    const style = document.createElement('style');
    style.innerHTML = `
        * {
            -webkit-user-select: none !important;
            -moz-user-select: none !important;
            -ms-user-select: none !important;
            user-select: none !important;
            -webkit-user-drag: none !important;
            -khtml-user-drag: none !important;
            -moz-user-drag: none !important;
            -o-user-drag: none !important;
        }
        /* Allow selection in inputs and textareas so users can type */
        input, textarea {
            -webkit-user-select: text !important;
            -moz-user-select: text !important;
            -ms-user-select: text !important;
            user-select: text !important;
        }
    `;
    document.head.appendChild(style);

    // Disable Dragging Events
    document.ondragstart = function () { return false; };
    document.onselectstart = function () { return false; };

    // 3. DISABLE KEYBOARD SHORTCUTS
    document.addEventListener('keydown', function (e) {
        // F12 (DevTools)
        if (e.keyCode == 123) {
            e.preventDefault();
            return false;
        }

        // Ctrl+Shift+I (DevTools)
        if (e.ctrlKey && e.shiftKey && e.keyCode == 73) {
            e.preventDefault();
            return false;
        }

        // Ctrl+Shift+J (Console)
        if (e.ctrlKey && e.shiftKey && e.keyCode == 74) {
            e.preventDefault();
            return false;
        }

        // Ctrl+Shift+C (Inspect Element)
        if (e.ctrlKey && e.shiftKey && e.keyCode == 67) {
            e.preventDefault();
            return false;
        }

        // Ctrl+U (View Source)
        if (e.ctrlKey && e.keyCode == 85) {
            e.preventDefault();
            return false;
        }

        // Ctrl+S (Save Page)
        if (e.ctrlKey && e.keyCode == 83) {
            e.preventDefault();
            return false;
        }

        // Ctrl+P (Print)
        if (e.ctrlKey && e.keyCode == 80) {
            e.preventDefault();
            return false;
        }

        // Ctrl+A (Select All)
        if (e.ctrlKey && e.keyCode == 65) {
            e.preventDefault();
            return false;
        }

        // Ctrl+C (Copy)
        if (e.ctrlKey && e.keyCode == 67) {
            e.preventDefault();
            return false;
        }

        // Ctrl+X (Cut)
        if (e.ctrlKey && e.keyCode == 88) {
            e.preventDefault();
            return false;
        }
    });

    // 4. DETECT DEVTOOLS OPENING (Advanced)
    // Tries to detect if DevTools is open by checking dimension changes significantly
    // or by overriding toString of console functions. Minimal impact version:
    const element = new Image();
    Object.defineProperty(element, 'id', {
        get: function () {
            // DevTools detected
            // We could redirect or clear body, but for now we just log
            console.clear();
            console.log("%c⚠️ Security Alert ⚠️", "color: red; font-size: 20px;");
        }
    });
    console.log(element);

})();
